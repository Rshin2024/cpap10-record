#!/usr/bin/env python3
"""Verify a CPAP-10 bundle with Python integers and bundled ECPP certificates.

Run this script in the bundle, or pass --directory PATH. No PARI, FLINT, GMP,
network access or third-party Python package is required. Manifest hashes and
saved primality/status flags are not evidence: the certificates and every
composite witness are checked mathematically.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys
import time

from check_ecpp import verify_certificate


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(path):
    def reject_constant(value):
        raise ValueError("Nonfinite JSON number: " + value)
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def integer(value, label):
    if type(value) is int:
        return value
    require(type(value) is str and value and value.isascii()
            and value.isdigit() and (value == "0" or value[0] != "0"),
            "Invalid decimal integer: " + label)
    return int(value)


def verify_evidence(manifest, proof, certificates):
    """Check parsed evidence; no saved success flag or hash grants acceptance."""
    started = time.monotonic()
    require(type(manifest) is dict and type(proof) is dict,
            "Manifest and native proof must be objects")
    p = integer(manifest["first_prime"], "first_prime")
    record = integer(manifest["comparison_record_first_prime"],
                     "comparison_record_first_prime")
    require(2 <= p < record, "First prime must be >= 2 and below comparison record")
    require(type(manifest["difference"]) is int and manifest["difference"] == 210,
            "Manifest difference must be 210")
    require(type(manifest["length"]) is int and manifest["length"] == 10,
            "Manifest length must be 10")
    require(integer(proof["first_prime"], "native first_prime") == p,
            "Native proof has the wrong first prime")
    require(type(proof["difference"]) is int and proof["difference"] == 210
            and type(proof["length"]) is int and proof["length"] == 10,
            "Native progression differs from manifest")

    targets = proof["targets"]
    require(type(targets) is list and len(targets) == 10,
            "Native proof must identify exactly ten targets")
    for j, row in enumerate(targets):
        require(type(row) is dict and type(row["index"]) is int
                and row["index"] == j
                and integer(row["integer"], "target integer") == p + 210*j,
                "Native target identity differs at index " + str(j))

    expected = set(range(1, 1890)) - set(range(210, 1890, 210))
    checks = proof["intermediate_checks"]
    require(type(checks) is list and len(checks) == 1881,
            "Native proof must supply exactly 1881 intermediate witnesses")
    seen = set()
    counts = Counter()
    for row in checks:
        require(type(row) is dict and type(row["offset"]) is int,
                "Intermediate offset must be an integer")
        offset = row["offset"]
        require(offset in expected and offset not in seen,
                "Unexpected or duplicate intermediate offset: " + str(offset))
        seen.add(offset)
        n = p + offset
        require(integer(row["integer"], "intermediate integer") == n,
                "Wrong intermediate integer at offset " + str(offset))
        method = row["method"]
        if method == "proper_factor":
            factor = integer(row["factor"], "factor")
            cofactor = integer(row["cofactor"], "cofactor")
            require(1 < factor < n and cofactor > 1 and factor*cofactor == n,
                    "Invalid proper factor at offset " + str(offset))
        elif method == "Fermat_witness":
            base = integer(row["base"], "Fermat base")
            exponent = integer(row["exponent"], "Fermat exponent")
            residue = integer(row["residue"], "Fermat residue")
            require(1 < base < n and exponent == n-1
                    and math.gcd(base, n) == 1,
                    "Invalid Fermat parameters at offset " + str(offset))
            require(pow(base, exponent, n) == residue and residue != 1,
                    "Invalid Fermat residue at offset " + str(offset))
        else:
            raise ValueError("Unsupported composite method: " + str(method))
        counts[method] += 1
    require(seen == expected, "Missing intermediate offsets")

    require(type(certificates) is list and len(certificates) == 10,
            "Exactly ten prime certificates are required")
    for j, cert in enumerate(certificates):
        # verify_certificate checks the ECPP theorem, the curve operations,
        # the entire chain and a deterministic terminal-prime test.
        verify_certificate(cert, p + 210*j)
    return dict(verified_cpap=True, first_prime=str(p), difference=210, length=10,
                verified_prime_targets=10, verified_intermediate_composites=1881,
                first_prime_below_comparison_record=True,
                composite_method_counts=dict(counts),
                seconds=round(time.monotonic()-started, 6))


def verify_bundle(directory):
    directory = Path(directory)
    manifest = load_json(directory / "manifest.json")
    proof = load_json(directory / "evidence" / "native-proof.json")
    certificates = [load_json(directory / "certificates" /
                              ("prime-%02d.pari.gp" % j)) for j in range(10)]
    return verify_evidence(manifest, proof, certificates)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path,
                        default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        result = verify_bundle(args.directory)
    except Exception as error:
        print(json.dumps(dict(verified_cpap=False,
                              error=type(error).__name__ + ": " + str(error))),
              file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

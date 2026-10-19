# CPAP-10 smaller than the listed record

The ten consecutive primes are `p + 210*j`, for `j = 0, 1, ..., 9`, where

```text
p = 100664739940046026209780422559742894159699605500571118110426323232564146473609861537109142019
```

The common difference is **210** and the total span is **1,890**. The first
prime has 93 decimal digits.

This progression was found on **2026-10-19 at 01:57:08 UTC**. Its first term
is **0.328952959% smaller** than the CPAP-10 record listed in the
[CPAP minimal-solutions table](https://www.pzktupel.de/CPAP/mini.php) when
fetched on 2026-10-19 at 02:00:07 UTC:

```text
100996972469714247637786655587969840329509324689190041803603417758904341703348882159067229719
```

This establishes an improvement over that listed record. It does not establish
an absolute global minimum.

## Verify

From this repository folder, run with Python 3:

```sh
python3 -E -S -B check_cpap10_bundle.py
```

No external Python packages or network connection are required. The checker
verifies ECPP certificates for all ten primes and recomputes exact composite
witnesses for all **1,881** other integers between the first and last prime.
It also checks that the first prime is below the stated comparison record.
Success prints `verified_cpap: true`, 10 verified prime targets and 1,881
verified intermediate composites. A failed check returns a nonzero exit code.

To verify a different copy of this bundle, use `--directory PATH`.

## Files

- `manifest.json`: exact progression, comparison and mathematical search expression.
- `certificates/`: ten PARI ECPP vectors, with Primo and readable exports.
- `evidence/native-proof.json`: 1,832 proper-factor and 49 Fermat witnesses.
- `check_ecpp.py`: standalone certificate checker using Python integer arithmetic.
- `check_cpap10_bundle.py`: complete progression and consecutiveness checker.
- `PROVENANCE.json`: software versions and relative proof-file hashes.
- `SHA256SUMS.txt`: integrity hashes; mathematical verification does not rely on them.

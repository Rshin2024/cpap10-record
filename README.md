# CPAP-10: verified 82-digit result

The ten consecutive primes are `p + 210*n`, for `n = 0, 1, ..., 9`, where

```text
p = 8712622385791862675085445195128970899134595793931334268640816440149827258572241659
```

The common difference is **210**, the total span is **1,890**, and the first
prime has **82 digits**, below the search target of `10^83`.

This progression was discovered on **21 October 2026**. Its first prime is
about **11.59 billion times smaller** than the 93-digit CPAP-10 first term
listed in the [CPAP minimal-solutions table](https://www.pzktupel.de/CPAP/mini.php)
when fetched on 21 October 2026 at 14:54:39 UTC. This is a verified improvement
over that listed result; no global minimum is claimed.

[Download the proof archive](cpap10-82digit-proof.zip) ·
[Archive SHA-256](cpap10-82digit-proof.zip.sha256) ·
[Browse the proof package](records/82-digit/)

## Verify the 82-digit result

From the repository root, run:

```sh
python3 -E -S -B records/82-digit/check_cpap10_bundle.py
```

The checker uses Python's standard library and the bundled integer-arithmetic
ECPP checker. No external packages or network connection are required. It
verifies **all ten prime certificates** and **all 1,881 intervening composites**:
1,822 proper-factor witnesses and 59 Fermat witnesses. A successful run reports
`verified_cpap: true`, ten verified prime targets, and 1,881 verified composites.

The ZIP contains the same standalone package. Extract it and run
`python3 -E -S -B check_cpap10_bundle.py` from the extracted `cpap10-82digit` folder.
See its [README](records/82-digit/README.md) and
[provenance](records/82-digit/PROVENANCE.json) for the exact search expression
and proof formats. `SHA256SUMS.txt` at the repository root covers every tracked
file except itself; the proof package also has its own checksum manifest.

## Earlier 93-digit result

The earlier proof files remain at the repository root, including
[the original archive](cpap10-record.zip), its certificates, and its checker.
The previous documentation is preserved in [README-93-digit.md](README-93-digit.md),
and the original publication is available at
[commit 5e618ab](https://github.com/Rshin2024/cpap10-record/tree/5e618ab8d197a84cbd5f9ba94b73cc70d76c65ea).
To verify that earlier result, run `python3 -E -S -B check_cpap10_bundle.py`.

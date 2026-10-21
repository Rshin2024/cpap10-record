# CPAP-10 with an 82-digit first prime

The ten consecutive primes are `p + 210*j`, for `j = 0, 1, ..., 9`, where

```text
p = 8712622385791862675085445195128970899134595793931334268640816440149827258572241659
```

The common difference is **210** and the total span is **1,890**. Every one of
the **1,881** other integers between the first and last prime is composite.
The first native proof report is dated **2026-10-21 at 14:51:48 UTC**.

At **2026-10-21 at 14:54:39 UTC**, the first-ranked CPAP-10 in the
[minimal-solutions table](https://www.pzktupel.de/CPAP/mini.php) had this
93-digit first prime:

```text
100996972469714247637786655587969840329509324689190041803603417758904341703348882159067229719
```

That listed first prime divided by this first prime is approximately
**11,592,029,127.122**. This result improves that dated table entry; no global
minimum is claimed. The search required `p < 10^83`.

## Verify

From this folder, run with Python 3:

```sh
python3 -E -S -B check_cpap10_bundle.py
```

No external Python package or network connection is needed. The checker
replays ten ECPP certificates and recomputes all 1,881 composite witnesses.
Success prints `"verified_cpap": true`, 10 verified prime targets, and 1,881
verified intermediate composites. Failure returns a nonzero exit code.
To verify another copy, add `--directory PATH`.

## Mathematical search expression

```text
p = 52299822424501 * 173# + x
x = 47097732608367487943628591116141852609567776190912870462611636356949
173# = 166589903787325219380851695350896256250980509594874862046961683989710
```

Here `173#` means the product of all primes at most 173.

## Files

- `manifest.json`: exact progression, search expression, and dated comparison.
- `certificates/`: ten ECPP vectors with Primo and readable exports.
- `evidence/native-proof.json`: 1,822 proper-factor and 59 Fermat witnesses.
- `check_ecpp.py`: standalone ECPP checker using Python integer arithmetic.
- `check_cpap10_bundle.py`: complete progression and consecutiveness checker.
- `PROVENANCE.json`: public software and proof-file provenance.
- `SHA256SUMS.txt`: integrity hashes; mathematical verification does not rely on them.

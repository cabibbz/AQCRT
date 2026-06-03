"""Golden-values regression test for the chi_F pipeline.

Run every sprint (it is wired into loop.sh as a pre-sprint gate). Fast (<60s, CPU-OK).
It asserts the chi_F machinery against KNOWN-EXACT anchors, so the error classes this
project has shipped before become impossible to ship silently:

  * factor-2 / per-site / absolute-scale error (Sprint 125): caught by the q=2 closed
    form chi_F == (n-1)/4 -- a 2x prefactor mistake fails this immediately.
  * Hamiltonian / estimator drift: caught by reproducing the stored results.db values
    (q=3 n=8 = 11.868345, q=4 n=8 = 45.527791) to ~1e-4.
  * INVERTED exponent framing (Sprint 129): the convention is *proven* trustworthy by
    showing q=2 and q=3 per-site effective exponents converge to their EXACT nulls
    (2/nu-d = 1.0 and 1.4); therefore the same convention's q=4 null is 2.0 -- asserted
    explicitly so "q=4 alpha=1.77, reject 2" can never again be recorded as a result.

Usage:  python test_golden.py        (exit 0 = all pass, 1 = a golden anchor broke)
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hamiltonian_utils import build_sq_potts_parts
from fss_utils import fit_power_law, pairwise_exponents
from chif_utils import chi_F_exact, chi_F_q2_closed_form, expected_persite_exponent

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def chi_series(q, sizes, g_c=None):
    g_c = (1.0 / q) if g_c is None else g_c
    out = []
    for n in sizes:
        Hc, Hf = build_sq_potts_parts(n, q)
        out.append(chi_F_exact(Hc, Hf, g_c, n))
    return np.array(sizes, float), np.array(out)


def main():
    t0 = time.time()
    print("=" * 70)
    print("GOLDEN-VALUES REGRESSION (chi_F pipeline)")
    print("=" * 70)

    # 1. q=2 closed form: chi_F == (n-1)/4  (pins factor-2 + per-site /n + absolute scale)
    print("\n[1] q=2 TFIM closed form  chi_F == (n-1)/4")
    s2, c2 = chi_series(2, [6, 8, 10, 12])
    for n, v in zip(s2, c2):
        exact = chi_F_q2_closed_form(n)
        check(f"q2 n={int(n)} chi_F={v:.6f} vs {exact:.6f}",
              abs(v - exact) / exact < 1e-3, f"reldiff {abs(v-exact)/exact:.1e}")

    # 2. Regression anchors against stored results.db values
    print("\n[2] results.db regression anchors")
    Hc, Hf = build_sq_potts_parts(8, 3); v3 = chi_F_exact(Hc, Hf, 1/3, 8)
    check("q3 n=8 == 11.868345 (DB)", abs(v3 - 11.868345) < 1e-3, f"got {v3:.6f}")
    Hc, Hf = build_sq_potts_parts(8, 4); v4 = chi_F_exact(Hc, Hf, 0.25, 8)
    check("q4 n=8 == 45.527791 (DB)", abs(v4 - 45.527791) < 2e-3, f"got {v4:.6f}")

    # 3. Convention is trustworthy: q=2,3 effective exponents -> their EXACT nulls
    print("\n[3] per-site effective exponents converge to the derived null 2/nu-d")
    s2, c2 = chi_series(2, [8, 10, 12, 14])
    a2 = fit_power_law(s2, c2)['alpha']
    null2 = expected_persite_exponent(2)
    check(f"q=2 effective alpha={a2:.3f} -> null {null2}", abs(a2 - null2) < 0.12,
          f"|a-null|={abs(a2-null2):.3f}")
    s3, c3 = chi_series(3, [6, 8, 10])
    p3 = pairwise_exponents(s3, c3)[-1]['alpha']  # largest-n local slope
    null3 = expected_persite_exponent(3)
    check(f"q=3 largest-n local alpha={p3:.3f} approaching null {null3}",
          1.30 < p3 < 1.60, f"in (1.30,1.60), null={null3}")

    # 4. ANTI-INVERSION GATE: q=4 null is 2.0, and measured is finite-size BELOW it.
    print("\n[4] anti-inversion gate (Sprint 129)")
    null4 = expected_persite_exponent(4)
    check("expected_persite_exponent(4) == 2.0  (the CORRECT q=4 exponent)",
          null4 == 2.0, f"got {null4}")
    check("nulls are exact: q2,q3,q4 = 1.0,1.4,2.0",
          [expected_persite_exponent(q) for q in (2, 3, 4)] == [1.0, 1.4, 2.0])
    # measured q=4 effective exponent (CPU sizes) must sit BELOW 2 (finite-size marginal log),
    # and must NOT be mistaken for the asymptote.
    s4, c4 = chi_series(4, [6, 8, 10])
    a4 = fit_power_law(s4, c4)['alpha']
    check(f"q=4 measured alpha={a4:.3f} is finite-size BELOW null 2.0 (NOT 'reject 2')",
          1.6 < a4 < 2.0, f"effective {a4:.3f} < null {null4}; gap = marginal-operator log")

    dt = time.time() - t0
    print("\n" + "=" * 70)
    print(f"GOLDEN: {len(PASS)} passed, {len(FAIL)} failed  ({dt:.1f}s)")
    if FAIL:
        print("FAILED:", ", ".join(FAIL))
    print("=" * 70)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

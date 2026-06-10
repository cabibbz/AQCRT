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
    (2/nu-d = 1.0 and 1.4); therefore the same convention's q=4 null is 2.0. NOTE
    (audit 2026-06-09): the "2.0 + finite-size-below-it" reading is the STANDING
    INTERPRETATION (S129/S130 + exact nu from literature), not unfalsifiable dogma --
    overturning it requires new evidence AND an explicit update to this gate.
  * thermal-gap EP estimator drift (Sprint 136 pipeline, via ep_utils): frozen q=2
    anchors for Im(g_EP) and its ~L^{-1} scaling.
  * hybrid-model builder drift: frozen chi_F anchor (results.db sprint 126).
  * GPU/CPU backend divergence: eigsh parity above the 50k GPU threshold (only when
    a GPU is present; skipped, loudly, otherwise).

Usage:  python test_golden.py        (exit 0 = all pass, 1 = a golden anchor broke)
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hamiltonian_utils import build_sq_potts_parts, build_hybrid_parts
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

    # 5. Thermal-gap EP estimator (Sprint 136 pipeline, shared impl in ep_utils.py).
    #    Frozen deterministic anchors: fixed windows, dense path, no GPU needed.
    print("\n[5] thermal-gap EP estimator anchors (q=2, ep_utils)")
    from ep_utils import im_gEP_estimate
    EP_ANCHORS = {6: (0.38, 0.49, 0.250022), 8: (0.41, 0.51, 0.191368),
                  10: (0.43, 0.52, 0.154521)}
    ims = {}
    for n, (lo, hi, ref) in EP_ANCHORS.items():
        r = im_gEP_estimate(2, n, lo, hi)
        ims[n] = r['im_gEP']
        check(f"q2 n={n} Im(g_EP)={r['im_gEP']:.6f} vs frozen {ref:.6f}",
              abs(r['im_gEP'] - ref) / ref < 1e-4, f"reldiff {abs(r['im_gEP']-ref)/ref:.1e}")
    sl = (np.log(ims[10]) - np.log(ims[6])) / (np.log(10) - np.log(6))
    check(f"q2 Im(g_EP) slope={sl:.3f} in (-1.05,-0.85) (Ising 1/nu=1)",
          -1.05 < sl < -0.85)

    # 6. Hybrid-model builder anchor (frozen from results.db sprint 126)
    print("\n[6] hybrid builder anchor")
    Hc, Hf = build_hybrid_parts(8, 4)
    herm = abs(Hc - Hc.T).max() + abs(Hf - Hf.T).max()
    check("hybrid q4 n8 builders Hermitian", herm < 1e-12, f"max|H-H^T|={herm:.1e}")
    vh = chi_F_exact(Hc, Hf, 0.393, 8)
    check("hybrid q4 n8 chi_F(g=0.393) == 13.064844 (DB s126)",
          abs(vh - 13.064844) < 2e-3, f"got {vh:.6f}")

    # 7. GPU/CPU eigsh parity above the 50k backend threshold (audit 2026-06-09:
    #    the two backends ordered eigenvalues differently on one path; assert parity)
    print("\n[7] GPU/CPU eigsh parity (dim > 50k)")
    from gpu_utils import GPU_ENABLED, eigsh as g_eigsh
    if GPU_ENABLED:
        from scipy.sparse.linalg import eigsh as s_eigsh
        Hc2, Hf2 = build_sq_potts_parts(16, 2)         # dim 65536 > 50000 -> GPU branch
        H = Hc2 + 0.5 * Hf2
        ev_g = g_eigsh(H, k=3, which='SA', return_eigenvectors=False)
        ev_c = np.sort(s_eigsh(H, k=3, which='SA', return_eigenvectors=False))
        d = float(np.max(np.abs(ev_g - ev_c)))
        check("GPU vs CPU lowest-3 eigenvalues agree (ascending both)", d < 1e-8,
              f"max|diff|={d:.1e}")
    else:
        print("  [SKIP] GPU unavailable -- parity not checkable on this machine "
              "(gpu_utils will warn loudly at runtime)")

    dt = time.time() - t0
    print("\n" + "=" * 70)
    print(f"GOLDEN: {len(PASS)} passed, {len(FAIL)} failed  ({dt:.1f}s)")
    if FAIL:
        print("FAILED:", ", ".join(FAIL))
    print("=" * 70)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

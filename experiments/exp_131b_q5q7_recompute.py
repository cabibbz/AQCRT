"""Sprint 131b: Independently recompute exact chi_F at CPU-accessible sizes for q=5, q=7.

Verifies the *raw data* underlying the alpha reconciliation (exp_131a) -- confirms the stored
(GPU-computed, Sprints 126-128) chi_F values reproduce with scipy on CPU, so the q=5/q=7
discrepancy is purely a fit/transcription artifact, not a data artifact.

Uses the identical canonical estimator: chi_F = (2 - |<0|+>|^2 - |<0|->|^2)/(dg^2 n), dg=1e-4,
g_c = 1/q (exact self-dual). CPU sizes only: q=5 n<=8 (390k), q=7 n<=7 (823k).
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gpu_utils import eigsh
from hamiltonian_utils import build_sq_potts_parts

def chi_F_exact(H_coup, H_field, g_c, n, dg=1e-4):
    Hp = H_coup + (g_c + dg) * H_field
    Hm = H_coup + (g_c - dg) * H_field
    H0 = H_coup + g_c * H_field
    _, v0 = eigsh(H0, k=1, which='SA')
    _, vp = eigsh(Hp, k=1, which='SA')
    _, vm = eigsh(Hm, k=1, which='SA')
    psi0, psip, psim = v0[:, 0], vp[:, 0], vm[:, 0]
    if np.dot(psi0, psip) < 0: psip = -psip
    if np.dot(psi0, psim) < 0: psim = -psim
    ov_p = np.dot(psi0, psip)**2
    ov_m = np.dot(psi0, psim)**2
    return (2.0 - ov_p - ov_m) / (dg**2 * n)

# Stored values to verify (from exp_127a prior_data + new_points / results.db)
STORED = {
    5: {4: 30.943214, 6: 72.624695, 8: 132.424150},
    7: {4: 117.243073, 6: 333.985930, 7: 501.054584},
}

results = {'experiment': '131b_q5q7_recompute', 'sprint': 131, 'checks': []}
def save():
    p = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_131b_q5q7_recompute.json')
    with open(p, 'w') as f:
        json.dump(results, f, indent=2, default=str)

print("=" * 72)
print("Sprint 131b: CPU recompute of exact chi_F (verify raw data)")
print("=" * 72)
print(f"{'q':>2} {'n':>3} {'dim':>10} {'recomputed':>14} {'stored':>14} {'rel.diff':>10} {'t(s)':>6}")

max_rel = 0.0
for q in (5, 7):
    g_c = 1.0 / q
    for n in sorted(STORED[q]):
        dim = q**n
        t0 = time.time()
        Hc, Hf = build_sq_potts_parts(n, q)
        chi = chi_F_exact(Hc, Hf, g_c, n)
        dt = time.time() - t0
        stored = STORED[q][n]
        rel = abs(chi - stored) / stored
        max_rel = max(max_rel, rel)
        print(f"{q:>2} {n:>3} {dim:>10,} {chi:>14.6f} {stored:>14.6f} {rel:>10.2e} {dt:>6.1f}")
        results['checks'].append({'q': q, 'n': n, 'dim': dim, 'recomputed': float(chi),
                                  'stored': stored, 'rel_diff': float(rel), 'time_s': round(dt, 1)})
        save()

results['max_rel_diff'] = float(max_rel)
results['verdict'] = 'DATA REPRODUCES (CPU scipy == GPU stored)' if max_rel < 1e-4 else 'MISMATCH'
print(f"\nMax relative difference: {max_rel:.2e}  -> {results['verdict']}")
save()
print("Saved results/sprint_131b_q5q7_recompute.json")

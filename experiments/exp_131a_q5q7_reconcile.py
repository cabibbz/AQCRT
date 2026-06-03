"""Sprint 131a: Reconcile the S_q chi_F walking exponents at q=5 and q=7.

The canonical alpha(q) table (KNOWLEDGE.md, sprints/sprint_128.md) lists
  q=5 -> 2.139,  q=7 -> 2.584
but results.db (Sprint 127, exact_chif_power_law) and CHANGELOG list
  q=5 -> 2.094,  q=7 -> 2.636.
q=3, 4, 6 agree between the two. This script reproduces the canonical fits from the raw
exact chi_F series, cross-checks pairwise + Sprint-128c extrapolation, tries to locate the
origin of the stale values, and refits alpha(q) with the corrected numbers.

Pure analysis (no eigsh) -- runs in seconds. Raw chi_F values are the exact (finite-difference,
dg=1e-4, per-site) values computed in Sprints 126-128 with `chi_F_exact`; see exp_127a/128a.
exp_131b independently recomputes the CPU-accessible ones to verify the data itself.
"""
import numpy as np
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from fss_utils import fit_power_law, pairwise_exponents
from db_utils import record

# ---- Canonical exact chi_F series (per-site, dg=1e-4), as computed in Sprints 126-128 ----
# Source: exp_127a prior_data + new_points; q=6 from results.db (Sprint 128a chi_F_exact).
SERIES = {
    3: {4: 4.086420, 6: 7.717202, 8: 11.868345, 10: 16.456744, 12: 21.427516, 14: 26.741043},
    4: {4: 12.839321, 6: 27.138030, 8: 45.527791, 9: 56.183728, 10: 67.784201, 11: 80.310875},
    5: {4: 30.943214, 6: 72.624695, 8: 132.424150, 9: 169.455103, 10: 211.410717},
    6: {4: 63.565710, 5: 107.344523, 6: 164.724878, 7: 237.086100, 8: 325.804672, 9: 432.259953},
    7: {4: 117.243073, 6: 333.985930, 7: 501.054584, 8: 715.699344},
}
# What the DB currently holds (Sprint 127/128 exact_chif_power_law):
DB_ALPHA = {3: 1.4676, 4: 1.7945, 5: 2.0944, 6: 2.3749, 7: 2.6357}
# What KNOWLEDGE.md / sprint_128.md currently list:
KB_ALPHA = {3: 1.468, 4: 1.794, 5: 2.139, 6: 2.375, 7: 2.584}

results = {'experiment': '131a_q5q7_reconcile', 'sprint': 131, 'fits': {}, 'origin_probe': {},
           'alpha_q_refit': {}}

def save():
    p = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_131a_q5q7_reconcile.json')
    with open(p, 'w') as f:
        json.dump(results, f, indent=2, default=str)

print("=" * 78)
print("Sprint 131a: reconcile S_q chi_F walking exponents")
print("=" * 78)

# ---- Phase 1: reproduce canonical fit_power_law for every q ----
print("\n[Phase 1] Canonical fit_power_law (linear-space NLS, uniform weights):")
print(f"{'q':>2} {'sizes':>22} {'alpha (refit)':>14} {'DB':>8} {'KB':>8} {'match?':>18}")
alpha_canon = {}
for q in sorted(SERIES):
    sizes = np.array(sorted(SERIES[q]), dtype=float)
    chi = np.array([SERIES[q][int(s)] for s in sizes])
    fit = fit_power_law(sizes, chi)
    a = fit['alpha']
    alpha_canon[q] = a
    db, kb = DB_ALPHA[q], KB_ALPHA[q]
    tag = "DB ok" if abs(a - db) < 0.005 else "DB MISMATCH"
    tag += "; KB ok" if abs(a - kb) < 0.005 else "; KB STALE"
    print(f"{q:>2} {str([int(s) for s in sizes]):>22} {a:>9.4f}+/-{fit['alpha_err']:.4f} "
          f"{db:>8.3f} {kb:>8.3f}   {tag}")
    results['fits'][q] = {'sizes': [int(s) for s in sizes], 'chi_F': list(chi),
                          'alpha': a, 'alpha_err': fit['alpha_err'], 'r_squared': fit['r_squared'],
                          'db_alpha': db, 'kb_alpha': kb,
                          'pairwise': pairwise_exponents(sizes, chi)}

# ---- Phase 2: pairwise + extrapolation cross-check for q=5, q=7 ----
print("\n[Phase 2] Cross-checks for the two disputed exponents:")
for q in (5, 7):
    sizes = np.array(sorted(SERIES[q]), dtype=float)
    chi = np.array([SERIES[q][int(s)] for s in sizes])
    pw = pairwise_exponents(sizes, chi)
    print(f"\n  q={q}: canonical={alpha_canon[q]:.4f}  (DB={DB_ALPHA[q]}, KB stale={KB_ALPHA[q]})")
    print("    pairwise: " + "  ".join(f"({p['n1']},{p['n2']})={p['alpha']:.4f}" for p in pw))

# ---- Phase 3: hunt for the origin of the stale 2.139 / 2.584 ----
print("\n[Phase 3] Origin probe -- which fit (if any) reproduces the stale value?")
def logspace_alpha(sizes, chi):
    """Equal-weight log-log linear fit (vs fit_power_law's linear-space NLS)."""
    return np.polyfit(np.log(sizes), np.log(chi), 1)[0]

for q, stale in ((5, 2.139), (7, 2.584)):
    full = sorted(SERIES[q])
    cand = {}
    cand['fit_power_law_full'] = alpha_canon[q]
    cand['logspace_full'] = logspace_alpha(np.array(full, float),
                                           np.array([SERIES[q][n] for n in full], float))
    # subset fits (drop largest / drop smallest / consecutive triples)
    for drop in ('drop_largest', 'drop_smallest'):
        sub = full[:-1] if drop == 'drop_largest' else full[1:]
        s = np.array(sub, float); c = np.array([SERIES[q][n] for n in sub], float)
        cand[f'fit_power_law_{drop}'] = fit_power_law(s, c)['alpha']
        cand[f'logspace_{drop}'] = logspace_alpha(s, c)
    # smallest pair (the 4,6 leg) -- candidate seed for the stale value
    s2 = np.array(full[:2], float); c2 = np.array([SERIES[q][n] for n in full[:2]], float)
    cand['pairwise_smallest'] = logspace_alpha(s2, c2)
    hit = [k for k, v in cand.items() if abs(v - stale) < 0.01]
    print(f"\n  q={q} stale={stale}:")
    for k, v in cand.items():
        mark = "  <== reproduces stale" if abs(v - stale) < 0.01 else ""
        print(f"    {k:24s} {v:.4f}{mark}")
    results['origin_probe'][q] = {'stale': stale, 'candidates': cand, 'reproduced_by': hit}

# ---- Phase 4: refit alpha(q) with stale vs corrected values ----
print("\n[Phase 4] alpha(q) refit -- effective walking-exponent curve (q=3..7):")
qs = np.array([3, 4, 5, 6, 7], float)
lnq = np.log(qs)
for label, table in (('STALE (old KB/sprint128)', KB_ALPHA),
                     ('CORRECTED (canonical)', {q: alpha_canon[q] for q in (3,4,5,6,7)})):
    a = np.array([table[int(q)] for q in qs])
    # linear in ln q
    c1 = np.polyfit(lnq, a, 1)
    resid1 = a - np.polyval(c1, lnq)
    chi2dof_1 = np.sum(resid1**2) / (len(qs) - 2)
    # quadratic in ln q
    c2 = np.polyfit(lnq, a, 2)
    resid2 = a - np.polyval(c2, lnq)
    chi2dof_2 = np.sum(resid2**2) / (len(qs) - 3)
    # local slopes d alpha / d ln q (monotonic? = convex signature)
    dadlnq = np.diff(a) / np.diff(lnq)
    print(f"\n  {label}:")
    print(f"    linear:    alpha = {c1[0]:.4f} ln q + {c1[1]:.4f}   "
          f"chi2/dof={chi2dof_1:.4f}  max|resid|={np.max(np.abs(resid1)):.4f}")
    print(f"    quadratic: {c2[0]:.4f} (ln q)^2 + {c2[1]:.4f} ln q + {c2[2]:.4f}  "
          f"chi2/dof={chi2dof_2:.4f}")
    print(f"    local slopes d_alpha/d_lnq: "
          + ", ".join(f"{x:.3f}" for x in dadlnq)
          + ("   [monotonic increasing -> convex/super-log]" if np.all(np.diff(dadlnq) > 0)
             else "   [non-monotonic]"))
    results['alpha_q_refit'][label] = {
        'alpha_values': {int(q): table[int(q)] for q in qs},
        'linear': {'slope': c1[0], 'intercept': c1[1], 'chi2_dof': chi2dof_1,
                   'max_resid': float(np.max(np.abs(resid1)))},
        'quadratic': {'a': c2[0], 'b': c2[1], 'c': c2[2], 'chi2_dof': chi2dof_2},
        'local_slopes': [float(x) for x in dadlnq],
        'monotonic_increasing': bool(np.all(np.diff(dadlnq) > 0)),
    }

# Record the corrected alpha(q) linear-fit coefficients to DB (derived quantity)
cc = results['alpha_q_refit']['CORRECTED (canonical)']['linear']
record(sprint=131, model='sq', q=0, n=7, quantity='alpha_q_slope',
       value=cc['slope'], error=None, method='lnq_linear_corrected',
       notes=f"alpha(q)={cc['slope']:.4f}ln q+{cc['intercept']:.4f}; q=5->{alpha_canon[5]:.4f}, q=7->{alpha_canon[7]:.4f}")

save()
print("\nSaved results/sprint_131a_q5q7_reconcile.json")

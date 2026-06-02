"""Sprint 130c: q=4 (4-state Potts) chi_F FSS -- THE TEST.

Same four estimators, calibrated on q=2 (130a) and q=3 (130b). q=4: nu=2/3
(literature) -> 1/nu=1.5, 2/nu-d = 2.0 (Albuquerque et al.); g_c=1/4 exact.
q=4 has the marginal (dilution, c=1) operator -> multiplicative log corrections,
so finite-size estimators are expected biased BELOW their asymptotes. The
at-g_c value at n<=11 is ~1.77 (KNOWLEDGE.md); this sprint asks whether the
g_c-assumption-free peak-HEIGHT exponent and the full-curve collapse tell the
same finite-size story, and how far they sit from the targets a=2.0 / 1/nu=1.5.
CPU-only -> n<=10.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from collapse_utils import scan_curve, peak_from_curve, chi_at, collapse_scan, collapse_scan_2d
from hamiltonian_utils import build_sq_potts_parts
from fss_utils import fit_power_law, pairwise_exponents
from db_utils import record

Q = 4
G_C = 1.0 / Q
SIZES = [5, 6, 7, 8, 9, 10]
KAPPA0 = 1.5                       # nu=2/3
THEORY_INV_NU = 1.5
THEORY_A = 2.0 / (2.0 / 3.0) - 1.0   # = 2.0
X_LO, X_HI, M = -2.5, 2.5, 17

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_130c_fss_q4.json')
results = {
    'experiment': '130c_fss_q4', 'sprint': 130, 'q': Q, 'g_c': G_C,
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'kappa0_window': KAPPA0, 'x_window': [X_LO, X_HI, M],
    'theory': {'inv_nu': THEORY_INV_NU, 'a_2nu_minus_d': THEORY_A},
    'points': [], 'curves': [],
}

def save():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2, default=str)

print("=" * 78)
print(f"Sprint 130c: q={Q} chi_F FSS TEST (g_c={G_C}, target 1/nu->1.5, a->2.0)")
print("=" * 78)

curves = []
for n in SIZES:
    t0 = time.time()
    Hc, Hf = build_sq_potts_parts(n, Q)
    xlo, xhi = X_LO, X_HI
    for attempt in range(2):
        gs = G_C + np.linspace(xlo, xhi, M) * (n ** (-KAPPA0))
        gs = gs[gs > 1e-4]
        mids, chi = scan_curve(Hc, Hf, n, gs)
        pk = peak_from_curve(mids, chi)
        if not pk['edge']:
            break
        xlo, xhi = 1.6 * xlo, 1.6 * xhi
    at_gc = chi_at(mids, chi, G_C)
    rec = {'n': n, 'dim': Q ** n, 'gstar': pk['gstar'], 'chi_peak': pk['chi_peak'],
           'shift': pk['gstar'] - G_C, 'at_gc': at_gc, 'edge': pk['edge'],
           'time_s': round(time.time() - t0, 1)}
    curves.append({'n': n, 'mids': mids.tolist(), 'chi': chi.tolist()})
    results['points'].append(rec)
    results['curves'].append(curves[-1])
    print(f"  n={n:2d} dim={Q**n:>9,} g*={pk['gstar']:.5f} shift={rec['shift']:+.5f} "
          f"chi_peak={pk['chi_peak']:.4f} chi(g_c)={at_gc:.4f} edge={pk['edge']} ({rec['time_s']}s)")
    save()

sizes = np.array([r['n'] for r in results['points']], float)
heights = np.array([r['chi_peak'] for r in results['points']], float)
atgc = np.array([r['at_gc'] for r in results['points']], float)
shifts = np.abs(np.array([r['shift'] for r in results['points']], float))

fit_h = fit_power_law(sizes, heights)
fit_g = fit_power_law(sizes, atgc)
fit_s = fit_power_law(sizes, shifts)
a_h = fit_h['alpha']

kappa_grid = np.arange(KAPPA0 - 0.7, KAPPA0 + 0.7 + 1e-9, 0.02)
col = collapse_scan(curves, G_C, a_h, kappa_grid)
col2 = collapse_scan_2d(curves, G_C,
                        np.arange(KAPPA0 - 0.6, KAPPA0 + 0.6 + 1e-9, 0.03),
                        np.arange(THEORY_A - 0.8, THEORY_A + 0.6 + 1e-9, 0.03))

pair_h = pairwise_exponents(sizes, heights)
pair_g = pairwise_exponents(sizes, atgc)
pair_s = pairwise_exponents(sizes, shifts)

print(f"\n  (1) at-g_c  : a = {fit_g['alpha']:.4f} +/- {fit_g['alpha_err']:.4f}  "
      f"(target {THEORY_A}; prior ~1.77)  R2={fit_g['r_squared']:.5f}")
print(f"      pairwise at-g_c a: " + " ".join(f"{p['alpha']:.2f}" for p in pair_g))
print(f"  (2) height  : a = {fit_h['alpha']:.4f} +/- {fit_h['alpha_err']:.4f}  "
      f"(target {THEORY_A})  R2={fit_h['r_squared']:.5f}")
print(f"      pairwise height a: " + " ".join(f"{p['alpha']:.2f}" for p in pair_h))
print(f"  (3) shift   : 1/nu = {-fit_s['alpha']:.4f} +/- {fit_s['alpha_err']:.4f}  "
      f"(target {THEORY_INV_NU})  R2={fit_s['r_squared']:.5f}   <- FRAGILE (see q=2/3)")
print(f"      pairwise shift 1/nu: " + " ".join(f"{-p['alpha']:.2f}" for p in pair_s))
print(f"  (4) collapse: 1/nu = {col['kappa_refined']:.4f} (grid-min {col['kappa_best']:.3f}, "
      f"cost {col['cost_min']:.4e})  (target {THEORY_INV_NU})")
print(f"      2D collapse: 1/nu = {col2['kappa_best']:.3f}, a = {col2['a_best']:.3f}  "
      f"(check a=2/nu-d: {2*col2['kappa_best']-1:.3f})")

results['fits'] = {
    'at_gc_exp': fit_g['alpha'], 'at_gc_exp_err': fit_g['alpha_err'], 'at_gc_r2': fit_g['r_squared'],
    'height_exp': a_h, 'height_exp_err': fit_h['alpha_err'], 'height_r2': fit_h['r_squared'],
    'shift_inv_nu': -fit_s['alpha'], 'shift_inv_nu_err': fit_s['alpha_err'], 'shift_r2': fit_s['r_squared'],
    'collapse': col, 'collapse_2d': col2,
    'pairwise_height': [{'n1': p['n1'], 'n2': p['n2'], 'a': p['alpha']} for p in pair_h],
    'pairwise_at_gc': [{'n1': p['n1'], 'n2': p['n2'], 'a': p['alpha']} for p in pair_g],
    'pairwise_shift_inv_nu': [{'n1': p['n1'], 'n2': p['n2'], 'inv_nu': -p['alpha']} for p in pair_s],
}
save()

nmax = int(max(sizes))
record(sprint=130, model='sq', q=Q, n=nmax, quantity='chiF_height_exp', value=float(a_h),
       error=float(fit_h['alpha_err']), method='chi_F_peakheight', notes=f'target 2/nu-d={THEORY_A} finite-size')
record(sprint=130, model='sq', q=Q, n=nmax, quantity='chiF_collapse_inv_nu',
       value=float(col['kappa_refined']), error=col['kappa_err'],
       method='chi_F_data_collapse', notes=f'target 1/nu={THEORY_INV_NU} a_fixed={a_h:.3f}')
record(sprint=130, model='sq', q=Q, n=nmax, quantity='chiF_atgc_exp', value=float(fit_g['alpha']),
       error=float(fit_g['alpha_err']), method='chi_F_at_gc_curve', notes=f'sizes={[int(s) for s in sizes]} prior~1.77')
save()
print(f"\nSaved -> {os.path.relpath(OUT)}")

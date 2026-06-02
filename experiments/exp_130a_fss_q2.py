"""Sprint 130a: q=2 (Ising) chi_F finite-size-scaling cross-check -- CALIBRATION.

Scan the per-site chi_F(g,N) curve on a scaling-variable window and read off
FOUR estimators of the per-site exponent / nu, to see which are trustworthy at
accessible sizes before applying them to q=4:
  (1) at-g_c exponent      chi_F(g_c) ~ N^a      a = 2/nu - d   (= 1.0 for q=2)
  (2) peak-HEIGHT exponent chi_F(g*)  ~ N^a      (g* self-located, no g_c needed)
  (3) peak-SHIFT exponent  |g*-g_c|   ~ N^{-1/nu} (expect 1.0; KNOWN fragile)
  (4) data-collapse 1/nu   (full curve; fix a=a_height, scan kappa)

q=2: nu=1 -> 1/nu=1.0, 2/nu-d = 1.0, g_c=1/2 exact (self-dual). No marginal op.
CPU-only this session. Curves saved for the collapse and for re-analysis.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from collapse_utils import scan_curve, peak_from_curve, chi_at, collapse_scan, collapse_scan_2d
from hamiltonian_utils import build_sq_potts_parts
from fss_utils import fit_power_law, pairwise_exponents
from db_utils import record

Q = 2
G_C = 1.0 / Q
SIZES = [8, 10, 12, 14, 16, 18, 20]
KAPPA0 = 1.0                     # literature 1/nu, sets the scaling window
THEORY_INV_NU = 1.0
THEORY_A = 2.0 / 1.0 - 1.0       # 2/nu - d = 1.0
X_LO, X_HI, M = -4.0, 4.0, 17    # window in scaling variable x=(g-g_c)N^kappa0

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_130a_fss_q2.json')
results = {
    'experiment': '130a_fss_q2', 'sprint': 130, 'q': Q, 'g_c': G_C,
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
print(f"Sprint 130a: q={Q} chi_F FSS calibration (g_c={G_C}, expect 1/nu=1.0, a=1.0)")
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
        xlo, xhi = 2 * xlo, 2 * xhi      # widen once if peak hit a boundary
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

kappa_grid = np.arange(KAPPA0 - 0.6, KAPPA0 + 0.6 + 1e-9, 0.02)
col = collapse_scan(curves, G_C, a_h, kappa_grid)
col2 = collapse_scan_2d(curves, G_C,
                        np.arange(KAPPA0 - 0.5, KAPPA0 + 0.5 + 1e-9, 0.03),
                        np.arange(THEORY_A - 0.6, THEORY_A + 0.8 + 1e-9, 0.03))

pair_h = pairwise_exponents(sizes, heights)
pair_g = pairwise_exponents(sizes, atgc)
pair_s = pairwise_exponents(sizes, shifts)

print(f"\n  (1) at-g_c  : a = {fit_g['alpha']:.4f} +/- {fit_g['alpha_err']:.4f}  "
      f"(theory {THEORY_A})  R2={fit_g['r_squared']:.5f}")
print(f"  (2) height  : a = {fit_h['alpha']:.4f} +/- {fit_h['alpha_err']:.4f}  "
      f"(theory {THEORY_A})  R2={fit_h['r_squared']:.5f}")
print(f"  (3) shift   : 1/nu = {-fit_s['alpha']:.4f} +/- {fit_s['alpha_err']:.4f}  "
      f"(theory {THEORY_INV_NU})  R2={fit_s['r_squared']:.5f}   <- expect FRAGILE")
print(f"      pairwise shift 1/nu: " + " ".join(f"{-p['alpha']:.2f}" for p in pair_s))
print(f"  (4) collapse: 1/nu = {col['kappa_refined']:.4f} (grid-min {col['kappa_best']:.3f}, "
      f"cost {col['cost_min']:.4e})  (theory {THEORY_INV_NU})")
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
       error=float(fit_h['alpha_err']), method='chi_F_peakheight', notes=f'theory 2/nu-d={THEORY_A}')
record(sprint=130, model='sq', q=Q, n=nmax, quantity='chiF_collapse_inv_nu',
       value=float(col['kappa_refined']), error=col['kappa_err'],
       method='chi_F_data_collapse', notes=f'theory 1/nu={THEORY_INV_NU} a_fixed={a_h:.3f}')
record(sprint=130, model='sq', q=Q, n=nmax, quantity='chiF_atgc_exp', value=float(fit_g['alpha']),
       error=float(fit_g['alpha_err']), method='chi_F_at_gc_curve', notes=f'sizes={[int(s) for s in sizes]}')
save()
print(f"\nSaved -> {os.path.relpath(OUT)}")

"""Sprint 137b: Im(g_EP)(L) via Z_q-conserving DMRG, OPEN BC -- the walking-crossover hunt.

Production observable (S136 estimator, DMRG-extended): the charge-0 thermal gap near its
minimum is a 2-level avoided crossing. On OPEN chains the two crossing levels have
DIFFERENT slopes (left/right wings asymmetric -- seen directly in the 137a data), so we fit
    Delta(g) = sqrt(Delta_m^2 + f(g)^2),   f = c1*(g-g*) + c2*(g-g*)^2
    =>  Im(g_EP) = Delta_m / c1   (leading order; c2 absorbs the wing asymmetry).
Fitting the crossing FORM (not parabola-sampling the minimum) sidesteps the exponentially
narrow dip at L >~ xi. Points with Delta > 3x the smallest sampled gap are excluded from
the fit (far wings feel other levels). Equivalent to the S136 parabola at small L
(Delta'' = c1^2/Delta_m at the min => sqrt(Dmin/D'') = Dm/c1 identically).

Prediction (audit-retargeted): xi_d(q=8)=23.9, xi_d(q=10)=10.6 (exact, Buffenoir-Wallon)
=> the local slope of ln Im(g_EP) vs ln L should STEEPEN beyond L ~ xi for q=10 (visible
from n~12) and late/weakly for q=8 (n>~24); the q=6 control (xi=158.9) must stay smooth.

Usage:  python exp_137b_walking_crossover_dmrg.py Q n1 [n2 ...]
Accumulates results/sprint_137b_crossover_q{Q}.json; DB (BC-qualified names, audit rule):
im_gEP_open / thermal_gap_min_open / gstar_thermal_open.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.optimize import curve_fit
from zq_dmrg_utils import thermal_gap_charge0
from db_utils import record

q = int(sys.argv[1])
sizes = [int(x) for x in sys.argv[2:]]
g_c = 1.0 / q
XI = {5: 2512.2, 6: 158.9, 7: 48.1, 8: 23.9, 9: 16.0, 10: 10.56}.get(q)
# generic harness since S137; later sprints set SPRINT_NO so provenance (DB rows + filename)
# is honest -- e.g. the S138 q=7 prediction test writes sprint_138b_crossover_q7.json
SPRINT = int(os.environ.get('SPRINT_NO', 137))
OUT = os.path.join(os.path.dirname(__file__), '..', 'results',
                   f'sprint_{SPRINT}b_crossover_q{q}.json')


def chi_for(n):
    return 64 if n <= 16 else (96 if n <= 24 else 128)


if os.path.exists(OUT):
    with open(OUT) as f:
        results = json.load(f)
    results['sizes'] = {int(k): v for k, v in results['sizes'].items()}
else:
    results = {'experiment': f'{SPRINT}b_crossover_q{q}', 'sprint': SPRINT, 'q': q, 'g_c': g_c,
               'xi_d_exact': XI, 'BC': 'open', 'method': 'zq_dmrg_hyperbola_fit', 'sizes': {}}


def save():
    # merge-on-save: another invocation may have added sizes since we loaded the JSON
    # (a concurrent re-measure chain clobbered q=10 n=28 this way -- read-modify-write
    # race on the accumulate pattern). Disk wins for sizes THIS process didn't measure.
    if os.path.exists(OUT):
        try:
            with open(OUT) as f:
                disk = json.load(f)
            for k, v in disk.get('sizes', {}).items():
                if int(k) not in results['sizes']:
                    results['sizes'][int(k)] = v
        except Exception:
            pass
    results['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2)


def hyper(qq, dm, c1, c2, gs):
    f = c1 * (qq - gs) + c2 * (qq - gs)**2
    return np.sqrt(dm**2 + f**2)


def predict(n):
    """(g*_pred, dm_pred, c1_pred) extrapolated from accumulated sizes."""
    ns = sorted(results['sizes'])
    if len(ns) >= 2:
        arr = np.array([[m, results['sizes'][m]['g_star'], results['sizes'][m]['gap_min'],
                         results['sizes'][m]['c1']] for m in ns[-4:]], float)
        gs = np.polyval(np.polyfit(1.0 / arr[:, 0], arr[:, 1], 1), 1.0 / n)
        dm = float(np.exp(np.polyval(np.polyfit(arr[:, 0], np.log(arr[:, 2]), 1), n)))
        c1 = float(np.polyval(np.polyfit(arr[:, 0], arr[:, 3], 1), n))
        return min(gs, g_c), max(dm, 1e-8), max(c1, 1e-3)
    return 0.85 * g_c, 0.3, 8.0


def measure(n):
    chi = chi_for(n)
    gs_pred, dm_pred, c1_pred = predict(n)
    w = float(np.clip(3.0 * dm_pred / c1_pred, 0.03 * g_c, 0.20 * g_c))
    t0 = time.time()
    pts, p0w, p1w, cu_max, nsolve = {}, None, None, 0, 0
    fast = {'max_sweeps': 20, 'svd_min': 1e-9}

    def gap_at(g):
        nonlocal p0w, p1w, cu_max, nsolve
        if g in pts:
            return pts[g]
        _, _, d, p0w, p1w, cu = thermal_gap_charge0(n, q, g, chi, warm0=p0w, warm1=p1w, **fast)
        cu_max = max(cu_max, cu); nsolve += 2
        pts[g] = d
        return d

    # round 1: 5 points across the predicted dip (ascending g for warm-starting)
    center = gs_pred
    for attempt in range(3):
        grid = np.linspace(center - w, min(center + w, g_c * 1.05), 5)
        for g in grid:
            gap_at(float(g))
        gsort = sorted(pts)
        dvals = np.array([pts[g] for g in gsort])
        i = int(np.argmin(dvals))
        if 0 < i < len(gsort) - 1:
            break
        center = gsort[i]                      # recenter once toward the edge minimum
        w *= 1.6
    else:
        raise RuntimeError(f"q={q} n={n}: dip not bracketed after recentering")

    def fit():
        gg_all = np.array(sorted(pts)); dd_all = np.array([pts[g] for g in gg_all])
        keep = dd_all <= 3.0 * dd_all.min()    # far wings feel other levels -> exclude
        if keep.sum() < 7 and len(gg_all) >= 7:
            keep = dd_all <= 4.0 * dd_all.min()   # widen rather than fit 4 params to ~4 pts
        gg, dd = gg_all[keep], dd_all[keep]
        if len(gg) < 4:
            gg, dd = gg_all, dd_all
        i = int(np.argmin(dd))
        p0 = [max(dd.min() * 0.7, 1e-9), max(c1_pred, 0.5), 0.0, gg[i]]
        popt, pcov = curve_fit(hyper, gg, dd, p0=p0,
                               bounds=([1e-10, 1e-3, -3e3, gg[0] - 0.1],
                                       [dd.min(), 200.0, 3e3, gg[-1] + 0.1]),
                               maxfev=60000)
        resid = dd - hyper(gg, *popt)
        return popt, float(np.sqrt(np.mean(resid**2)) / dd.min()), pcov, int(len(gg))

    popt, relres, pcov, nfit = fit()
    # refinement until: dip bottom sampled (<=1.5x Delta_m), tight fit (relres < 5e-3),
    # AND >=7 kept points -- a 4-param fit through ~5 points is exact-identified, passes
    # any relres gate, yet leaves 5-20% parameter noise (caught on q=10 n=8/10: Dm moved
    # 18% on re-measurement). nfit >= 7 makes the residual a real diagnostic.
    for refine in range(4):
        dm, c1, c2, gs = popt
        if min(pts.values()) <= 1.5 * dm and relres < 5e-3 and nfit >= 7:
            break
        if min(pts.values()) > 1.5 * dm:
            extra = [gs - dm / c1, gs, gs + dm / c1]
        else:
            extra = [gs - 1.5 * dm / c1, gs - 0.5 * dm / c1, gs + 0.5 * dm / c1,
                     gs + 1.5 * dm / c1][:max(3, 7 - nfit)]
        for g in extra:
            gap_at(float(np.clip(g, gs - w, gs + w)))
        popt, relres, pcov, nfit = fit()
    dm, c1, c2, gs = popt
    perr = np.sqrt(np.diag(pcov))
    im = dm / c1
    dt = time.time() - t0
    rec = {'n': n, 'chi_max': chi, 'chi_used': cu_max, 'n_solves': nsolve,
           'g_star': float(gs), 'gap_min': float(dm), 'gap_min_err': float(perr[0]),
           'c1': float(c1), 'c1_err': float(perr[1]), 'c2': float(c2), 'im_gEP': float(im),
           'gapmin_times_L': float(dm * n), 'L_over_xi': (n / XI) if XI else None,
           'fit_rel_resid': relres, 'n_fit_points': nfit,
           'min_sampled_gap': float(min(pts.values())),
           'points': {f"{g:.6f}": pts[g] for g in sorted(pts)}, 'time_s': round(dt, 1)}
    results['sizes'][n] = rec
    print(f" n={n:2d} L/xi={rec['L_over_xi']:.2f}  g*={gs:.5f}  Dm={dm:.6f} (Dm*L={dm*n:.3f})  "
          f"c1={c1:.3f}  Im(g_EP)={im:.6f}  relres={relres:.1e}  "
          f"[{nsolve} solves, chi {cu_max}/{chi}, {dt:.0f}s]", flush=True)
    record(sprint=SPRINT, model='sq_potts', q=q, n=n, quantity='im_gEP_open', value=float(im),
           error=float(im * np.hypot(perr[0] / dm, perr[1] / c1)),
           method='thermal_gap_EP_hyperbola_dmrg_open',
           notes=f'g*={gs:.5f} Dm={dm:.6f} c1={c1:.3f} chi={cu_max} relres={relres:.1e}')
    record(sprint=SPRINT, model='sq_potts', q=q, n=n, quantity='thermal_gap_min_open',
           value=float(dm), error=float(perr[0]), method='hyperbola_fit_dmrg_open',
           notes=f'g*={gs:.5f}; L/xi={rec["L_over_xi"]:.2f}' if XI else None)
    record(sprint=SPRINT, model='sq_potts', q=q, n=n, quantity='gstar_thermal_open',
           value=float(gs), error=None, method='hyperbola_fit_dmrg_open',
           notes='pseudo-critical (charge-0 gap min), open BC')
    save()


print("=" * 78, flush=True)
print(f"Sprint 137b: q={q} (xi_d={XI})  Im(g_EP) via Z_q-DMRG hyperbola fit, sizes={sizes}", flush=True)
print("=" * 78, flush=True)
for n in sizes:
    measure(n)

ns = sorted(results['sizes'])
if len(ns) >= 2:
    print("\n  local slopes  d ln Im / d ln L   (steepening past L~xi = the crossover):", flush=True)
    ims = [results['sizes'][n]['im_gEP'] for n in ns]
    slopes = []
    for k in range(len(ns) - 1):
        s = (np.log(ims[k + 1]) - np.log(ims[k])) / (np.log(ns[k + 1]) - np.log(ns[k]))
        Lmid = np.sqrt(ns[k] * ns[k + 1])
        slopes.append([ns[k], ns[k + 1], float(s), float(Lmid / XI) if XI else None])
        print(f"    ({ns[k]:2d},{ns[k+1]:2d})  L_mid/xi={Lmid/XI:5.2f}  slope={s:+.3f}", flush=True)
    results['local_slopes'] = slopes
    save()
print("\nDONE ->", OUT, flush=True)

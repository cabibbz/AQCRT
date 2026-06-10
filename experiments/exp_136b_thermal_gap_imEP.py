"""Sprint 136b: Im(g_EP)(L) for the transverse-field S_q Potts chain (PERIODIC BC).

Production run of the validated (136a) thermal-gap exceptional-point method:
  - thermal gap Delta_eps(g) = E1c0 - E0c0  (two lowest Z_q-charge-0 states; P=prod X_i filter)
  - find the gap minimum g*(L) (coarse + fine parabola), Delta_min, curvature Delta''
  - Im(g_EP)(L) = sqrt(Delta_min / Delta'')   (2-level avoided-crossing EP; validated 136a)

Prediction:
  continuous (q<=4): Im(g_EP) ~ L^{-1/nu} -> 0   (real fixed point; nu: q2=1, q3=5/6, q4=2/3)
  walking   (q>=5):  Im(g_EP) -> gamma_q > 0       (complex fixed point off the real axis)

Usage:  python exp_136b_thermal_gap_imEP.py Q [n1 n2 ...]
Accumulates results/sprint_136b_imEP_q{Q}.json ; records DB im_gEP / thermal_gap_min / gstar_thermal.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gpu_utils import gpu_status
from ep_utils import (build_parts as _ep_build_parts, charge0_two_lowest,
                      gap_curve as _ep_gap_curve, parab_min, free_gpu as _free_gpu,
                      DENSE_MAX)
from db_utils import record

q = int(sys.argv[1]) if len(sys.argv) > 1 else 2
g_c = 1.0 / q
DEFAULTS = {2: range(6, 17), 3: range(5, 13), 4: range(5, 11),
            5: range(4, 10), 6: range(4, 9), 7: range(4, 8)}
sizes = [int(x) for x in sys.argv[2:]] or list(DEFAULTS.get(q, range(4, 9)))
K = 2 * q + 6                                   # enough lowest states to reach 2nd charge-0
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', f'sprint_136b_imEP_q{q}.json')

# EP math now lives in ep_utils.py (audit 2026-06-09): one implementation shared by
# experiments and the golden gate. These thin wrappers keep this script's call shape.

def build_parts(n):
    return _ep_build_parts(n, q)


def gap_curve(Hc, Hf, P, gs):
    return _ep_gap_curve(Hc, Hf, P, gs, K)


if os.path.exists(OUT):
    with open(OUT) as f:
        results = json.load(f)
    results['sizes'] = {int(k): v for k, v in results.get('sizes', {}).items()}
else:
    results = {'experiment': f'136b_imEP_q{q}', 'sprint': 136, 'q': q, 'g_c': g_c,
               'BC': 'periodic', 'K': K, 'sizes': {}}


def save():
    results['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    results['gpu_status'] = gpu_status()
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2, default=str)


print("=" * 78)
print(f"Sprint 136b: q={q} Im(g_EP)(L), g_c={g_c:.5f}, sizes={sizes}, K={K}")
print(f"  {gpu_status()}")
print("=" * 78)

def plan_window(n):
    """(center, half_width) for the gap-min scan. Wide & safe for the first/small sizes;
    extrapolated & narrow once >=2 prior g* exist (keeps large-dim SPARSE scans out of the
    deep-ordered near-degenerate region that stalls Lanczos). g*(L) sits below g_c -> g_c."""
    gs = sorted((m, results['sizes'][m]['g_star']) for m in results['sizes'])
    if len(gs) >= 2:
        ms = np.array([m for m, _ in gs][-3:], float)
        vs = np.array([v for _, v in gs][-3:], float)
        cen = float(np.polyval(np.polyfit(ms, vs, 2 if len(ms) >= 3 else 1), n))
        cen = min(cen, g_c)
        return cen, max(0.04 * g_c, 2.5 * abs(vs[-1] - vs[-2]))
    return 0.92 * g_c, 0.14 * g_c                 # wide first scan (~0.78..1.06 g_c)


def find_min(Hc, Hf, P, n, dim):
    center, hw = plan_window(n)
    safe = dim <= DENSE_MAX                        # only small/dense scans may recenter
    coarse = cg = None
    for attempt in range(3 if safe else 1):
        lo, hi = center - hw, min(center + hw, g_c + 0.4 * hw)
        coarse = np.linspace(lo, hi, 9)
        cg = gap_curve(Hc, Hf, P, coarse)
        i = int(np.argmin(cg))
        if (0 < i < len(coarse) - 1) or not safe:
            break
        center = coarse[i]; hw *= 1.5
    raw_i = int(np.argmin(cg))
    edge_hit = raw_i in (0, len(coarse) - 1)     # audit: clamping a window-edge argmin
    if edge_hit and not safe:                    # fits a parabola around a NON-minimum;
        raise RuntimeError(                      # fail loudly instead of recording it
            f"n={n}: coarse gap minimum sits at the window edge (i={raw_i}) and the "
            f"sparse path cannot recenter -- widen/move the window before trusting this n")
    i = max(1, min(raw_i, len(coarse) - 2))
    fine = np.linspace(coarse[i - 1], coarse[i + 1], 7)
    fg = gap_curve(Hc, Hf, P, fine)
    raw_j = int(np.argmin(fg))
    if raw_j in (0, len(fine) - 1):
        raise RuntimeError(
            f"n={n}: fine-grid gap minimum sits at the grid edge (j={raw_j}) -- "
            f"parabola vertex would extrapolate; adjust the window")
    j = raw_j
    g_star, gmin, gpp = parab_min(fine[j - 1:j + 2], fg[j - 1:j + 2])
    return g_star, gmin, gpp, coarse, cg, fine, fg


for n in sizes:
    t0 = time.time()
    dim = q ** n
    Hc, Hf, P = build_parts(n)
    g_star, gmin, gpp, coarse, cg, fine, fg = find_min(Hc, Hf, P, n, dim)
    im_est = float(np.sqrt(gmin / gpp)) if gpp > 0 else float('nan')
    rec = {'n': n, 'dim': dim, 'g_star': float(g_star), 'gap_min': float(gmin),
           'gap_curv': float(gpp), 'im_gEP': im_est, 'gapmin_times_L': float(gmin * n),
           'coarse_g': coarse.tolist(), 'coarse_gap': cg.tolist(),
           'fine_g': fine.tolist(), 'fine_gap': fg.tolist(), 'time_s': time.time() - t0}
    results['sizes'][n] = rec
    print(f" n={n:2d} dim={dim:>9,}  g*={g_star:.5f}  Dmin={gmin:.6f}  Dmin*L={gmin*n:.4f}"
          f"  Im(g_EP)={im_est:.6f}  [{rec['time_s']:.1f}s]")
    record(sprint=136, model='sq', q=q, n=n, quantity='im_gEP', value=im_est, error=None,
           method='thermal_gap_EP_realaxis_periodic',
           notes=f'g*={g_star:.5f}, Dmin={gmin:.6f}; Im part of complex fixed-point coupling')
    record(sprint=136, model='sq', q=q, n=n, quantity='thermal_gap_min', value=float(gmin),
           error=None, method='charge0_gap_min_periodic', notes=f'g*={g_star:.5f}')
    record(sprint=136, model='sq', q=q, n=n, quantity='gstar_thermal', value=float(g_star),
           error=None, method='charge0_gap_min_periodic', notes='pseudo-critical (gap min)')
    del Hc, Hf, P; _free_gpu()
    save()

# local log-log slopes (continuous: ~ -1/nu const; walking: drifts toward 0)
ns = sorted(results['sizes'])
if len(ns) >= 2:
    print("\n  pairwise local slope d ln Im(g_EP)/d ln L:")
    ims = [results['sizes'][n]['im_gEP'] for n in ns]
    slopes = []
    for a, b, ia, ib in [(ns[k], ns[k + 1], ims[k], ims[k + 1]) for k in range(len(ns) - 1)]:
        s = (np.log(ib) - np.log(ia)) / (np.log(b) - np.log(a))
        slopes.append([a, b, float(s)])
        print(f"    ({a:2d},{b:2d})  slope={s:+.3f}")
    results['pairwise_slopes'] = slopes
    full = float(np.polyfit(np.log(ns), np.log(ims), 1)[0])
    results['loglog_slope_full'] = full
    nu = {2: 1.0, 3: 5 / 6, 4: 2 / 3}.get(q)
    tgt = f" (continuous target -1/nu = {-1/nu:.3f})" if nu else " (walking: expect drift toward 0)"
    print(f"  full-range slope = {full:+.3f}{tgt}")
    save()
print("\nDONE ->", OUT)

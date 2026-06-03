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
from scipy.sparse import csr_matrix
from scipy.linalg import eigh as dense_eigh
from gpu_utils import eigsh, gpu_status, GPU_ENABLED
from hamiltonian_utils import _decode_states, _build_coupling, _build_field
from db_utils import record

q = int(sys.argv[1]) if len(sys.argv) > 1 else 2
g_c = 1.0 / q
DEFAULTS = {2: range(6, 17), 3: range(5, 13), 4: range(5, 11),
            5: range(4, 10), 6: range(4, 9), 7: range(4, 8)}
sizes = [int(x) for x in sys.argv[2:]] or list(DEFAULTS.get(q, range(4, 9)))
K = 2 * q + 6                                   # enough lowest states to reach 2nd charge-0
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', f'sprint_136b_imEP_q{q}.json')


def _free_gpu():
    try:
        import cupy as cp; cp.get_default_memory_pool().free_all_blocks()
    except Exception:
        pass


def build_parts(n):
    dim, all_idx, digits, powers = _decode_states(n, q)
    H_coup = _build_coupling(all_idx, digits, n, dim)
    H_field = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
    new_idx = (((digits + 1) % q) * powers).sum(axis=1)
    P = csr_matrix((np.ones(dim), (new_idx, all_idx)), shape=(dim, dim))
    return H_coup, H_field, P


DENSE_MAX = 1500                               # dense subset only for the smallest dims
                                                # (dense eigh is O(dim^3); sparse for the rest)


def _lowest(H, dim):
    """K lowest (eval, evec) of real-symmetric H. Dense subset for tiny dim; sparse eigsh
    (which='SA', large ncv+maxiter) above -- converges fine since the scan window is narrow
    and on the disordered side (near g_c, gap~1/L), away from the ordered-side near-degeneracy
    that stalled Lanczos with the old wide window."""
    if dim <= DENSE_MAX:
        evals, evecs = dense_eigh(H.toarray(), subset_by_index=[0, min(K, dim) - 1])
        return evals, evecs
    ncv = min(dim - 1, max(4 * K, 80))
    evals, evecs = eigsh(H, k=K, which='SA', ncv=ncv, maxiter=5000, tol=1e-9)
    order = np.argsort(evals)
    return evals[order], evecs[:, order]


def charge0_gap(Hc, Hf, P, g):
    dim = Hc.shape[0]
    evals, evecs = _lowest(Hc + g * Hf, dim)
    chexp = np.einsum('ij,ij->j', evecs, (P @ evecs))     # <v|P|v>, real
    c0 = np.where(chexp > 0.9)[0]
    _free_gpu()
    if len(c0) < 2:
        raise RuntimeError(f"only {len(c0)} charge-0 states in lowest {K} at g={g:.4f}")
    return evals[c0[0]], evals[c0[1]]


def gap_curve(Hc, Hf, P, gs):
    return np.array([charge0_gap(Hc, Hf, P, g)[1] - charge0_gap(Hc, Hf, P, g)[0] for g in gs])


def parab_min(gs, ys):
    a, b, c = np.polyfit(gs, ys, 2)
    g0 = -b / (2 * a)
    return g0, a * g0**2 + b * g0 + c, 2 * a


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
    i = max(1, min(int(np.argmin(cg)), len(coarse) - 2))
    fine = np.linspace(coarse[i - 1], coarse[i + 1], 7)
    fg = gap_curve(Hc, Hf, P, fine)
    j = max(1, min(int(np.argmin(fg)), len(fine) - 2))
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

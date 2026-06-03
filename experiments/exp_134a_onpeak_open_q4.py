"""Sprint 134a: q=4 S_q Potts per-site chi_F at the FINITE-SIZE PEAK g*(L), OPEN BC, n=4..12.

Falsification test of the S133 non-monotonic open kappa_eff. S133 measured open chi_F at the
PERIODIC critical point g_c=1/q=0.25; but the open chain peaks at g*(L)<g_c (boundary shift),
g*(L)->g_c as L->inf. So the fixed-g_c series samples a MOVING off-peak tail, which can manufacture
a kappa_eff dip. Here we measure chi_F AT the peak g*(L) -- the standard FSS observable
(Albuquerque 0912.2689; Schwandt-Alet-Capponi PRL 2009) -- and ask whether the dip survives.

Canonical estimator (chif_utils convention), but evaluated at the self-located peak instead of g_c:
    chi_F(g) = (2 - |<psi(g)|psi(g+dg)>|^2 - |<psi(g)|psi(g-dg)>|^2)/(dg^2 n),  dg=1e-4.
Peak located by an adaptive scan + parabola vertex; chi_F is then evaluated canonically AT g* (the
peak is flat, so a ~1e-3 error in g* gives O(1e-6) error in the height -> robust).

Usage:  python exp_134a_onpeak_open_q4.py [n1 n2 ...]      (default 4..11; run 12 separately)
Saves results/sprint_134a_onpeak_open_q4.json (ACCUMULATES across runs) and records to DB.
Validation: chi_F(g_c) recomputed here must reproduce results.db chi_F_open_exact (S133) to ~1e-6.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scipy.sparse import csr_matrix
from gpu_utils import eigsh, gpu_status, GPU_ENABLED
from hamiltonian_utils import _decode_states, _build_field
from db_utils import record, query

q = 4
g_c = 1.0 / q
dg = 1e-4
DEFAULT_SIZES = list(range(4, 12))          # 4..11; n=12 run separately
sizes = [int(x) for x in sys.argv[1:]] or DEFAULT_SIZES

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_134a_onpeak_open_q4.json')

# ---- load accumulator (so n=12 run appends to n=4..11) ----
if os.path.exists(OUT):
    with open(OUT) as f:
        results = json.load(f)
    results['peaks'] = {int(k): v for k, v in results.get('peaks', {}).items()}
else:
    results = {'experiment': '134a_onpeak_open_q4', 'sprint': 134, 'q': q, 'g_c': g_c,
               'dg': dg, 'convention': 'canonical central, evaluated AT peak g*(L), OPEN BC',
               'peaks': {}}

def save():
    results['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    results['gpu_status'] = gpu_status()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def _free_gpu():
    try:
        import cupy as cp; cp.get_default_memory_pool().free_all_blocks()
    except Exception:
        pass

# ---- builders: open BC (drop the single wrap bond) ----
def build_parts(n):
    dim, all_idx, digits, powers = _decode_states(n, q)
    diag = np.zeros(dim, dtype=np.float64)
    for site in range(n - 1):                      # OPEN: n-1 bonds, no wrap
        diag -= (digits[:, site] == digits[:, site + 1]).astype(np.float64)
    H_coup = csr_matrix((diag, (all_idx, all_idx)), shape=(dim, dim))
    H_field = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
    return H_coup, H_field

def ground_state(Hc, Hf, g):
    _, v = eigsh(Hc + g * Hf, k=1, which='SA')
    psi = np.ascontiguousarray(v[:, 0])
    _free_gpu()
    return psi

_NSOLVE = [0]
def chi_at(Hc, Hf, g, n):
    """Canonical per-site chi_F at arbitrary g."""
    p0 = ground_state(Hc, Hf, g)
    pp = ground_state(Hc, Hf, g + dg)
    pm = ground_state(Hc, Hf, g - dg)
    _NSOLVE[0] += 3
    if np.dot(p0, pp) < 0: pp = -pp
    if np.dot(p0, pm) < 0: pm = -pm
    return (2.0 - float(np.dot(p0, pp) ** 2) - float(np.dot(p0, pm) ** 2)) / (dg ** 2 * n)

def parab_vertex(gs, cs):
    """Vertex of the quadratic through (gs, cs). gs/cs length >=3."""
    a, b, c = np.polyfit(gs, cs, 2)
    gstar = -b / (2.0 * a)
    return gstar, a * gstar ** 2 + b * gstar + c, a

def plan_scan(n, peaks):
    """Return (center, half_width, fast) for the size-n scan, using smaller-n peaks.
    fast=True for n>=12 (one narrow scan, ~9 evals) since each eval is ~6s at dim 16.78M."""
    ns = sorted(m for m in peaks if m < n)
    if len(ns) == 0:
        return g_c - 0.07, 0.10, False          # wide first scan (peak below g_c)
    if len(ns) == 1:
        return peaks[ns[0]]['g_star'], 0.05, False
    use = ns[-3:]
    gs = np.array([peaks[m]['g_star'] for m in use])
    deg = 2 if len(use) >= 3 else 1             # quadratic catches the decelerating approach
    A = np.polyfit(use, gs, deg)
    cen = float(np.polyval(A, n))
    cen = min(cen, g_c - 0.003)                 # peak stays below g_c
    fast = n >= 12
    return cen, (0.016 if fast else 0.024), fast

def find_peak(Hc, Hf, n, center, half_width, fast=False):
    """Adaptive: coarse scan, recenter-if-edge (once), then fine parabola vertex.

    fast=True (large n): skip the coarse scan -- trust the prediction `center` and do a single
    narrow fine scan. Costs ~9 chi-evals instead of ~18 (n=12 is ~6s/eval). The prediction comes
    from a linear extrap of g*(n-3..n-1), and the peak is flat, so a slightly-off center is fine."""
    if fast:
        fgrid = np.linspace(center - half_width, min(center + half_width, g_c - 0.001), 7)
        fcs = np.array([chi_at(Hc, Hf, g, n) for g in fgrid])
        k = int(np.argmax(fcs)); k = max(1, min(k, 5))
        g_star, chi_vertex, curv = parab_vertex(fgrid[k - 1:k + 2], fcs[k - 1:k + 2])
        chi_star = chi_at(Hc, Hf, g_star, n)
        return {'g_star': float(g_star), 'chi_star': float(chi_star),
                'chi_vertex_interp': float(chi_vertex), 'curvature': float(curv),
                'coarse_grid': fgrid.tolist(), 'coarse_chi': fcs.tolist(),
                'fine_grid': fgrid.tolist(), 'fine_chi': fcs.tolist(),
                'edge_warn': bool(k in (1, 5))}
    npts = 9
    for attempt in range(3):
        lo, hi = center - half_width, min(center + half_width, g_c + 0.005)
        grid = np.linspace(lo, hi, npts)
        cs = np.array([chi_at(Hc, Hf, g, n) for g in grid])
        i = int(np.argmax(cs))
        if 0 < i < npts - 1:
            break
        # peak at edge -> recenter & widen
        center = grid[i]
        half_width *= 1.6
    # fine parabola through the top-3 around the coarse argmax
    j0 = max(1, min(i, npts - 2))
    # fine scan: 7 points within the bracketing interval, parabola vertex of its top-3
    fl, fh = grid[j0 - 1], grid[j0 + 1]
    fgrid = np.linspace(fl, fh, 7)
    fcs = np.array([chi_at(Hc, Hf, g, n) for g in fgrid])
    k = int(np.argmax(fcs)); k = max(1, min(k, 5))
    g_star, chi_vertex, curv = parab_vertex(fgrid[k - 1:k + 2], fcs[k - 1:k + 2])
    # canonical evaluation AT g* (most rigorous height)
    chi_star = chi_at(Hc, Hf, g_star, n)
    return {'g_star': float(g_star), 'chi_star': float(chi_star),
            'chi_vertex_interp': float(chi_vertex), 'curvature': float(curv),
            'coarse_grid': grid.tolist(), 'coarse_chi': cs.tolist(),
            'fine_grid': fgrid.tolist(), 'fine_chi': fcs.tolist()}

# ---- DB fixed-g_c open series (S133) for the off-peak validation ----
db_open_gc = {int(r[4]): float(r[6]) for r in query(quantity='chi_F_open_exact', q=q)}

print("=" * 78)
print(f"Sprint 134a: q={q} OPEN on-peak chi_F, sizes={sizes}")
print(f"  {gpu_status()}")
print("=" * 78)
if not GPU_ENABLED and max(sizes) >= 11:
    print("  *** GPU disabled and n>=11 requested -- abort. ***"); sys.exit(1)

for n in sizes:
    t0 = time.time(); _NSOLVE[0] = 0
    dim = q ** n
    Hc, Hf = build_parts(n)
    center, hw, fast = plan_scan(n, results['peaks'])
    pk = find_peak(Hc, Hf, n, center, hw, fast=fast)
    chi_gc = chi_at(Hc, Hf, g_c, n)            # for off-peak validation vs S133
    ref = db_open_gc.get(n)
    val_tag = ""
    if ref is not None:
        rd = abs(chi_gc - ref) / ref
        val_tag = f" | chi(g_c)={chi_gc:.6f} vs S133 DB {ref:.6f} reldiff={rd:.1e}"
    shift = pk['g_star'] - g_c
    ratio = chi_gc / pk['chi_star']
    rec = {'n': n, 'dim': dim, 'g_star': pk['g_star'], 'shift': shift,
           'chi_peak': pk['chi_star'], 'chi_gc': float(chi_gc),
           'offpeak_ratio_gc_over_peak': float(ratio), 'curvature': pk['curvature'],
           'n_solves': _NSOLVE[0], 'scan': {'coarse_grid': pk['coarse_grid'],
           'coarse_chi': pk['coarse_chi'], 'fine_grid': pk['fine_grid'], 'fine_chi': pk['fine_chi']}}
    results['peaks'][n] = rec
    print(f"\n  n={n:2d} dim={dim:>10,}  g*={pk['g_star']:.5f} (shift {shift:+.5f})"
          f"  chi_peak={pk['chi_star']:.5f}  chi/peak@gc={ratio:.4f}{val_tag}")
    print(f"     [{_NSOLVE[0]} solves, {time.time()-t0:.1f}s]")
    record(sprint=134, model='sq', q=q, n=n, quantity='chi_F_open_peak',
           value=float(pk['chi_star']), error=None,
           method='exact_canonical_at_peak_dg1e-4',
           notes=f'OPEN BC, g*={pk["g_star"]:.5f} (shift {shift:+.5f}); on-peak chi_F')
    record(sprint=134, model='sq', q=q, n=n, quantity='gstar_open',
           value=float(pk['g_star']), error=None, method='parabola_vertex_chiF_peak',
           notes=f'open pseudo-critical peak; shift from g_c={shift:+.5f}')
    del Hc, Hf; _free_gpu()
    save()

# ---- inline summary: on-peak pairwise kappa vs fixed-g_c pairwise kappa ----
def pairwise(d, key):
    ns = sorted(d)
    out = []
    for i in range(len(ns) - 1):
        a, b = ns[i], ns[i + 1]
        ka = (np.log(d[b][key]) - np.log(d[a][key])) / (np.log(b) - np.log(a))
        out.append((a, b, ka))
    return out

pk = results['peaks']
if len(pk) >= 3:
    print("\n" + "=" * 78)
    print("ON-PEAK vs FIXED-g_c pairwise kappa_eff (OPEN BC):")
    print(f"  {'pair':>8} {'kappa_onpeak':>13} {'kappa_fixed_gc':>15}")
    onp = pairwise(pk, 'chi_peak'); fix = pairwise(pk, 'chi_gc')
    for (a, b, ko), (_, _, kf) in zip(onp, fix):
        print(f"  ({a:2d},{b:2d}) {ko:>13.4f} {kf:>15.4f}")
    ko_vals = [k for _, _, k in onp]
    imin = int(np.argmin(ko_vals))
    print(f"\n  on-peak kappa min = {ko_vals[imin]:.4f} at pair index {imin}"
          f"  (interior? {0 < imin < len(ko_vals)-1})")
    print(f"  on-peak kappa monotonic increasing? {all(np.diff(ko_vals) > 0)}")
    print(f"  on-peak kappa monotonic decreasing? {all(np.diff(ko_vals) < 0)}")
    results['summary_pairwise'] = {'onpeak': [[a, b, k] for a, b, k in onp],
                                   'fixed_gc': [[a, b, k] for a, b, k in fix]}
    save()
print("\nDONE -- results/sprint_134a_onpeak_open_q4.json")

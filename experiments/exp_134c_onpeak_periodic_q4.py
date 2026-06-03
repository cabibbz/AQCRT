"""Sprint 134c: q=4 PERIODIC on-peak chi_F control, n=4..11.

exp_134a showed the open-BC kappa_eff *dip* was a fixed-g_c off-peak artifact (open peak is far below
g_c). The periodic series (the cleaner bulk probe, S132) was ALSO measured at fixed g_c=1/q and was
DESCENDING (1.85->1.78). Periodic has no boundary, so its pseudo-critical shift is much smaller -- but
nonzero. Question: does the periodic *descent* survive on-peak, or is part of it off-peak too?

If periodic on-peak kappa_eff also rises (like open on-peak), then BOTH BC, measured at their own peaks,
give a monotonic RISE toward 2.0 -- a clean, consistent finite-size flow (and the S132 'descending away
from 2.0' face-value reading is itself a fixed-g_c artifact). If periodic on-peak still descends, the
periodic descent is intrinsic and the BC genuinely differ.

PERIODIC BC (n wrap bonds). Canonical estimator at the self-located peak. n=11 = 4.19M (GPU).
Validation: chi_F(g_c) recomputed here reproduces results.db chi_F_exact (periodic, S132) to ~1e-6.
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
sizes = [int(x) for x in sys.argv[1:]] or list(range(4, 12))

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_134c_onpeak_periodic_q4.json')
if os.path.exists(OUT):
    with open(OUT) as f:
        results = json.load(f)
    results['peaks'] = {int(k): v for k, v in results.get('peaks', {}).items()}
else:
    results = {'experiment': '134c_onpeak_periodic_q4', 'sprint': 134, 'q': q, 'g_c': g_c,
               'dg': dg, 'convention': 'canonical central at peak g*(L), PERIODIC BC', 'peaks': {}}

def save():
    results['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    results['gpu_status'] = gpu_status()
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def _free_gpu():
    try:
        import cupy as cp; cp.get_default_memory_pool().free_all_blocks()
    except Exception:
        pass

def build_parts(n):
    dim, all_idx, digits, powers = _decode_states(n, q)
    diag = np.zeros(dim, dtype=np.float64)
    for site in range(n):                       # PERIODIC: n bonds (wrap)
        diag -= (digits[:, site] == digits[:, (site + 1) % n]).astype(np.float64)
    Hc = csr_matrix((diag, (all_idx, all_idx)), shape=(dim, dim))
    Hf = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
    return Hc, Hf

def gstate(Hc, Hf, g):
    _, v = eigsh(Hc + g * Hf, k=1, which='SA')
    p = np.ascontiguousarray(v[:, 0]); _free_gpu(); return p

def chi_at(Hc, Hf, g, n):
    p0, pp, pm = gstate(Hc, Hf, g), gstate(Hc, Hf, g + dg), gstate(Hc, Hf, g - dg)
    if np.dot(p0, pp) < 0: pp = -pp
    if np.dot(p0, pm) < 0: pm = -pm
    return (2.0 - float(np.dot(p0, pp) ** 2) - float(np.dot(p0, pm) ** 2)) / (dg ** 2 * n)

def parab(gs, cs):
    a, b, c = np.polyfit(gs, cs, 2); gv = -b / (2 * a)
    return gv, a * gv ** 2 + b * gv + c

def find_peak(Hc, Hf, n, center, hw):
    # periodic peak is NEAR g_c (small shift) and can lie just below OR above; scan symmetric.
    npts = 9
    for _ in range(4):
        grid = np.linspace(center - hw, center + hw, npts)
        cs = np.array([chi_at(Hc, Hf, g, n) for g in grid])
        i = int(np.argmax(cs))
        if 0 < i < npts - 1:
            break
        center = grid[i]; hw *= 1.7
    j = max(1, min(i, npts - 2))
    fg = np.linspace(grid[j - 1], grid[j + 1], 7)
    fc = np.array([chi_at(Hc, Hf, g, n) for g in fg])
    k = max(1, min(int(np.argmax(fc)), 5))
    gstar, _ = parab(fg[k - 1:k + 2], fc[k - 1:k + 2])
    return float(gstar), float(chi_at(Hc, Hf, gstar, n))

db_per_gc = {int(r[4]): float(r[6]) for r in query(quantity='chi_F_exact', model='sq', q=q)}

print("=" * 78)
print(f"Sprint 134c: q={q} PERIODIC on-peak chi_F, sizes={sizes}")
print(f"  {gpu_status()}")
print("=" * 78)

for n in sizes:
    t0 = time.time()
    Hc, Hf = build_parts(n)
    ms = sorted(m for m in results['peaks'] if m < n)
    if len(ms) < 2:
        center, hw = g_c, 0.04          # periodic peak is close to g_c
    else:
        use = ms[-3:]; A = np.polyfit(use, [results['peaks'][m]['g_star'] for m in use], min(2, len(use) - 1))
        center, hw = float(np.polyval(A, n)), 0.02
    gstar, chistar = find_peak(Hc, Hf, n, center, hw)
    chi_gc = chi_at(Hc, Hf, g_c, n)
    ref = db_per_gc.get(n)
    vt = ""
    if ref is not None:
        vt = f" | chi(g_c)={chi_gc:.6f} vs DB {ref:.6f} reldiff={abs(chi_gc-ref)/ref:.1e}"
    results['peaks'][n] = {'n': n, 'dim': q ** n, 'g_star': gstar, 'shift': gstar - g_c,
                           'chi_peak': chistar, 'chi_gc': float(chi_gc),
                           'offpeak_ratio': float(chi_gc / chistar)}
    print(f"  n={n:2d} dim={q**n:>10,}  g*={gstar:.5f} (shift {gstar-g_c:+.5f})  "
          f"chi_peak={chistar:.5f}  chi/peak@gc={chi_gc/chistar:.4f}{vt}  [{time.time()-t0:.1f}s]")
    record(sprint=134, model='sq', q=q, n=n, quantity='chi_F_periodic_peak',
           value=float(chistar), method='exact_canonical_at_peak_dg1e-4',
           notes=f'PERIODIC BC, g*={gstar:.5f} (shift {gstar-g_c:+.5f})')
    del Hc, Hf; _free_gpu()
    save()

pk = results['peaks']
if len(pk) >= 3:
    ns = sorted(pk)
    def pw(key):
        return [(ns[i], ns[i+1], (np.log(pk[ns[i+1]][key]) - np.log(pk[ns[i]][key])) /
                 (np.log(ns[i+1]) - np.log(ns[i]))) for i in range(len(ns) - 1)]
    onp, fix = pw('chi_peak'), pw('chi_gc')
    print("\nPERIODIC on-peak vs fixed-g_c pairwise kappa_eff:")
    print(f"  {'pair':>8} {'kappa_onpeak':>13} {'kappa_fixed_gc':>15}")
    for (a, b, ko), (_, _, kf) in zip(onp, fix):
        print(f"  ({a:2d},{b:2d}) {ko:>13.4f} {kf:>15.4f}")
    kv = [k for _, _, k in onp]
    print(f"\n  periodic on-peak kappa monotonic increasing? {all(np.diff(kv) > 0)}")
    print(f"  periodic on-peak kappa monotonic decreasing? {all(np.diff(kv) < 0)}")
    results['summary_pairwise'] = {'onpeak': [[a, b, k] for a, b, k in onp],
                                   'fixed_gc': [[a, b, k] for a, b, k in fix]}
    save()
print("\nDONE -- results/sprint_134c_onpeak_periodic_q4.json")

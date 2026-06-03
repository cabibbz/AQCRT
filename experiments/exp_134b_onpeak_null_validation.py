"""Sprint 134b: validate the on-peak chi_F method against the EXACT nulls at q=2 and q=3.

exp_134a introduces a new observable: per-site chi_F at the self-located finite-size PEAK g*(L),
OPEN BC. Before interpreting the q=4 on-peak flow, prove the observable recovers the known leading
exponents where they are exactly known (no marginal operator):
    q=2 (nu=1)   -> 2/nu-d = 1.0
    q=3 (nu=5/6) -> 2/nu-d = 1.4
This is the on-peak analog of test_golden.py (which validates the FIXED-g_c convention). If on-peak
kappa_eff(L) climbs cleanly toward 1.0 / 1.4 for q=2 / q=3, the method is trustworthy and the q=4
on-peak rise toward 2.0 is the analogous (log-slowed) behavior.

OPEN BC throughout (matches exp_134a). Canonical estimator at the peak. Cheap (q=2,3 dims small).
Saves results/sprint_134b_onpeak_null_validation.json + records on-peak kappa to DB.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scipy.sparse import csr_matrix
from gpu_utils import eigsh
from hamiltonian_utils import _decode_states, _build_field
from chif_utils import expected_persite_exponent
from db_utils import record

dg = 1e-4
CASES = {2: list(range(6, 17, 2)),          # q=2: n=6,8,..,16  (2^16=65536)
         3: [4, 5, 6, 7, 8, 9, 10, 11, 12]} # q=3: n=4..12      (3^12=531441)

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_134b_onpeak_null_validation.json')
results = {'experiment': '134b_onpeak_null_validation', 'sprint': 134, 'dg': dg,
           'convention': 'canonical central at peak g*(L), OPEN BC', 'cases': {}}

def save():
    results['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def _free_gpu():
    try:
        import cupy as cp; cp.get_default_memory_pool().free_all_blocks()
    except Exception:
        pass

def build_parts(n, q):
    dim, all_idx, digits, powers = _decode_states(n, q)
    diag = np.zeros(dim, dtype=np.float64)
    for site in range(n - 1):                 # OPEN BC
        diag -= (digits[:, site] == digits[:, site + 1]).astype(np.float64)
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

def find_peak(Hc, Hf, n, q, center, hw):
    npts = 9
    for _ in range(4):
        lo, hi = center - hw, min(center + hw, (1.0 / q) + 0.01)
        grid = np.linspace(lo, hi, npts)
        cs = np.array([chi_at(Hc, Hf, g, n) for g in grid])
        i = int(np.argmax(cs))
        if 0 < i < npts - 1:
            break
        center = grid[i]; hw *= 1.7
    j = max(1, min(i, npts - 2))
    fl, fh = grid[j - 1], grid[j + 1]
    fg = np.linspace(fl, fh, 7)
    fc = np.array([chi_at(Hc, Hf, g, n) for g in fg])
    k = max(1, min(int(np.argmax(fc)), 5))
    gstar, _ = parab(fg[k - 1:k + 2], fc[k - 1:k + 2])
    return float(gstar), float(chi_at(Hc, Hf, gstar, n))

print("=" * 78)
print("Sprint 134b: on-peak chi_F NULL validation (open BC), q=2 -> 1.0, q=3 -> 1.4")
print("=" * 78)

for q, sizes in CASES.items():
    gc = 1.0 / q
    null = expected_persite_exponent(q)
    peaks = {}
    print(f"\n--- q={q}  (null 2/nu-d = {null}) ---")
    for n in sizes:
        t0 = time.time()
        Hc, Hf = build_parts(n, q)
        # plan: first wide below g_c, then quad-extrapolate
        ms = sorted(peaks)
        if len(ms) < 2:
            center, hw = gc - 0.07, 0.10
        else:
            use = ms[-3:]; A = np.polyfit(use, [peaks[m]['g_star'] for m in use], min(2, len(use) - 1))
            center, hw = min(float(np.polyval(A, n)), gc - 0.003), 0.03
        gstar, chistar = find_peak(Hc, Hf, n, q, center, hw)
        peaks[n] = {'n': n, 'g_star': gstar, 'shift': gstar - gc, 'chi_peak': chistar}
        print(f"  n={n:2d} dim={q**n:>9,}  g*={gstar:.5f} (shift {gstar-gc:+.5f})  chi_peak={chistar:.5f}  [{time.time()-t0:.1f}s]")
        del Hc, Hf; _free_gpu()
    # pairwise on-peak kappa
    ns = sorted(peaks)
    kap = [( ns[i], ns[i+1],
             (np.log(peaks[ns[i+1]]['chi_peak']) - np.log(peaks[ns[i]]['chi_peak'])) /
             (np.log(ns[i+1]) - np.log(ns[i])) ) for i in range(len(ns) - 1)]
    print(f"  on-peak pairwise kappa_eff (-> null {null}):")
    for a, b, kk in kap:
        print(f"    ({a:2d},{b:2d}) = {kk:.4f}")
    kvals = [k for _, _, k in kap]
    print(f"  largest-n on-peak kappa = {kvals[-1]:.4f}   |kappa-null| = {abs(kvals[-1]-null):.4f}")
    print(f"  monotonic increasing toward null? {all(np.diff(kvals) > -1e-6)}")
    results['cases'][q] = {'null': null, 'peaks': peaks,
                           'pairwise_kappa': [[a, b, k] for a, b, k in kap],
                           'largest_n_kappa': kvals[-1], 'monotone_inc': bool(all(np.diff(kvals) > -1e-6))}
    record(sprint=134, model='sq', q=q, n=ns[-1], quantity='kappa_open_peak',
           value=float(kvals[-1]), error=None, method='onpeak_pairwise_largest_n',
           notes=f'on-peak open chi_F effective exp; null 2/nu-d={null}')
    save()

print("\n" + "=" * 78)
print("VALIDATION SUMMARY (on-peak open chi_F effective exponent vs exact null):")
for q in CASES:
    c = results['cases'][q]
    ok = abs(c['largest_n_kappa'] - c['null']) < 0.20
    print(f"  q={q}: largest-n kappa={c['largest_n_kappa']:.4f}  null={c['null']}  "
          f"{'OK (<0.20)' if ok else 'OFF'}  monotone_inc={c['monotone_inc']}")
print("=" * 78)
save()
print("\nDONE -- results/sprint_134b_onpeak_null_validation.json")

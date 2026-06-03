"""Sprint 134e: PERIODIC on-peak validation -- the linchpin for the strong claim.

exp_134c found: for q=4 PERIODIC, on-peak kappa_eff ASCENDS (1.68->1.76) while fixed-g_c DESCENDS
(1.86->1.78). If real, this means the S132 'wrong-sign descent away from 2.0' is largely a fixed-g_c
off-peak-penalty artifact and the genuine (peak-height) bulk effective exponent ASCENDS toward 2.0.

That claim only holds if the on-peak peak-height is a VALID estimator of 2/nu-d. Test it where the
answer is exact and there is NO marginal operator (fast convergence):
    q=2 (null 1.0), q=3 (null 1.4), PERIODIC BC.
Decisive signature to confirm: on-peak kappa ASCENDS to the null FROM BELOW while fixed-g_c kappa
DESCENDS to the SAME null FROM ABOVE -- both converging to the exact 2/nu-d. If we see that for
q=2 and q=3, the identical q=4 pattern (on-peak ascends, fixed descends) is the universal finite-size
flow and the common destination is the null = 2.0.

PERIODIC BC. Canonical estimator at peak. q=2,3 dims small. Reports BOTH on-peak and fixed-g_c kappa.
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
CASES = {2: list(range(6, 17, 2)), 3: [4, 5, 6, 7, 8, 9, 10, 11, 12]}
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_134e_onpeak_periodic_validation.json')
results = {'experiment': '134e_onpeak_periodic_validation', 'sprint': 134, 'dg': dg,
           'convention': 'canonical central at peak g*(L), PERIODIC BC', 'cases': {}}

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
    for site in range(n):                          # PERIODIC
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

def find_peak(Hc, Hf, n, q, center, hw):
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

def pw(ns, vals):
    return [(ns[i], ns[i+1], (np.log(vals[i+1]) - np.log(vals[i])) / (np.log(ns[i+1]) - np.log(ns[i])))
            for i in range(len(ns) - 1)]

print("=" * 80)
print("Sprint 134e: PERIODIC on-peak validation -- does on-peak ASCEND to null while fixed DESCENDS?")
print("=" * 80)
for q, sizes in CASES.items():
    gc = 1.0 / q; null = expected_persite_exponent(q)
    rows = {}
    print(f"\n--- q={q}  PERIODIC  (null 2/nu-d = {null}) ---")
    for n in sizes:
        t0 = time.time()
        Hc, Hf = build_parts(n, q)
        ms = sorted(rows)
        if len(ms) < 2:
            center, hw = gc, 0.04
        else:
            use = ms[-3:]; A = np.polyfit(use, [rows[m]['g_star'] for m in use], min(2, len(use)-1))
            center, hw = float(np.polyval(A, n)), 0.02
        gstar, chistar = find_peak(Hc, Hf, n, q, center, hw)
        chigc = chi_at(Hc, Hf, gc, n)
        rows[n] = {'n': n, 'g_star': gstar, 'shift': gstar - gc, 'chi_peak': chistar, 'chi_gc': chigc}
        print(f"  n={n:2d} dim={q**n:>9,}  g*={gstar:.5f} (shift {gstar-gc:+.5f})  "
              f"chi_peak={chistar:.4f} chi_gc={chigc:.4f}  [{time.time()-t0:.1f}s]")
        del Hc, Hf; _free_gpu()
    ns = sorted(rows)
    kon = pw(ns, [rows[n]['chi_peak'] for n in ns])
    kfx = pw(ns, [rows[n]['chi_gc'] for n in ns])
    print(f"  {'pair':>8} {'kappa_onpeak':>13} {'kappa_fixed_gc':>15}   (null {null})")
    for (a, b, ko), (_, _, kf) in zip(kon, kfx):
        print(f"  ({a:2d},{b:2d}) {ko:>13.4f} {kf:>15.4f}")
    kov = [k for _, _, k in kon]; kfv = [k for _, _, k in kfx]
    on_asc = all(np.diff(kov) > -1e-6); fx_desc = all(np.diff(kfv) < 1e-6)
    print(f"  on-peak ASCENDS from below? {on_asc} (last {kov[-1]:.4f} vs null {null}); "
          f"fixed-g_c DESCENDS from above? {fx_desc} (last {kfv[-1]:.4f})")
    print(f"  both bracket the null? on-peak<null<fixed: {kov[-1] <= null + 0.05 and kfv[-1] >= null - 0.05}")
    results['cases'][q] = {'null': null, 'sizes': ns,
                           'kappa_onpeak': [[a, b, k] for a, b, k in kon],
                           'kappa_fixed_gc': [[a, b, k] for a, b, k in kfx],
                           'onpeak_ascends': bool(on_asc), 'fixed_descends': bool(fx_desc),
                           'onpeak_last': kov[-1], 'fixed_last': kfv[-1],
                           'g_star': {n: rows[n]['g_star'] for n in ns}}
    record(sprint=134, model='sq', q=q, n=ns[-1], quantity='kappa_periodic_peak',
           value=float(kov[-1]), method='onpeak_pairwise_largest_n',
           notes=f'periodic on-peak chi_F eff exp; null={null}; ascends={on_asc}')
    save()
print("\n" + "=" * 80)
print("VALIDATION: if on-peak ascends-from-below AND fixed descends-from-above to the SAME exact null")
print("for q=2,3 (no marginal op), the q=4 pattern (on-peak ascends to ~2.0, fixed descends to ~1.78)")
print("is the universal finite-size flow with common destination 2/nu-d.")
for q in CASES:
    c = results['cases'][q]
    print(f"  q={q}: on-peak->{c['onpeak_last']:.3f} (asc {c['onpeak_ascends']}) | "
          f"fixed->{c['fixed_last']:.3f} (desc {c['fixed_descends']}) | null {c['null']}")
print("=" * 80)
save()
print("\nDONE -- results/sprint_134e_onpeak_periodic_validation.json")

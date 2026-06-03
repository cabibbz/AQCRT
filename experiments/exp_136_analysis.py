"""Sprint 136 analysis: complex-fixed-point imaginary coupling Im(g_EP)(L) across q.

Reads results/sprint_136b_imEP_q{q}.json for available q and:
  - pure-power fit Im(g_EP) = A * L^{-p}  (continuous: p -> 1/nu)
  - local log-log slopes (continuous: const at -1/nu; walking: magnitude shrinks -> saturation)
  - saturating fit Im(g_EP) = gamma + A * L^{-p}  (gamma = thermodynamic Im of the complex
    fixed-point coupling; ~0 for continuous q<=4, >0 for walking q>=5 IF saturation is reached)
  - thermal-gap amplitude Dmin*L (continuous: -> 2*pi*v*x_eps const; walking: turns up ~L)

Saves results/sprint_136_analysis.json ; records DB imEP_exponent / imEP_gamma.
"""
import numpy as np
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from db_utils import record
try:
    from scipy.optimize import curve_fit
except Exception:
    curve_fit = None

RES = os.path.join(os.path.dirname(__file__), '..', 'results')
OUT = os.path.join(RES, 'sprint_136_analysis.json')
NU_EXACT = {2: 1.0, 3: 5.0 / 6.0, 4: 2.0 / 3.0}        # continuous Potts
X_EPS = {2: 1.0, 3: 0.8, 4: 0.5}                        # = 2 - 1/nu


def load(q):
    p = os.path.join(RES, f'sprint_136b_imEP_q{q}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    s = d['sizes']
    ns = sorted(int(k) for k in s)
    return {'n': np.array(ns, float),
            'im': np.array([s[str(k)]['im_gEP'] for k in ns]),
            'dmin': np.array([s[str(k)]['gap_min'] for k in ns]),
            'dminL': np.array([s[str(k)]['gapmin_times_L'] for k in ns]),
            'gstar': np.array([s[str(k)]['g_star'] for k in ns])}


def powerfit(n, y):
    p = np.polyfit(np.log(n), np.log(y), 1)
    pred = np.polyval(p, np.log(n))
    ss = 1 - np.sum((np.log(y) - pred)**2) / np.sum((np.log(y) - np.log(y).mean())**2)
    return -p[0], float(ss)                              # exponent magnitude p, R^2


def satfit(n, y):
    if curve_fit is None or len(n) < 5:
        return None
    try:
        popt, pcov = curve_fit(lambda L, g, A, p: g + A * L**(-p), n, y,
                               p0=[0.0, y[0] * n[0], 1.0],
                               bounds=([0, 0, 0.1], [max(y), 1e3, 6]), maxfev=20000)
        perr = np.sqrt(np.diag(pcov))
        return {'gamma': float(popt[0]), 'gamma_err': float(perr[0]),
                'A': float(popt[1]), 'p': float(popt[2]), 'p_err': float(perr[2])}
    except Exception as e:
        return {'error': str(e)}


out = {'experiment': '136_analysis', 'sprint': 136, 'per_q': {}}
print("=" * 90)
print("Sprint 136: Im(g_EP)(L) -- complex-fixed-point imaginary coupling across q  (PERIODIC)")
print("=" * 90)

for q in [2, 3, 4, 5, 6, 7]:
    d = load(q)
    if d is None:
        continue
    n, im = d['n'], d['im']
    p, r2 = powerfit(n, im)
    sat = satfit(n, im)
    locs = [(int(n[i]), int(n[i + 1]),
             float((np.log(im[i + 1]) - np.log(im[i])) / (np.log(n[i + 1]) - np.log(n[i]))))
            for i in range(len(n) - 1)]
    rec = {'n': n.tolist(), 'im_gEP': im.tolist(), 'dminL': d['dminL'].tolist(),
           'gstar': d['gstar'].tolist(), 'power_p': p, 'power_R2': r2,
           'local_slopes': locs, 'sat_fit': sat,
           'nu_exact': NU_EXACT.get(q), 'inv_nu_exact': (1 / NU_EXACT[q]) if q in NU_EXACT else None}
    out['per_q'][q] = rec

    print(f"\n--- q={q}  (g_c={1/q:.4f}) ---")
    print(f"  n:        {[int(x) for x in n]}")
    print(f"  Im(g_EP): {[round(x,5) for x in im]}")
    print(f"  Dmin*L:   {[round(x,3) for x in d['dminL']]}  "
          f"({'->2pi*v*x_eps const (CFT)' if q<=4 else 'walking: should turn UP ~L'})")
    print(f"  local slopes: {[round(s[2],3) for s in locs]}")
    if q in NU_EXACT:
        print(f"  power fit p = {p:.3f} (R2={r2:.4f})   vs exact 1/nu = {1/NU_EXACT[q]:.3f}"
              f"   [{'q=4: marginal log biases p below 1.5' if q==4 else 'continuous'}]")
    else:
        print(f"  power fit p = {p:.3f} (R2={r2:.4f})   [walking: no exact nu; "
              f"local-slope shrink / gamma>0 = complex fixed point off real axis]")
    if sat and 'gamma' in sat:
        sig = sat['gamma'] / sat['gamma_err'] if sat['gamma_err'] > 0 else float('inf')
        print(f"  saturating fit: gamma={sat['gamma']:.5f} +/- {sat['gamma_err']:.5f} "
              f"({sig:.1f} sigma >0), p={sat['p']:.3f}")
    record(sprint=136, model='sq', q=q, n=int(n[-1]), quantity='imEP_exponent',
           value=float(p), error=None, method='powerfit_im_gEP_vs_L',
           notes=f'R2={r2:.4f}; continuous->1/nu' if q <= 4 else 'walking effective')
    if sat and 'gamma' in sat:
        record(sprint=136, model='sq', q=q, n=int(n[-1]), quantity='imEP_gamma',
               value=float(sat['gamma']), error=float(sat['gamma_err']),
               method='satfit_gamma_A_Lp', notes='Im of complex fixed-point coupling (0 if continuous)')

# verdict
print("\n" + "=" * 90)
print("CONTRAST (continuous q<=4 vs walking q>=5):")
print(f"  {'q':>2} {'power p':>8} {'1/nu_exact':>11} {'last local slope':>17} {'gamma':>10}")
for q in sorted(out['per_q']):
    r = out['per_q'][q]
    inv = f"{r['inv_nu_exact']:.3f}" if r['inv_nu_exact'] else "  --"
    g = (f"{r['sat_fit']['gamma']:.4f}" if r['sat_fit'] and 'gamma' in r['sat_fit'] else "--")
    print(f"  {q:>2} {r['power_p']:>8.3f} {inv:>11} {r['local_slopes'][-1][2]:>17.3f} {g:>10}")
print("=" * 90)

with open(OUT, 'w') as f:
    json.dump(out, f, indent=2, default=str)
print("DONE ->", OUT)

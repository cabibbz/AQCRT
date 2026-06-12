"""Sprint 141a: the q=8 universality verdict -- does sigma(q)*xi_d_cl(q) = 1/4 recur?

Registered predictions (sprints/sprint_141.md, BEFORE the data):
  P1: sigma_loc * xi_d_cl flattens at 0.25 +/- 0.04 by L/xi ~ 2 (mirroring q=10).
  P2: tail fit (n >= 36, L/xi >= 1.5): s consistent with 1/4; s==1/4 AIC-competitive;
      s==0.40 (frozen onset) and s==0.50 (classical duality) disfavored.

Data: sprint_141b_crossover_q8.json (S137 n=8..28 + S141 n=36..48), xi_d_cl = 23.9;
matched-L/xi overlay against q=10 (sprint_139b_crossover_q10.json, xi = 10.56).

Usage:  python exp_141a_q8_universality.py
Saves results/sprint_141_analysis.json; DB: sigma_xi_product (q=8).
"""
import numpy as np
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
from scipy.optimize import least_squares
from db_utils import record

RES = os.path.join(os.path.dirname(__file__), '..', 'results')
XI8, XI10 = 23.9, 10.56


def load(path, xi):
    d = json.load(open(os.path.join(RES, path)))
    s = {int(k): v for k, v in d['sizes'].items()}
    ns = np.array(sorted(s), float)
    dm = np.array([s[int(n)]['gap_min'] for n in ns])
    sig = np.array([max(max((s[int(n)].get('fit_rel_resid') or 2e-3), 2e-3),
                        8e-3 if ((s[int(n)].get('n_fit_points') or 9) < 7) else 0)
                    for n in ns])
    return ns, dm, sig, xi


def sigloc(ns, dm, xi):
    lnR = np.log(dm * ns)
    return [[float(ns[i]), float(ns[i + 1]),
             float(np.sqrt(ns[i] * ns[i + 1]) / xi),
             float(-(lnR[i + 1] - lnR[i]) / (ns[i + 1] - ns[i]) * xi)]
            for i in range(len(ns) - 1)]


def tail_fit(ns, dm, sig, xi, n_min, s_fix=None):
    keep = ns >= n_min
    nt, dt, st = ns[keep], dm[keep], sig[keep]
    def res(th):
        s = th[2] if s_fix is None else s_fix
        return (np.log(dt) - (th[0] - th[1] * np.log(nt) - (s / xi) * nt)) / st
    th0 = [np.log(dt[0]) + np.log(nt[0]), 1.0] + ([0.3] if s_fix is None else [])
    r = least_squares(res, th0, method='lm', max_nfev=20000)
    ss = float(np.sum(r.fun**2)); npar = len(th0); m = len(nt)
    serr = None
    if s_fix is None:
        try:
            cov = np.linalg.inv(r.jac.T @ r.jac) * ss / max(m - npar, 1)
            serr = float(np.sqrt(cov[2, 2]))
        except Exception:
            pass
    return {'s': float(r.x[2]) if s_fix is None else float(s_fix), 's_err': serr,
            'a': float(r.x[1]), 'n_pts': int(m),
            'aic': float(m * np.log(ss / m) + 2 * npar)}


ns8, dm8, sg8, _ = load('sprint_141b_crossover_q8.json', XI8)
ns10, dm10, sg10, _ = load('sprint_139b_crossover_q10.json', XI10)

out = {'experiment': '141a_q8_universality', 'sprint': 141, 'xi8': XI8,
       'prediction': 'P1 plateau 0.25+/-0.04 by L/xi~2; P2 tail s ~ 1/4'}
print("=" * 88)
print("Sprint 141a: q=8 universality verdict (registered: plateau 0.25±0.04 by L/xi≈2)")
print("=" * 88)

loc8 = sigloc(ns8, dm8, XI8)
loc10 = sigloc(ns10, dm10, XI10)
out['q8_sigloc'] = loc8
out['q10_sigloc_ref'] = loc10
print("\n[P1] sigma_loc * xi_d_cl  (q=8 vs the q=10 reference at matched L/xi):")
print(f"  {'q=8 window':>12} {'L_mid/xi':>9} {'s_loc*xi':>9}     {'q=10 window':>12} {'L_mid/xi':>9} {'s_loc*xi':>9}")
for i in range(max(len(loc8), len(loc10))):
    l8 = loc8[i] if i < len(loc8) else None
    l10 = loc10[i] if i < len(loc10) else None
    a = f"  ({int(l8[0]):2d},{int(l8[1]):2d})    {l8[2]:9.2f} {l8[3]:+9.3f}" if l8 else " " * 36
    b = f"     ({int(l10[0]):2d},{int(l10[1]):2d})    {l10[2]:9.2f} {l10[3]:+9.3f}" if l10 else ""
    print(a + b)

print("\n[P2] q=8 tail fits (n >= 36, L/xi >= 1.5):")
tf = tail_fit(ns8, dm8, sg8, XI8, 36, None)
out['q8_tail_free'] = tf
print(f"  s FREE     : s = {tf['s']:.3f}" + (f" +/- {tf['s_err']:.3f}" if tf['s_err'] else "")
      + f"   a = {tf['a']:.2f}   ({tf['n_pts']} pts)   AIC = {tf['aic']:.1f}")
for lab, sv in [('1/4 (LAW)', 0.25), ('0.40 (onset frozen)', 0.40), ('0.50 (classical duality)', 0.50)]:
    t = tail_fit(ns8, dm8, sg8, XI8, 36, sv)
    out[f'q8_tail_s_{sv}'] = t
    print(f"  s == {sv:.2f} [{lab:24s}]: dAIC vs free = {t['aic']-tf['aic']:+6.1f}")

# joint q=8+q=10 tails: shared s
def joint(s_fix=None):
    k8, k10 = ns8 >= 36, ns10 >= 16
    def res(th):
        s = th[4] if s_fix is None else s_fix
        r8 = (np.log(dm8[k8]) - (th[0] - th[1] * np.log(ns8[k8]) - (s / XI8) * ns8[k8])) / sg8[k8]
        r10 = (np.log(dm10[k10]) - (th[2] - th[3] * np.log(ns10[k10]) - (s / XI10) * ns10[k10])) / sg10[k10]
        return np.concatenate([r8, r10])
    th0 = [0, 1, 0, 1] + ([0.25] if s_fix is None else [])
    r = least_squares(res, th0, method='lm', max_nfev=20000)
    m = int(np.sum(ns8 >= 36) + np.sum(ns10 >= 16)); npar = len(th0)
    ss = float(np.sum(r.fun**2))
    serr = None
    if s_fix is None:
        try:
            cov = np.linalg.inv(r.jac.T @ r.jac) * ss / max(m - npar, 1)
            serr = float(np.sqrt(cov[4, 4]))
        except Exception:
            pass
    return {'s': float(r.x[4]) if s_fix is None else float(s_fix), 's_err': serr,
            'aic': float(m * np.log(ss / m) + 2 * npar), 'n_pts': m}


jf = joint(None); jq = joint(0.25)
out['joint_tail_free'] = jf; out['joint_tail_quarter'] = jq
print(f"\n[joint q=8 (n>=36) + q=10 (n>=16) tails, SHARED s]:")
print(f"  s = {jf['s']:.3f}" + (f" +/- {jf['s_err']:.3f}" if jf['s_err'] else "")
      + f"   ({jf['n_pts']} pts)   |   s==1/4: dAIC vs free = {jq['aic']-jf['aic']:+.1f}")

out['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
with open(os.path.join(RES, 'sprint_141_analysis.json'), 'w') as f:
    json.dump(out, f, indent=2)
record(sprint=141, model='sq_potts', q=8, n=int(ns8[-1]), quantity='sigma_xi_product',
       value=tf['s'], error=tf['s_err'], method='tail_fit_dmrg_open_nmin36',
       notes=f"registered prediction 0.25+/-0.04; q=10 ref 0.213+/-0.035; "
             f"dAIC(s=1/4 vs free)={out['q8_tail_s_0.25']['aic']-tf['aic']:+.1f}")
print("\nDONE -> results/sprint_141_analysis.json")

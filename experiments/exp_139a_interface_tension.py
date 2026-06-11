"""Sprint 139a: interface-tension test -- is the walking-crossover decay rate the EXACT
2D Potts order-disorder interface tension sigma_od = 1/(2 xi_d)?

JOINT fit across q = 6, 7, 8, 10 (xi_d = 158.9, 48.1, 23.9, 10.56 -- a 15x lever):
    ln Dm_q(L) = ln A_q - a ln L - (s / xi_q) L      (shared a, s; per-q amplitude)
Variants: V1 s free | V2 s = 1/2 FIXED (H_dual) | V3 s = 0 (pure shadow) |
          V4 per-q a_q (degeneracy robustness check).
Plus per-q individual fits s_q, and the q=10 local decay-rate trajectory
sigma_loc(L) = -d ln(Dm*L)/dL vs the H_dual expectation.

Data: sprint_137b_crossover_q{6,8}.json, sprint_138b_crossover_q7.json,
      sprint_139b_crossover_q10.json (S137 series + S139 tail n=32,36).

Usage:  python exp_139a_interface_tension.py
Saves results/sprint_139_analysis.json; DB: sigma_xi_product.
"""
import numpy as np
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.optimize import least_squares
from db_utils import record

RES = os.path.join(os.path.dirname(__file__), '..', 'results')
SERIES = {6: ('sprint_137b_crossover_q6.json', 158.9),
          7: ('sprint_138b_crossover_q7.json', 48.1),
          8: ('sprint_137b_crossover_q8.json', 23.9),
          10: ('sprint_139b_crossover_q10.json', 10.56)}


def load(q):
    path, xi = SERIES[q]
    d = json.load(open(os.path.join(RES, path)))
    s = {int(k): v for k, v in d['sizes'].items()}
    ns = np.array(sorted(s), float)
    dm = np.array([s[int(n)]['gap_min'] for n in ns])
    sig = []
    for n in ns:
        r = s[int(n)].get('fit_rel_resid') or 2e-3
        f = s[int(n)].get('n_fit_points')
        sig.append(max(r, 2e-3, 8e-3 if (f is not None and f < 7) else 0))
    return ns, dm, np.array(sig), xi


DATA = {q: load(q) for q in SERIES}
QS = sorted(DATA)
NPTS = sum(len(DATA[q][0]) for q in QS)


def pack_residuals(theta, s_mode, per_q_a):
    """theta layout: [lnA_q ...] + ([a] or [a_q ...]) + ([s] if free)."""
    k = len(QS)
    lnA = dict(zip(QS, theta[:k]))
    if per_q_a:
        a = dict(zip(QS, theta[k:2 * k])); j = 2 * k
    else:
        a = {q: theta[k] for q in QS}; j = k + 1
    s = theta[j] if s_mode == 'free' else s_mode
    out = []
    for q in QS:
        ns, dm, sig, xi = DATA[q]
        model = lnA[q] - a[q] * np.log(ns) - (s / xi) * ns
        out.append((np.log(dm) - model) / sig)
    return np.concatenate(out)


def fit(s_mode='free', per_q_a=False):
    k = len(QS)
    th0 = [np.log(DATA[q][1][0]) + 1.0 * np.log(DATA[q][0][0]) for q in QS]
    th0 += [1.0] * (k if per_q_a else 1)
    if s_mode == 'free':
        th0 += [0.4]
    r = least_squares(pack_residuals, th0, args=(s_mode, per_q_a), method='lm', max_nfev=20000)
    ss = float(np.sum(r.fun**2))
    npar = len(th0)
    aic = NPTS * np.log(ss / NPTS) + 2 * npar
    err = None
    if s_mode == 'free':
        try:
            J = r.jac
            cov = np.linalg.inv(J.T @ J) * ss / max(NPTS - npar, 1)
            err = float(np.sqrt(cov[-1, -1]))
        except Exception:
            pass
    return {'ss': ss, 'npar': npar, 'aic': float(aic),
            's': float(r.x[-1]) if s_mode == 'free' else float(s_mode),
            's_err': err,
            'a': (dict(zip(QS, [float(x) for x in r.x[len(QS):2 * len(QS)]])) if per_q_a
                  else float(r.x[len(QS)]))}


out = {'experiment': '139a_interface_tension', 'sprint': 139,
       'exact_anchor': '2 sigma_od = 1/xi_d (Borgs-Janke duality+wetting; H_dual: s=1/2)'}
print("=" * 88)
print("Sprint 139a: interface-tension test  --  ln Dm = lnA_q - a lnL - (s/xi_q) L  (joint)")
print(f"  data: {NPTS} points across q={QS}  (xi 10.56..158.9)")
print("=" * 88)

V1 = fit('free', False)
V2 = fit(0.5, False)
V3 = fit(0.0, False)
V4 = fit('free', True)
out.update({'V1_s_free': V1, 'V2_s_half': V2, 'V3_s_zero': V3, 'V4_perq_a': V4})

print(f"\n  V1 s FREE      : s = {V1['s']:.4f} +/- {V1['s_err']:.4f}   a = {V1['a']:.3f}   AIC = {V1['aic']:.1f}")
print(f"  V2 s = 1/2 (H_dual, exact duality): a = {V2['a']:.3f}   AIC = {V2['aic']:.1f}   dAIC vs V1 = {V2['aic']-V1['aic']:+.1f}")
print(f"  V3 s = 0   (pure shadow)          :              AIC = {V3['aic']:.1f}   dAIC vs V1 = {V3['aic']-V1['aic']:+.1f}")
print(f"  V4 s free, per-q a: s = {V4['s']:.4f} +/- {V4['s_err'] or 0:.4f}   "
      f"a_q = { {q: round(v,2) for q,v in V4['a'].items()} }   AIC = {V4['aic']:.1f}")

print("\n  per-q individual fits (3 params each):")
out['per_q'] = {}
for q in QS:
    ns, dm, sig, xi = DATA[q]
    DATA1 = {q: DATA[q]}
    QS1, NP1 = [q], len(ns)
    def res1(th):
        model = th[0] - th[1] * np.log(ns) - (th[2] / xi) * ns
        return (np.log(dm) - model) / sig
    r = least_squares(res1, [np.log(dm[0]) + np.log(ns[0]), 1.0, 0.4], method='lm')
    ss = float(np.sum(r.fun**2))
    try:
        cov = np.linalg.inv(r.jac.T @ r.jac) * ss / max(len(ns) - 3, 1)
        serr = float(np.sqrt(cov[2, 2]))
    except Exception:
        serr = None
    out['per_q'][q] = {'s': float(r.x[2]), 's_err': serr, 'a': float(r.x[1])}
    print(f"    q={q:2d} (xi={xi:6.1f}, maxL/xi={ns[-1]/xi:.2f}): s_q = {r.x[2]:.3f}"
          + (f" +/- {serr:.3f}" if serr else "") + f"   a_q = {r.x[1]:.2f}")

# q=10 TAIL-ONLY discriminator (n >= 16, L/xi >= 1.5): in the deepest-crossover window,
# is s = 1/2 (exact duality) still excluded, and is the onset value preferred?
ns_a, dm_a, sig_a, xi10 = DATA[10]
keep = ns_a >= 16
nt, dt, st = ns_a[keep], dm_a[keep], sig_a[keep]
def tail_fit(s_fix=None):
    def res(th):
        s = th[2] if s_fix is None else s_fix
        return (np.log(dt) - (th[0] - th[1] * np.log(nt) - (s / xi10) * nt)) / st
    th0 = [np.log(dt[0]) + np.log(nt[0]), 1.0] + ([0.4] if s_fix is None else [])
    r = least_squares(res, th0, method='lm')
    ss = float(np.sum(r.fun**2)); npar = len(th0)
    serr = None
    if s_fix is None:
        try:
            cov = np.linalg.inv(r.jac.T @ r.jac) * ss / max(len(nt) - npar, 1)
            serr = float(np.sqrt(cov[2, 2]))
        except Exception:
            pass
    return {'s': float(r.x[2]) if s_fix is None else s_fix, 's_err': serr,
            'a': float(r.x[1]), 'ss': ss,
            'aic': float(len(nt) * np.log(ss / len(nt)) + 2 * npar)}
tf = tail_fit(None); th = tail_fit(0.5); tq = tail_fit(0.25); tz = tail_fit(V4['s'])
out['q10_tail'] = {'n_min': 16, 'free': tf, 's_half': th, 's_quarter': tq, 's_joint': tz}
print(f"\n  q=10 TAIL-ONLY (n>=16, L/xi 1.5-3.4):  s = {tf['s']:.3f}"
      + (f" +/- {tf['s_err']:.3f}" if tf['s_err'] else ""))
print(f"      dAIC vs free:  s=1/2 (H_dual): {th['aic']-tf['aic']:+.1f}   "
      f"s=1/4 (amplitude = sigma_od/2): {tq['aic']-tf['aic']:+.1f}   "
      f"s={V4['s']:.3f} (joint): {tz['aic']-tf['aic']:+.1f}")

# q=10 local decay-rate trajectory vs H_dual expectation
ns, dm, sig, xi = DATA[10]
lnR = np.log(dm * ns)
loc = []
print("\n  q=10 local rate sigma_loc*xi = -xi * d ln(Dm*L)/dL   (H_dual expectation in []):")
a_fit = V1['a']; s_fit = V1['s']
for i in range(len(ns) - 1):
    sl = -(lnR[i + 1] - lnR[i]) / (ns[i + 1] - ns[i]) * xi
    Lm = 0.5 * (ns[i] + ns[i + 1])
    exp_dual = 0.5 - (a_fit - 1.0) * xi / Lm          # d/dL[(a-1)lnL + (s/xi)L] * xi
    loc.append([float(ns[i]), float(ns[i + 1]), float(sl), float(exp_dual)])
    print(f"    ({int(ns[i]):2d},{int(ns[i+1]):2d}) L_mid/xi={Lm/xi:4.2f}:  {sl:+.3f}   [H_dual: {exp_dual:+.3f}]")
out['q10_local'] = loc

out['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
with open(os.path.join(RES, 'sprint_139_analysis.json'), 'w') as f:
    json.dump(out, f, indent=2)
record(sprint=139, model='sq_potts', q=0, n=0, quantity='sigma_xi_product', value=V1['s'],
       error=V1['s_err'], method='joint_shadow_decay_fit_q6_7_8_10',
       notes=f"exact duality predicts 0.5; dAIC(s=1/2 vs free)={V2['aic']-V1['aic']:+.1f}, "
             f"(s=0 vs free)={V3['aic']-V1['aic']:+.1f}; a={V1['a']:.3f}; q=0/n=0 = global")
print("\nDONE -> results/sprint_139_analysis.json")

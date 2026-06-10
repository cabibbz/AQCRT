"""Sprint 138a: the q=7 parameter-free Lambda prediction test.

S137 measured Lambda_Im/xi = 1.59 (q=8), 1.71 (q=10) and Lambda_Dm/xi = 2.51, 2.71.
PREDICTION (registered in sprints/sprint_138.md BEFORE this data):
    q=7 (xi_d = 48.1):  Lambda_Im = 79 +/- 5,   Lambda_Dm = 126 +/- 7.

Tests on the S138 q=7 DMRG series (n=8..40, L/xi <= 0.83):
  T1 free shadow+decay fit  y = A L^-p exp(-L/Lambda)  vs pure power (weighted dAIC),
     free Lambda vs the prediction band.
  T2 FIXED-Lambda fit (Lambda pinned at the predicted value; 2 free params, same count
     as pure power): direct weighted-SS comparison -- does the PREDICTION itself beat
     pure power with no extra freedom?
  T3 matched-window calibration: q=8 restricted to n<=20 (L/xi <= 0.84) -- how much decay
     signal does a confirmed-crossover q show in the same L/xi window?
  T4 internal consistency: Lambda_Dm / Lambda_Im vs the ~1.6 ratio at q=8,10.

Usage:  python exp_138a_q7_prediction.py
Saves results/sprint_138_analysis.json; DB: crossover_Lambda (q=7), lambda_pred_ratio.
"""
import numpy as np
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.optimize import curve_fit
from db_utils import record

RES = os.path.join(os.path.dirname(__file__), '..', 'results')
XI7 = 48.1
PRED = {'im': (1.65 * XI7, 0.09 * XI7), 'dm': (2.61 * XI7, 0.14 * XI7)}   # (79.4+/-4.3, 125.5+/-6.7)


def load(path):
    d = json.load(open(os.path.join(RES, path)))
    s = {int(k): v for k, v in d['sizes'].items()}
    ns = np.array(sorted(s), float)
    out = {'n': ns}
    for key, fld in [('im', 'im_gEP'), ('dm', 'gap_min')]:
        out[key] = np.array([s[int(n)][fld] for n in ns])
    rr = [s[int(n)].get('fit_rel_resid') for n in ns]
    nf = [s[int(n)].get('n_fit_points') for n in ns]
    out['sig'] = np.array([max(max(r if r else 2e-3, 2e-3), 8e-3 if (f is not None and f < 7) else 0)
                           for r, f in zip(rr, nf)])
    return out


def wfit(ns, y, sig, model, p0, bounds):
    popt, pcov = curve_fit(model, ns, np.log(y), p0=p0, sigma=sig, absolute_sigma=False,
                           bounds=bounds, maxfev=60000)
    ss = float(np.sum(((np.log(y) - model(ns, *popt)) / sig)**2))
    return popt, pcov, ss


def aic(n_pts, ss, k):
    return n_pts * np.log(ss / n_pts) + 2 * k


def analyze(dat, key, lam_fixed=None, xi=None):
    ns, y, sig = dat['n'], dat[key], dat['sig']
    mp = lambda L, lA, p: lA - p * np.log(L)
    md = lambda L, lA, p, iv: lA - p * np.log(L) - L * iv
    pp, _, ss_pp = wfit(ns, y, sig, mp, [0.0, 1.5], ([-50, 0], [50, 4]))
    sd, sd_cov, ss_sd = wfit(ns, y, sig, md, [0.0, 1.2, 1e-3],
                             ([-50, 0, 0], [50, 4, 1]))
    lam = 1.0 / sd[2] if sd[2] > 1e-12 else float('inf')
    with np.errstate(invalid='ignore'):
        lam_err = (np.sqrt(np.diag(sd_cov))[2] / sd[2]**2) if sd[2] > 1e-12 else None
    res = {'power_p': float(pp[1]), 'decay_p': float(sd[1]),
           'Lambda': float(lam), 'Lambda_err': float(lam_err) if lam_err and np.isfinite(lam_err) else None,
           'Lambda_over_xi': float(lam / xi) if (xi and np.isfinite(lam)) else None,
           'dAIC_power_minus_decay': float(aic(len(ns), ss_pp, 2) - aic(len(ns), ss_sd, 3)),
           'slopes': [[int(ns[i]), int(ns[i + 1]),
                       float((np.log(y[i + 1] / y[i])) / np.log(ns[i + 1] / ns[i]))]
                      for i in range(len(ns) - 1)]}
    if lam_fixed:
        mf = lambda L, lA, p: lA - p * np.log(L) - L / lam_fixed
        _, _, ss_fx = wfit(ns, y, sig, mf, [0.0, 1.2], ([-50, 0], [50, 4]))
        res['fixedLam'] = {'Lambda': lam_fixed,
                           'dAIC_power_minus_fixed': float(aic(len(ns), ss_pp, 2) - aic(len(ns), ss_fx, 2))}
    return res


out = {'experiment': '138a_q7_prediction', 'sprint': 138, 'xi7': XI7,
       'prediction': {k: {'Lambda': v[0], 'err': v[1]} for k, v in PRED.items()}}
print("=" * 86)
print("Sprint 138a: q=7 Lambda prediction test  (predicted Lambda_Im=79+/-5, Lambda_Dm=126+/-7)")
print("=" * 86)

q7 = load('sprint_138b_crossover_q7.json')
for key, label in [('dm', 'Dm   '), ('im', 'Im_EP')]:
    lam_p = PRED[key][0]
    r = analyze(q7, key, lam_fixed=lam_p, xi=XI7)
    out[f'q7_{key}'] = r
    lam_s = f"{r['Lambda']:.0f}" if np.isfinite(r['Lambda']) else "inf"
    err_s = f"+/-{r['Lambda_err']:.0f}" if r['Lambda_err'] else ""
    print(f"\n[{label}] slopes: {[round(s[2], 2) for s in r['slopes']]}")
    print(f"  T1 free fit:   Lambda = {lam_s}{err_s}  (= {r['Lambda_over_xi']:.2f} xi)" if r['Lambda_over_xi']
          else f"  T1 free fit:   Lambda = {lam_s}{err_s}")
    print(f"                 predicted {lam_p:.0f} +/- {PRED[key][1]:.0f}   "
          f"dAIC(power-decay) = {r['dAIC_power_minus_decay']:+.1f}")
    print(f"  T2 fixed-Lambda={lam_p:.0f} (no extra params): dAIC(power-fixed) = "
          f"{r['fixedLam']['dAIC_power_minus_fixed']:+.1f}  (>0 = the PREDICTION beats pure power)")

# T3: matched-window q=8 calibration (n<=20, L/xi<=0.84)
q8 = load('sprint_137b_crossover_q8.json')
keep = q8['n'] <= 20
q8m = {'n': q8['n'][keep], 'im': q8['im'][keep], 'dm': q8['dm'][keep], 'sig': q8['sig'][keep]}
print("\n[T3] q=8 matched window (n<=20, L/xi<=0.84) calibration:")
for key in ['dm', 'im']:
    r = analyze(q8m, key, xi=23.9)
    out[f'q8_matched_{key}'] = r
    lam_s = f"{r['Lambda']:.0f}" if np.isfinite(r['Lambda']) else "inf"
    print(f"  {key}: dAIC = {r['dAIC_power_minus_decay']:+.1f}, Lambda = {lam_s}"
          + (f" ({r['Lambda_over_xi']:.2f} xi)" if r['Lambda_over_xi'] else ""))

# T4: internal ratio
ld, li = out['q7_dm']['Lambda'], out['q7_im']['Lambda']
if np.isfinite(ld) and np.isfinite(li) and li > 0:
    out['Lambda_dm_over_im'] = ld / li
    print(f"\n[T4] Lambda_Dm/Lambda_Im = {ld/li:.2f}  (q=8: 1.58, q=10: 1.59)")

out['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
with open(os.path.join(RES, 'sprint_138_analysis.json'), 'w') as f:
    json.dump(out, f, indent=2)

for key in ['dm', 'im']:
    r = out[f'q7_{key}']
    if np.isfinite(r['Lambda']):
        record(sprint=138, model='sq_potts', q=7, n=int(max(q7['n'])), quantity='crossover_Lambda',
               value=r['Lambda'], error=r['Lambda_err'],
               method=f'shadow_decay_fit_{key.capitalize()}_dmrg_open',
               notes=f"predicted {PRED[key][0]:.0f}+/-{PRED[key][1]:.0f} (S137 Lambda~xi); "
                     f"dAIC={r['dAIC_power_minus_decay']:+.1f}; xi_exact=48.1")
print("\nDONE -> results/sprint_138_analysis.json")

"""Sprint 137c: analysis -- (1) the walking-crossover verdict from the 137b DMRG data,
(2) the PROPER Coulomb-gas (Jacobsen-Wiese-style analytic continuation) comparison the
audit demanded before any further 'complex-CFT shadow' language.

(1) Shadow+decay model:  Im(g_EP)(L) = A * L^(-p) * exp(-L/Lambda).
    Pure shadow (L<<xi): Lambda -> infinity, p ~ Re(1/nu_complex).
    First-order crossover: Lambda ~ O(xi). Local slope = -p - L/Lambda steepens LINEARLY
    in L -- the q=10 (xi=10.6) curve should need finite Lambda, the q=6 control
    (xi=158.9) should not. Fit per q on the 137b open-DMRG series; AIC-compare against
    the pure power law.

(2) Coulomb-gas continuation (den Nijs parametrization, validated on exact Q<=4):
    sqrt(Q) = 2 cos(pi v / 2),  x_eps = (1+v)/(2-v),  y_t = 1/nu = 2 - x_eps = 3(1-v)/(2-v).
    For Q>4: v = -i*theta, cosh(pi theta/2) = sqrt(Q)/2  =>  complex y_t;
    Re(y_t) = 3(2+theta^2)/(4+theta^2),  |Im(y_t)| = 3 theta/(4+theta^2).
    This is the same analytic continuation underlying Jacobsen-Wiese PRL 133 077101 (2024).

Usage:  python exp_137c_crossover_analysis.py
Saves results/sprint_137_analysis.json; DB: crossover_Lambda (per q), inv_nu_complex_re (per q).
"""
import numpy as np
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.optimize import curve_fit
from db_utils import record

RES = os.path.join(os.path.dirname(__file__), '..', 'results')
OUT = os.path.join(RES, 'sprint_137_analysis.json')
XI = {5: 2512.2, 6: 158.9, 7: 48.1, 8: 23.9, 10: 10.56}

# ---------------- (2) Coulomb-gas continuation ----------------
def y_t_complex(Q):
    """1/nu from the den Nijs Coulomb-gas formula, analytically continued to Q>4.
    Returns (Re, Im>=0) -- exact real value for Q<=4."""
    if Q <= 4:
        v = (2.0 / np.pi) * np.arccos(np.sqrt(Q) / 2.0)
        return 3.0 * (1 - v) / (2 - v), 0.0
    th = (2.0 / np.pi) * np.arccosh(np.sqrt(Q) / 2.0)
    return 3.0 * (2 + th**2) / (4 + th**2), 3.0 * th / (4 + th**2)


def validate_coulomb():
    exact = {1: 0.75, 2: 1.0, 3: 1.2, 4: 1.5}
    ok = True
    for Q, target in exact.items():
        re, im = y_t_complex(Q)
        good = abs(re - target) < 1e-12 and im == 0.0
        ok &= good
        print(f"  CG validation Q={Q}: y_t={re:.6f} (exact {target})  {'OK' if good else 'FAIL'}")
    return ok


# ---------------- (1) crossover fits ----------------
def shadow_decay(L, A, p, invLam):
    return A * L**(-p) * np.exp(-L * invLam)


def pure_power(L, A, p):
    return A * L**(-p)


def aic(n_pts, ss_res, k):
    return n_pts * np.log(ss_res / n_pts) + 2 * k


def analyze_q(q):
    path = os.path.join(RES, f'sprint_137b_crossover_q{q}.json')
    if not os.path.exists(path):
        return None
    d = json.load(open(path))
    s = {int(k): v for k, v in d['sizes'].items()}
    ns = np.array(sorted(s), float)
    if len(ns) < 4:
        return None
    im = np.array([s[int(n)]['im_gEP'] for n in ns])
    ln_im = np.log(im)

    # pure power
    pp, _ = curve_fit(lambda L, A, p: np.log(pure_power(L, A, p)), ns, ln_im,
                      p0=[im[0] * ns[0], 1.5], maxfev=20000)
    ss_pp = float(np.sum((ln_im - np.log(pure_power(ns, *pp)))**2))
    # shadow + decay (fit in log space; invLam >= 0)
    sd, sd_cov = curve_fit(lambda L, A, p, iv: np.log(shadow_decay(L, A, p, iv)), ns, ln_im,
                           p0=[im[0] * ns[0], 1.2, 1e-3],
                           bounds=([1e-12, 0.0, 0.0], [1e6, 4.0, 1.0]), maxfev=40000)
    ss_sd = float(np.sum((ln_im - np.log(shadow_decay(ns, *sd)))**2))
    Lam = (1.0 / sd[2]) if sd[2] > 1e-12 else float('inf')
    Lam_err = float(np.sqrt(np.diag(sd_cov))[2] / sd[2]**2) if sd[2] > 1e-12 else None
    a_pp, a_sd = aic(len(ns), ss_pp, 2), aic(len(ns), ss_sd, 3)
    slopes = [[int(ns[i]), int(ns[i + 1]),
               float((ln_im[i + 1] - ln_im[i]) / (np.log(ns[i + 1]) - np.log(ns[i])))]
              for i in range(len(ns) - 1)]
    return {'q': q, 'xi': XI.get(q), 'n': ns.tolist(), 'im_gEP': im.tolist(),
            'local_slopes': slopes,
            'pure_power': {'p': float(pp[1]), 'ss': ss_pp, 'aic': a_pp},
            'shadow_decay': {'p': float(sd[1]), 'Lambda': Lam, 'Lambda_err': Lam_err,
                             'Lambda_over_xi': (Lam / XI[q]) if (XI.get(q) and np.isfinite(Lam)) else None,
                             'ss': ss_sd, 'aic': a_sd},
            'dAIC_power_minus_decay': a_pp - a_sd}


out = {'experiment': '137_analysis', 'sprint': 137, 'coulomb_gas': {}, 'crossover': {}}
print("=" * 86)
print("Sprint 137c: crossover verdict + Coulomb-gas continuation comparison")
print("=" * 86)
print("\n[2] Coulomb-gas 1/nu (den Nijs / Jacobsen-Wiese analytic continuation):")
assert validate_coulomb(), "Coulomb-gas formula failed exact validation"
meas_ed = {5: 1.505, 6: 1.648, 7: 1.775}      # S136 periodic-ED power-fit p (results/sprint_136_analysis.json)
for Q in [5, 6, 7, 8, 9, 10]:
    re, imv = y_t_complex(Q)
    out['coulomb_gas'][Q] = {'re_inv_nu': re, 'im_inv_nu': imv}
    m = f"   measured(S136 ED, effective) p={meas_ed[Q]}" if Q in meas_ed else ""
    print(f"  q={Q}: Re(1/nu)={re:.4f}  |Im(1/nu)|={imv:.4f}{m}")
    record(sprint=137, model='sq_potts', q=Q, n=0, quantity='inv_nu_complex_re', value=re,
           error=None, method='coulomb_gas_continuation',
           notes=f'den Nijs CG, |Im|={imv:.4f}; n=0 sentinel = size-independent theory value')

print("\n[1] crossover fits  Im(g_EP) = A L^-p exp(-L/Lambda)   (137b open-BC Z_q DMRG):")
for q in [6, 8, 10]:
    r = analyze_q(q)
    if r is None:
        print(f"  q={q}: insufficient data")
        continue
    out['crossover'][q] = r
    sd = r['shadow_decay']
    lam_s = f"{sd['Lambda']:.1f}" if np.isfinite(sd['Lambda']) else "inf"
    lox = f" = {sd['Lambda_over_xi']:.2f} xi" if sd['Lambda_over_xi'] else ""
    print(f"  q={q} (xi={r['xi']}):  slopes {[round(s[2], 3) for s in r['local_slopes']]}")
    print(f"        pure power p={r['pure_power']['p']:.3f}  vs  shadow+decay p={sd['p']:.3f}, "
          f"Lambda={lam_s}{lox}   dAIC(power-decay)={r['dAIC_power_minus_decay']:+.1f}")
    if np.isfinite(sd['Lambda']):
        record(sprint=137, model='sq_potts', q=q, n=int(max(r['n'])), quantity='crossover_Lambda',
               value=sd['Lambda'], error=sd['Lambda_err'], method='shadow_decay_fit_dmrg_open',
               notes=f"p={sd['p']:.3f}; xi_exact={r['xi']}; dAIC vs pure power={r['dAIC_power_minus_decay']:+.1f}")

out['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
with open(OUT, 'w') as f:
    json.dump(out, f, indent=2)
print("\nDONE ->", OUT)

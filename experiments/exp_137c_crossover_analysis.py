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


def _fit_series(ns, y, q, relres=None):
    """Pure-power vs shadow+decay comparison for one series y(L) (log-space fits).
    Points are weighted by their per-size hyperbola fit quality: sigma_i =
    max(fit_rel_resid_i, 2e-3) -- small-n sizes have a ~1e-2 model-error floor
    (wide dips), large-n fits are clean; unweighted fits would let the noisy small-n
    points distort the crossover term."""
    ln_y = np.log(y)
    rr, nf = relres if relres is not None else ([None] * len(ns), [None] * len(ns))
    sig = np.array([max(r if r else 2e-3, 2e-3) for r in rr])
    # a 4-param hyperbola through <7 points is exact-identified: its residual is fake
    # precision (caught at q=10 n=8/10: 6-18% parameter moves on re-measurement).
    # Floor such points at the empirical model-error scale instead.
    sig = np.array([max(s, 8e-3) if (f is not None and f < 7) else s
                    for s, f in zip(sig, nf)])
    pp, _ = curve_fit(lambda L, A, p: np.log(pure_power(L, A, p)), ns, ln_y,
                      p0=[y[0] * ns[0], 1.5], sigma=sig, absolute_sigma=False, maxfev=20000)
    ss_pp = float(np.sum(((ln_y - np.log(pure_power(ns, *pp))) / sig)**2))
    sd, sd_cov = curve_fit(lambda L, A, p, iv: np.log(shadow_decay(L, A, p, iv)), ns, ln_y,
                           p0=[y[0] * ns[0], 1.2, 1e-3], sigma=sig, absolute_sigma=False,
                           bounds=([1e-12, 0.0, 0.0], [1e6, 4.0, 1.0]), maxfev=40000)
    ss_sd = float(np.sum(((ln_y - np.log(shadow_decay(ns, *sd))) / sig)**2))
    Lam = (1.0 / sd[2]) if sd[2] > 1e-12 else float('inf')
    with np.errstate(invalid='ignore'):
        dia = np.sqrt(np.diag(sd_cov))
    Lam_err = float(dia[2] / sd[2]**2) if (sd[2] > 1e-12 and np.isfinite(dia[2])) else None
    a_pp, a_sd = aic(len(ns), ss_pp, 2), aic(len(ns), ss_sd, 3)
    slopes = [[int(ns[i]), int(ns[i + 1]),
               float((ln_y[i + 1] - ln_y[i]) / (np.log(ns[i + 1]) - np.log(ns[i])))]
              for i in range(len(ns) - 1)]
    return {'local_slopes': slopes,
            'pure_power': {'p': float(pp[1]), 'ss': ss_pp, 'aic': a_pp},
            'shadow_decay': {'p': float(sd[1]), 'Lambda': Lam, 'Lambda_err': Lam_err,
                             'Lambda_over_xi': (Lam / XI[q]) if (XI.get(q) and np.isfinite(Lam)) else None,
                             'ss': ss_sd, 'aic': a_sd},
            'dAIC_power_minus_decay': a_pp - a_sd}


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
    dm = np.array([s[int(n)]['gap_min'] for n in ns])
    # Two series: Im = Dm/c1 (the EP observable; c1 division adds smooth power only but
    # carries fit-degeneracy noise at sizes with few kept points) and Dm itself (robustly
    # pinned by the sampled minimum; the exponential crossover lives in Dm).
    rr = [s[int(n)].get('fit_rel_resid') for n in ns]
    nf = [s[int(n)].get('n_fit_points') for n in ns]
    return {'q': q, 'xi': XI.get(q), 'n': ns.tolist(), 'im_gEP': im.tolist(),
            'gap_min': dm.tolist(), 'fit_relres': rr, 'n_fit_points': nf,
            'im': _fit_series(ns, im, q, (rr, nf)), 'dm': _fit_series(ns, dm, q, (rr, nf))}


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

print("\n[1] crossover fits  y(L) = A L^-p exp(-L/Lambda)   (137b open-BC Z_q DMRG):")
for q in [6, 8, 10]:
    r = analyze_q(q)
    if r is None:
        print(f"  q={q}: insufficient data")
        continue
    out['crossover'][q] = r
    print(f"  q={q} (xi={r['xi']}):")
    for key, label in [('dm', 'Dm   '), ('im', 'Im_EP')]:
        f = r[key]; sd = f['shadow_decay']
        lam_s = f"{sd['Lambda']:.1f}" if np.isfinite(sd['Lambda']) else "inf"
        lox = f" = {sd['Lambda_over_xi']:.2f} xi" if sd['Lambda_over_xi'] else ""
        print(f"    {label}: slopes {[round(s[2], 2) for s in f['local_slopes']]}")
        print(f"           power p={f['pure_power']['p']:.3f}  vs  decay p={sd['p']:.3f} "
              f"Lambda={lam_s}{lox}   dAIC(power-decay)={f['dAIC_power_minus_decay']:+.1f}")
    sd = r['dm']['shadow_decay']
    if np.isfinite(sd['Lambda']):
        record(sprint=137, model='sq_potts', q=q, n=int(max(r['n'])), quantity='crossover_Lambda',
               value=sd['Lambda'], error=sd['Lambda_err'], method='shadow_decay_fit_Dm_dmrg_open',
               notes=f"from gap_min series; p={sd['p']:.3f}; xi_exact={r['xi']}; "
                     f"dAIC vs pure power={r['dm']['dAIC_power_minus_decay']:+.1f}")

out['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
with open(OUT, 'w') as f:
    json.dump(out, f, indent=2)
print("\nDONE ->", OUT)

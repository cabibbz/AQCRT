"""Sprint 135 analysis: does OPEN on-peak chi_F(L) for q=4 follow the proven leading exponent
2/nu-d=2.0 suppressed by the marginal (dilution) operator's log, and is that log ABSENT for q=3?

Builds the on-peak per-site chi_F series from results.db chi_F_open_peak:
  - q=4: S134 exact canonical (dg=1e-4) n<=12  +  S135 DMRG (dg=1e-3) n>12   (mixed, gold anchor)
         also a SINGLE-METHOD S135 DMRG-only series (check the method/dg junction is harmless)
  - q=3 CONTROL: S135 DMRG  (no marginal operator -> null 1.40, power-law corrections)

TWO complementary views:
 (1) Direct chi_F(L) data fits (log space, ln chi = ln a + kappa ln L + sigma ln ln L):
       (A) pure power     ln chi = ln a + kappa ln L                 -> free effective kappa
       (B) forced-null+log ln chi = ln a + NULL*ln L + sigma ln ln L -> marginal log amplitude
       (C) free power+log  ln chi = ln a + kappa ln L + sigma ln ln L-> does kappa -> NULL w/ a log?
     Compare SSR (A vs B same #params). For q=4 expect (B)/(C) competitive and (C) kappa near 2 with
     sigma<0; for q=3 expect (A) best and sigma~0 (no marginal op).
 (2) kappa_eff(L) pairwise + Cardy/Hamer 1/ln L extrapolation kappa_eff = K_inf + s/lnL (intercept K_inf).

Usage: python exp_135_analysis.py    Reads DB; writes results/sprint_135_analysis.json.
"""
import numpy as np, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from db_utils import query

NULL = {2: 1.0, 3: 1.4, 4: 2.0}
RES = os.path.join(os.path.dirname(__file__), '..', 'results')

def db_series(q, sprint):
    return {r[4]: r[6] for r in query(quantity='chi_F_open_peak', q=q) if r[1] == sprint}

def lstsq(X, y):
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ c
    ssr = float(resid @ resid)
    r2 = float(1 - ssr / np.sum((y - y.mean()) ** 2))
    return c, ssr, r2

def chiF_data_fits(series, null):
    ns = np.array(sorted(series), dtype=float)
    chi = np.array([series[int(n)] for n in ns])
    lnL, lnchi, lnlnL = np.log(ns), np.log(chi), np.log(np.log(ns))
    one = np.ones_like(lnL)
    cA, sA, rA = lstsq(np.vstack([one, lnL]).T, lnchi)                 # power
    cB, sB, rB = lstsq(np.vstack([one, lnlnL]).T, lnchi - null * lnL)  # forced null + log
    cC, sC, rC = lstsq(np.vstack([one, lnL, lnlnL]).T, lnchi)          # free power + log
    return {
        'sizes': ns.tolist(),
        'power':        {'kappa': float(cA[1]), 'ssr': sA, 'r2': rA},
        'forced_null_log': {'null': null, 'sigma': float(cB[1]), 'ssr': sB, 'r2': rB},
        'free_power_log': {'kappa': float(cC[1]), 'sigma': float(cC[2]), 'ssr': sC, 'r2': rC},
    }

def kappa_pairwise(series):
    ns = sorted(series)
    out = []
    for i in range(len(ns) - 1):
        a, b = ns[i], ns[i + 1]
        k = (np.log(series[b]) - np.log(series[a])) / (np.log(b) - np.log(a))
        Lm = (a * b) ** 0.5
        out.append({'pair': (a, b), 'L_mid': Lm, 'inv_lnL': 1.0 / np.log(Lm), 'kappa': k})
    return out

def kappa_invlnL_fit(pw):
    x = np.array([r['inv_lnL'] for r in pw]); y = np.array([r['kappa'] for r in pw])
    c, ssr, r2 = lstsq(np.vstack([np.ones_like(x), x]).T, y)
    return {'K_inf': float(c[0]), 'slope': float(c[1]), 'r2': r2, 'ssr': ssr}

def kappa_surface_fits(pw, null):
    """OPEN BC kappa_eff carries BOTH a marginal log (s/lnL) and a surface term (d/L). Fit:
       free3 : kappa = K + s/lnL + d/L     (free intercept K; does K land near null?)
       fixed : kappa = null + s/lnL + d/L  (intercept FIXED at proven null; small residual => consistent)
       surf  : kappa = K + d/L             (NO log term; good for q=3, should be poor for q=4)
    Need >=4 pairwise points for free3."""
    invlnL = np.array([r['inv_lnL'] for r in pw])
    invL = np.array([1.0 / r['L_mid'] for r in pw])
    y = np.array([r['kappa'] for r in pw])
    out = {}
    if len(y) >= 4:
        c, ssr, r2 = lstsq(np.vstack([np.ones_like(y), invlnL, invL]).T, y)
        out['free3'] = {'K_inf': float(c[0]), 's_log': float(c[1]), 'd_surf': float(c[2]), 'ssr': ssr, 'r2': r2}
    if len(y) >= 3:
        c, ssr, r2 = lstsq(np.vstack([invlnL, invL]).T, y - null)   # intercept fixed = null
        out['fixed_null'] = {'null': null, 's_log': float(c[0]), 'd_surf': float(c[1]), 'ssr': ssr,
                             'max_resid': float(np.max(np.abs((y - null) - np.vstack([invlnL, invL]).T @ c)))}
        c2, ssr2, r22 = lstsq(np.vstack([np.ones_like(y), invL]).T, y)   # K + d/L, no log
        out['surface_only'] = {'K_inf': float(c2[0]), 'd_surf': float(c2[1]), 'ssr': ssr2, 'r2': r22}
    return out

def report(q, label, series):
    null = NULL[q]
    print("\n" + "=" * 80)
    print(f"q={q}  [{label}]   null 2/nu-d = {null}   sizes={sorted(series)}  ({len(series)} pts)")
    print("=" * 80)
    if len(series) < 4:
        print("  <4 sizes, skipping fits"); return {'q': q, 'label': label, 'series': series}
    f = chiF_data_fits(series, null)
    print("  -- direct chi_F(L) data fits (log space) --")
    print(f"   (A) pure power        kappa={f['power']['kappa']:.4f}                  SSR={f['power']['ssr']:.3e} R2={f['power']['r2']:.6f}")
    print(f"   (B) forced {null}+log    sigma={f['forced_null_log']['sigma']:+.4f}              SSR={f['forced_null_log']['ssr']:.3e} R2={f['forced_null_log']['r2']:.6f}")
    print(f"   (C) free power+log    kappa={f['free_power_log']['kappa']:.4f} sigma={f['free_power_log']['sigma']:+.4f}  SSR={f['free_power_log']['ssr']:.3e} R2={f['free_power_log']['r2']:.6f}")
    win = 'B(=null+log)' if f['forced_null_log']['ssr'] < f['power']['ssr'] else 'A(free power)'
    print(f"   --> A vs B (same #params): SSR winner = {win}")
    pw = kappa_pairwise(series)
    kfit = kappa_invlnL_fit(pw)
    print("  -- kappa_eff(L) pairwise + Cardy/Hamer 1/lnL extrapolation --")
    print(f"   {'pair':>9} {'L_mid':>6} {'1/lnL':>7} {'kappa':>8}")
    for r in pw:
        print(f"   {str(r['pair']):>9} {r['L_mid']:6.2f} {r['inv_lnL']:7.4f} {r['kappa']:8.4f}")
    print(f"   naive  kappa = K + s/lnL          :  K_inf={kfit['K_inf']:.3f} (UNRELIABLE for open BC -- see q=3 control)")
    sfit = kappa_surface_fits(pw, null)
    if 'free3' in sfit:
        print(f"   +surf  kappa = K + s/lnL + d/L     :  K_inf={sfit['free3']['K_inf']:.3f}  s={sfit['free3']['s_log']:+.3f}  d={sfit['free3']['d_surf']:+.2f}  R2={sfit['free3']['r2']:.4f}")
    if 'fixed_null' in sfit:
        print(f"   fix={null} kappa = {null} + s/lnL + d/L:  s={sfit['fixed_null']['s_log']:+.3f}  d={sfit['fixed_null']['d_surf']:+.2f}  max|resid|={sfit['fixed_null']['max_resid']:.3f}  (small => consistent w/ proven null)")
        print(f"   no-log kappa = K + d/L            :  K_inf={sfit['surface_only']['K_inf']:.3f}  R2={sfit['surface_only']['r2']:.4f}  (q=3 should fit; q=4 should be biased high/poor)")
    return {'q': q, 'label': label, 'series': {int(k): v for k, v in series.items()},
            'data_fits': f, 'kappa_pairwise': pw, 'kappa_invlnL': kfit, 'kappa_surface': sfit}

if __name__ == '__main__':
    out = {'experiment': '135_analysis'}
    q4_mixed = {**db_series(4, 134), **db_series(4, 135)}   # exact n<=12 overwritten by DMRG where present
    q4_dmrg = db_series(4, 135)
    out['q4_mixed'] = report(4, 'open on-peak: exact(S134,n<=12)+DMRG(S135,n>12)', q4_mixed)
    out['q4_dmrg_only'] = report(4, 'open on-peak: DMRG-only (S135)', q4_dmrg)

    q3_dmrg = db_series(3, 135)
    if len(q3_dmrg) >= 4:
        out['q3_control'] = report(3, 'open on-peak CONTROL: DMRG (no marginal op)', q3_dmrg)
    else:
        print("\n[q=3 control: <4 DMRG sizes yet]")

    with open(os.path.join(RES, 'sprint_135_analysis.json'), 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print("\nDONE -- results/sprint_135_analysis.json")

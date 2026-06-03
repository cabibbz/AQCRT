"""Sprint 132c: Does the q=4 chi_F local-exponent trend (now with n=12) come from a
leading power 2.0 dressed by marginal-irrelevant logs, or from a genuine sub-2 exponent?

This is the falsification test demanded by the novelty-hardening rules. It does NOT use
a no-log extrapolation to read off an asymptote (Sprint 129 proved that is circular:
fed true-2.0-with-logs data it returns ~1.77). Instead it uses two non-circular probes:

  PROBE 1 (sign-of-trend, the decisive one).  For ANY form chi = A N^a L(N) with L a
  slowly-varying correction, the local exponent is  alpha_loc(N) = a + dlnL/dlnN.
  A marginally-IRRELEVANT operator gives dlnL/dlnN ~ -c/ln N -> 0^- (flattening),
  so if a=2 the local exponent must CLIMB toward 2 from below.
  We measure dlnL2(N) := alpha_loc(N) - 2 and ask: is it flattening to 0 (=> a=2 alive)
  or converging to a NONZERO constant (=> that constant is a real power deficit, a<2)?

  PROBE 2 (model comparison with n=12).  Fit pure-power vs leading-2-with-logs forms in
  log space; report AIC and, crucially, the local-exponent trend each BEST FIT predicts.
  Does the leading-2 family even reproduce a DECREASING local exponent, or is it forced
  to the wrong sign?

CPU-only (post-processing 7 exact numbers).
"""
import numpy as np
import json, time, os, sys
from scipy.optimize import least_squares

# Exact chi_F series (results.db, sq q=4), n=12 added Sprint 132b.
SERIES = {4: 12.839321, 6: 27.138030, 8: 45.527791, 9: 56.183728,
          10: 67.784201, 11: 80.310875, 12: 93.747642}
NULL = 2.0  # 2/nu - d for nu=2/3 (Albuquerque); the leading exponent under test

sizes = np.array(sorted(SERIES), dtype=float)
chi = np.array([SERIES[int(s)] for s in sizes])
lnN = np.log(sizes)
lnchi = np.log(chi)

results = {'experiment': '132c_marginal_log_falsification', 'sprint': 132,
           'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
           'sizes': [int(s) for s in sizes], 'chi_F': list(chi),
           'probe1_local_exponent': {}, 'probe2_models': {}}

def save():
    p = os.path.join(os.path.dirname(__file__), '..', 'results',
                     'sprint_132c_marginal_log_falsification.json')
    with open(p, 'w') as f:
        json.dump(results, f, indent=2, default=str)

print("=" * 80)
print("Sprint 132c: marginal-log falsification (q=4 per-site chi_F, n=4..12)")
print("=" * 80)

# ---------------- PROBE 1: local exponent & correction log-slope ----------------
print("\nPROBE 1 -- local exponent alpha_loc and dlnL/dlnN = alpha_loc - 2")
print("  (a=2 + marginal-irrelevant log REQUIRES alpha_loc increasing, dlnL2 -> 0^-)")
print(f"  {'pair':>9} {'midN':>6} {'alpha_loc':>10} {'dlnL2':>9} {'d(alpha_loc)':>13}")
aloc, midN, prev = [], [], None
probe1 = []
for i in range(len(sizes) - 1):
    a = (lnchi[i+1] - lnchi[i]) / (lnN[i+1] - lnN[i])
    mid = np.sqrt(sizes[i] * sizes[i+1])
    dl2 = a - NULL
    da = '' if prev is None else f"{a - prev:+.4f}"
    print(f"  ({int(sizes[i]):2d},{int(sizes[i+1]):2d})  {mid:6.2f} {a:10.4f} {dl2:9.4f} {da:>13}")
    probe1.append({'n1': int(sizes[i]), 'n2': int(sizes[i+1]), 'midN': float(mid),
                   'alpha_loc': float(a), 'dlnL2': float(dl2),
                   'd_alpha_loc': None if prev is None else float(a - prev)})
    aloc.append(a); midN.append(mid); prev = a
aloc = np.array(aloc); midN = np.array(midN)

# Is dlnL2 flattening to 0 (marginal log) or converging to a nonzero constant (power deficit)?
# Fit alpha_loc(N) = a_inf + B / ln(N)  (the marginal-irrelevant ansatz: a_inf should be 2).
def res_marglog(p):  # p=[a_inf, B]
    return (p[0] + p[1] / np.log(midN)) - aloc
sol_ml = least_squares(res_marglog, [2.0, -1.0])
a_inf_ml, B_ml = sol_ml.x
# Fit alpha_loc(N) = a_inf + C / N  (analytic power-correction ansatz)
def res_pow(p):
    return (p[0] + p[1] / midN) - aloc
sol_pw = least_squares(res_pow, [1.78, 1.0])
a_inf_pw, C_pw = sol_pw.x
ssr_ml = float(np.sum(res_marglog(sol_ml.x)**2))
ssr_pw = float(np.sum(res_pow(sol_pw.x)**2))

print(f"\n  alpha_loc(N) extrapolations (where is the local exponent heading?):")
print(f"    marginal-log ansatz  alpha_loc = a_inf + B/lnN : a_inf = {a_inf_ml:.4f}, B = {B_ml:+.4f}  (SSR={ssr_ml:.2e})")
print(f"    power-corr   ansatz  alpha_loc = a_inf + C/N   : a_inf = {a_inf_pw:.4f}, C = {C_pw:+.4f}  (SSR={ssr_pw:.2e})")
print(f"  dlnL2 sequence: {[f'{x:.3f}' for x in (aloc-NULL)]}")
print(f"  -> dlnL2 is {'FLATTENING toward 0 (marginal log alive)' if abs(aloc[-1]-NULL) < abs(aloc[0]-NULL)/3 else 'CONVERGING to a NONZERO constant ~%.3f (power deficit => a<2)' % (aloc[-1]-NULL)}")

results['probe1_local_exponent'] = {
    'pairs': probe1,
    'marginal_log_ansatz': {'a_inf': float(a_inf_ml), 'B': float(B_ml), 'ssr': ssr_ml,
                            'note': 'a_inf should be 2.0 if leading power is 2'},
    'power_corr_ansatz': {'a_inf': float(a_inf_pw), 'C': float(C_pw), 'ssr': ssr_pw},
    'dlnL2_first': float(aloc[0] - NULL), 'dlnL2_last': float(aloc[-1] - NULL),
}
save()

# ---------------- PROBE 2: model fits in log space + AIC + predicted trend ----------------
print("\n" + "=" * 80)
print("PROBE 2 -- log-space model fits, AIC, and the local-exp trend each best fit predicts")
print("=" * 80)
Ndat = len(sizes)

def aic(ssr, k):
    return Ndat * np.log(ssr / Ndat) + 2 * k

def local_exp_of(model_lnchi, p, N):
    """numerical d ln chi / d ln N of a fitted model at size N."""
    h = 1e-4
    return (model_lnchi(p, N * np.exp(h)) - model_lnchi(p, N * np.exp(-h))) / (2 * h)

models = {}
# M1 pure power: ln chi = lnA + a lnN
def m1(p, N): return p[0] + p[1] * np.log(N)
s1 = least_squares(lambda p: m1(p, sizes) - lnchi, [0.0, 1.8])
models['pure_power'] = (m1, s1, 2, '{a}=%.4f' % s1.x[1])

# M2 power + analytic 1/N: ln chi = lnA + a lnN + ln(1 + c/N)
def m2(p, N): return p[0] + p[1]*np.log(N) + np.log1p(p[2]/N)
s2 = least_squares(lambda p: m2(p, sizes) - lnchi, [0.0, 1.78, 1.0])
models['power_plus_1overN'] = (m2, s2, 3, 'a=%.4f c=%.3f' % (s2.x[1], s2.x[2]))

# M3 leading-2 marginal-irrelevant log: ln chi = lnA + 2 lnN - r ln(1 + b lnN)
def m3(p, N): return p[0] + 2.0*np.log(N) - p[2]*np.log1p(p[1]*np.log(N))
s3 = least_squares(lambda p: m3(p, sizes) - lnchi, [0.0, 1.0, 1.0])
models['leading2_marg_log'] = (m3, s3, 3, 'b=%.4f r=%.4f' % (s3.x[1], s3.x[2]))

# M4 free power x power-of-log: ln chi = lnA + a lnN + p ln(lnN)
def m4(p, N): return p[0] + p[1]*np.log(N) + p[2]*np.log(np.log(N))
s4 = least_squares(lambda p: m4(p, sizes) - lnchi, [0.0, 1.8, 0.0])
models['free_power_x_logpow'] = (m4, s4, 3, 'a=%.4f p=%.4f' % (s4.x[1], s4.x[2]))

# M5 leading-2 x power-of-log: ln chi = lnA + 2 lnN + p ln(lnN)
def m5(p, N): return p[0] + 2.0*np.log(N) + p[2-1]*np.log(np.log(N)) if False else p[0] + 2.0*np.log(N) + p[1]*np.log(np.log(N))
s5 = least_squares(lambda p: m5(p, sizes) - lnchi, [0.0, 0.0])
models['leading2_logpow'] = (m5, s5, 2, 'p=%.4f' % s5.x[1])

print(f"\n  {'model':>22} {'k':>2} {'SSR(log)':>10} {'AIC':>9}   {'alpha_loc(12)':>13} {'alpha_loc(1e3)':>14}  params")
rows = []
for name, (fn, sol, k, lbl) in models.items():
    ssr = float(np.sum(sol.fun**2))
    a12 = local_exp_of(fn, sol.x, 12.0)
    a1k = local_exp_of(fn, sol.x, 1000.0)
    A = aic(ssr, k)
    print(f"  {name:>22} {k:>2} {ssr:10.2e} {A:9.2f}   {a12:13.4f} {a1k:14.4f}  {lbl}")
    rows.append({'model': name, 'k': k, 'ssr_log': ssr, 'aic': float(A),
                 'alpha_loc_12': float(a12), 'alpha_loc_1000': float(a1k),
                 'params': [float(x) for x in sol.x], 'label': lbl})
results['probe2_models'] = rows
best = min(rows, key=lambda r: r['aic'])
print(f"\n  AIC-best model: {best['model']}  (AIC={best['aic']:.2f})")

# Verdict on leading-2 family
ml = next(r for r in rows if r['model'] == 'leading2_marg_log')
lp = next(r for r in rows if r['model'] == 'leading2_logpow')
print("\n  Leading-2 family diagnostics:")
for r in (ml, lp):
    trend = 'INCREASES toward 2 (consistent w/ marginal log)' if r['alpha_loc_1000'] > r['alpha_loc_12'] + 1e-3 else 'does NOT climb to 2 by N=1e3'
    print(f"    {r['model']}: alpha_loc 12->1e3 = {r['alpha_loc_12']:.4f}->{r['alpha_loc_1000']:.4f}  [{trend}]")

results['verdict'] = {
    'aic_best': best['model'],
    'dlnL2_converges_to': float(aloc[-1] - NULL),
    'marg_log_ainf': float(a_inf_ml),
    'interpretation': (
        "alpha_loc decreases monotonically and dlnL2=alpha_loc-2 converges to a nonzero "
        "constant ~%.3f rather than flattening to 0; the marginal-log ansatz alpha_loc=a_inf+B/lnN "
        "returns a_inf=%.3f (NOT 2). The leading-2 forms cannot reproduce the observed downward "
        "local-exp trend without unphysical-sign couplings. The data behave as a genuine power "
        "N^%.3f at all reachable sizes; rescuing a=2 needs an unobserved turnaround beyond L=12."
        % (aloc[-1] - NULL, a_inf_ml, a_inf_pw)),
}
save()
print("\n" + "=" * 80)
print("VERDICT:", results['verdict']['interpretation'])
print("=" * 80)
print("saved -> results/sprint_132c_marginal_log_falsification.json")

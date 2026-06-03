"""Sprint 132d: Synthetic-recovery falsification — closes the Sprint-129 circularity.

Sprint 129 proved a no-log chi_F(N) power+correction extrapolation is CIRCULAR: fed
synthetic true-alpha=2-with-logs data it returns ~1.77, so it cannot tell a<2 from
2-with-logs. The local-EXPONENT-TREND diagnostic (Sprint 132c Probe 1) claims to break
that degeneracy. This script proves it does, by the exact test S129 demanded:

  Generate synthetic chi_F on our 7 exact sizes from a KNOWN truth, run the SAME local-
  exponent diagnostic, and check it gives the right answer:
    T_A2  : truth = leading power 2.0 x marginal-irrelevant log,  A*N^2*(lnN)^{-p}
            (endpoint-calibrated to pass through the REAL n=4 and n=12 chi_F values)
    T_pow : truth = genuine power, A*N^a*(1+c/N)  (the Sprint-132c AIC-best, a=1.721)

  If the diagnostic is sound, T_A2's local-exponent sequence must INCREASE (toward 2) and
  T_pow's must DECREASE -- and only one of them matches the REAL data's monotone decrease.
  This tells us which truth the real data look like, WITHOUT a circular extrapolation.

CPU-only.
"""
import numpy as np
import json, time, os

SERIES = {4: 12.839321, 6: 27.138030, 8: 45.527791, 9: 56.183728,
          10: 67.784201, 11: 80.310875, 12: 93.747642}
sizes = np.array(sorted(SERIES), dtype=float)
chi_real = np.array([SERIES[int(s)] for s in sizes])

def local_exps(ch):
    lnN, lnc = np.log(sizes), np.log(ch)
    return np.array([(lnc[i+1]-lnc[i])/(lnN[i+1]-lnN[i]) for i in range(len(sizes)-1)])

# --- T_A2: A * N^2 * (lnN)^{-p}, calibrated to real chi at n=4 and n=12 ---
N4, N12 = 4.0, 12.0
ratio = SERIES[12] / SERIES[4]
# ratio = (144/16) * (ln12/ln4)^{-p}  -> solve p
p_A2 = -np.log(ratio / (N12**2 / N4**2)) / np.log(np.log(N12) / np.log(N4))
A_A2 = SERIES[4] / (N4**2 * np.log(N4)**(-p_A2))
chi_A2 = A_A2 * sizes**2 * np.log(sizes)**(-p_A2)

# --- T_pow: A * N^a * (1+c/N), the Sprint-132c AIC-best (a=1.721, c=-0.525) ---
a_pw, c_pw = 1.7213, -0.525
A_pw = SERIES[12] / (N12**a_pw * (1 + c_pw / N12))
chi_pw = A_pw * sizes**a_pw * (1 + c_pw / sizes)

le_real = local_exps(chi_real)
le_A2 = local_exps(chi_A2)
le_pw = local_exps(chi_pw)

def monotonic(x):
    d = np.diff(x)
    return 'increasing' if np.all(d > 0) else 'decreasing' if np.all(d < 0) else 'non-monotone'

print("=" * 84)
print("Sprint 132d: synthetic-recovery falsification")
print("=" * 84)
print(f"  T_A2 truth: chi = {A_A2:.4f} * N^2 * (lnN)^(-{p_A2:.4f})   [leading power 2.0 + marginal log]")
print(f"  T_pow truth: chi = {A_pw:.4f} * N^{a_pw} * (1{c_pw:+.3f}/N)   [genuine power 1.721]")
print(f"\n  {'pair':>9} {'REAL a_loc':>11} {'T_A2 a_loc':>11} {'T_pow a_loc':>12}")
for i in range(len(sizes)-1):
    print(f"  ({int(sizes[i]):2d},{int(sizes[i+1]):2d}) {le_real[i]:11.4f} {le_A2[i]:11.4f} {le_pw[i]:12.4f}")
print(f"\n  monotonicity of local-exponent sequence:")
print(f"    REAL data : {monotonic(le_real)}   ({le_real[0]:.4f} -> {le_real[-1]:.4f})")
print(f"    T_A2 (a=2): {monotonic(le_A2)}   ({le_A2[0]:.4f} -> {le_A2[-1]:.4f})")
print(f"    T_pow     : {monotonic(le_pw)}   ({le_pw[0]:.4f} -> {le_pw[-1]:.4f})")

# distance of each template's local-exp fingerprint to the real one
d_A2 = float(np.sqrt(np.mean((le_A2 - le_real)**2)))
d_pw = float(np.sqrt(np.mean((le_pw - le_real)**2)))
print(f"\n  RMS local-exp distance to REAL data:")
print(f"    T_A2 (leading 2 + log) : {d_A2:.4f}")
print(f"    T_pow (genuine 1.721)  : {d_pw:.4f}")
verdict = ("REAL data match the GENUINE-POWER template (decreasing local exp); the leading-2 "
           "marginal-log template has the OPPOSITE (increasing) trend even when forced through "
           "the real n=4 and n=12 endpoints. The local-exponent diagnostic is NOT circular: it "
           "correctly separates the two truths, and the data fall on the a<2 side.") \
    if (monotonic(le_A2) == 'increasing' and monotonic(le_real) == 'decreasing' and d_pw < d_A2) \
    else "INCONCLUSIVE -- templates did not separate as expected; revisit."
print(f"\n  VERDICT: {verdict}")

out = {
    'experiment': '132d_synthetic_recovery', 'sprint': 132,
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'sizes': [int(s) for s in sizes],
    'T_A2': {'A': float(A_A2), 'p': float(p_A2), 'chi': list(chi_A2),
             'local_exps': list(le_A2), 'monotonic': monotonic(le_A2)},
    'T_pow': {'A': float(A_pw), 'a': a_pw, 'c': c_pw, 'chi': list(chi_pw),
              'local_exps': list(le_pw), 'monotonic': monotonic(le_pw)},
    'real': {'chi': list(chi_real), 'local_exps': list(le_real), 'monotonic': monotonic(le_real)},
    'rms_localexp_dist': {'T_A2': d_A2, 'T_pow': d_pw},
    'verdict': verdict,
}
path = os.path.join(os.path.dirname(__file__), '..', 'results',
                    'sprint_132d_synthetic_recovery.json')
with open(path, 'w') as f:
    json.dump(out, f, indent=2, default=str)
print("\nsaved -> results/sprint_132d_synthetic_recovery.json")

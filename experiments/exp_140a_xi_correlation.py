"""Sprint 140a: DIRECT measurement of the quantum chain's spatial correlation length xi_x
on the disordered branch at the transition (q=10, g_c = 1/q) -- the discriminator between
H_A (xi_x ~ xi_d^cl = 10.56 => amplitude-factor duality, sigma = 1/(4 xi_x)) and
H_B (xi_x ~ 2 xi_d^cl = 21.1 => naive duality with the quantum length, sigma = 1/(2 xi_x)).

Method: Z_q-conserving DMRG ground state (charge-0) on an OPEN chain, initialized from the
field-aligned product state (the g->inf disordered state) so DMRG converges onto the
DISORDERED branch despite the ordered-tower near-degeneracy at g ~ g_c. Correlator
C(r) = <Z1_i Z1d_{i+r}> over the bulk window (i = n/4, r <= n/2). Fits over r in [4, r_max]:
  pure exponential:  ln C = a - r/xi
  Ornstein-Zernike:  ln C = a - r/xi - 0.5 ln r     (correct 2D massive asymptotics)

Usage:  python exp_140a_xi_correlation.py [n1 n2 ...]    (default 48 64)
Writes results/sprint_140a_xi_q10.json; DB: xi_x_disordered (per n, at g_c) + g-robustness.
"""
import numpy as np
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zq_dmrg_utils import dmrg_state
from db_utils import record

q = 10
g_c = 1.0 / q
XI_CL = 10.56
CHI = 64
sizes = [int(x) for x in sys.argv[1:]] or [48, 64]
GS = [g_c, 0.103, 0.106]                      # g_c + robustness points
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_140a_xi_q10.json')

res = {'experiment': '140a_xi_q10', 'sprint': 140, 'q': q, 'g_c': g_c, 'chi': CHI,
       'xi_classical': XI_CL, 'runs': []}


def fits(rs, cs):
    rs = np.asarray(rs, float); cs = np.asarray(cs, float)
    keep = cs > 1e-12
    rs, cs = rs[keep], cs[keep]
    ln = np.log(cs)
    pe = np.polyfit(rs, ln, 1)                                    # pure exp
    xi_pe = -1.0 / pe[0]
    oz = np.polyfit(rs, ln + 0.5 * np.log(rs), 1)                 # OZ-corrected
    xi_oz = -1.0 / oz[0]
    # local xi(r) drift as a systematic check
    loc = [(-(np.log(cs[i + 1] / cs[i])) / (rs[i + 1] - rs[i])) ** -1
           for i in range(len(rs) - 1)]
    return float(xi_pe), float(xi_oz), [float(x) for x in loc]


print("=" * 80)
print(f"Sprint 140a: xi_x (disordered branch) q={q} at g_c={g_c} -- H_A: ~{XI_CL}, H_B: ~{2*XI_CL:.1f}")
print("=" * 80)
for n in sizes:
    for g in GS:
        t0 = time.time()
        E, psi, cu = dmrg_state(n, q, g, CHI)
        i0 = n // 4
        rmax = n // 2
        js = list(range(i0 + 2, i0 + rmax + 1))
        C = psi.correlation_function('Z1', 'Z1d', sites1=[i0], sites2=js)[0]
        rs = np.array(js) - i0
        # fit window: skip r<4 (short-distance), drop the last 2 points (boundary)
        win = (rs >= 4) & (rs <= rmax - 2)
        xi_pe, xi_oz, loc = fits(rs[win], np.real(C[win]))
        dt = time.time() - t0
        run = {'n': n, 'g': g, 'E0': E, 'chi_used': cu, 'r': rs.tolist(),
               'C': [float(np.real(c)) for c in C], 'xi_pure_exp': xi_pe, 'xi_OZ': xi_oz,
               'xi_local_drift': loc, 'time_s': round(dt, 1)}
        res['runs'].append(run)
        print(f"  n={n} g={g:.3f}:  xi_pure={xi_pe:.2f}  xi_OZ={xi_oz:.2f}  "
              f"(local drift {loc[0]:.1f}->{loc[-1]:.1f})  [chi {cu}, {dt:.0f}s]", flush=True)
        if abs(g - g_c) < 1e-9:
            record(sprint=140, model='sq_potts', q=q, n=n, quantity='xi_x_disordered',
                   value=xi_oz, error=abs(xi_oz - xi_pe), method='dmrg_corr_OZ_open_charge0',
                   notes=f'at exact g_c={g_c}; pure-exp {xi_pe:.2f}; xi_cl={XI_CL}; '
                         f'H_A~{XI_CL} vs H_B~{2*XI_CL:.1f}')
        res['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(OUT, 'w') as f:
            json.dump(res, f, indent=2)
print("DONE ->", OUT)

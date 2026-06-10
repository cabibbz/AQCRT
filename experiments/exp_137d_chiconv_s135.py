"""Sprint 137d: S135 rigor closure (audit item) -- chi-doubling check of the n=24 on-peak
open-BC DMRG chi_F that the S135 marginal-log fit leans on.

S135 production ran AT the chi=48 cap for every size with convergence verified only at
n=12. Here: recompute the canonical central chi_F at the RECORDED peak g* (DB gstar_open,
sprint 135) for q=4 and q=3 at n=24 with chi=96 / svd_min=1e-9 and compare against the
recorded chi_F_open_peak. PASS if |delta| < 0.1% (the S135 exponents move by <<1 sigma).

Usage:  python exp_137d_chiconv_s135.py     (writes results/sprint_137d_chiconv_s135.json)
"""
import numpy as np
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import warnings; warnings.filterwarnings('ignore')
from db_utils import query, record

from tenpy.models.model import CouplingMPOModel, NearestNeighborModel
from tenpy.networks.site import Site
from tenpy.linalg import np_conserved as npc
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg

N = 24
CHI = 96
SVD = 1e-9
DG = 1e-3
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_137d_chiconv_s135.json')


class SqPottsSite(Site):                      # = exp_135a (trivial leg, real ops)
    def __init__(self, q_val):
        leg = npc.LegCharge.from_trivial(q_val)
        Site.__init__(self, leg, [str(a) for a in range(q_val)], sort_charge=False)
        for a in range(q_val):
            P = np.zeros((q_val, q_val)); P[a, a] = 1.0
            self.add_op(f'P{a}', P)
        self.add_op('SqField', np.ones((q_val, q_val)) - np.eye(q_val), hc='SqField')


def make_chain(q):
    class SqPottsChain(CouplingMPOModel, NearestNeighborModel):
        def init_sites(self, mp): return SqPottsSite(mp.get('q', q))
        def init_terms(self, mp):
            J = mp.get('J', 1.0); g = mp.get('g', 0.25); qv = mp.get('q', q)
            for a in range(qv): self.add_coupling(-J, 0, f'P{a}', 0, f'P{a}', 1)
            self.add_onsite(-g, 0, 'SqField')
    return SqPottsChain


def gs(q, g, chi, init=None):
    model = make_chain(q)({'L': N, 'q': q, 'J': 1.0, 'g': g, 'bc_MPS': 'finite'})
    if init is None:
        np.random.seed(7 + N)
        psi = MPS.from_product_state(model.lat.mps_sites(),
                                     [int(np.random.randint(q)) for _ in range(N)], bc='finite')
    else:
        psi = init.copy()
    eng = dmrg.TwoSiteDMRGEngine(psi, model, {
        'mixer': True, 'max_E_err': 1e-11, 'max_S_err': 1e-8,
        'trunc_params': {'chi_max': chi, 'svd_min': SVD},
        'min_sweeps': 2, 'max_sweeps': 30})
    eng.run()
    psi.canonical_form()
    return psi


def chi_central(q, g, chi):
    p0 = gs(q, g, chi)
    pp = gs(q, g + DG, chi, init=p0)
    pm = gs(q, g - DG, chi, init=p0)
    Fp = abs(p0.overlap(pp))**2; Fm = abs(p0.overlap(pm))**2
    return (2.0 - Fp - Fm) / (DG**2 * N), int(max(p0.chi))


res = {'experiment': '137d_chiconv_s135', 'sprint': 137, 'n': N, 'chi': CHI,
       'svd_min': SVD, 'dg': DG, 'cases': {}}
print("=" * 78)
print(f"Sprint 137d: S135 chi-doubling check, n={N}, chi 48 -> {CHI}, svd_min={SVD}")
print("=" * 78)
ok_all = True
for q in [3, 4]:
    g135 = {r[4]: r[6] for r in query(quantity='gstar_open', q=q) if r[1] == 135}.get(N)
    c135 = {r[4]: r[6] for r in query(quantity='chi_F_open_peak', q=q) if r[1] == 135}.get(N)
    if g135 is None or c135 is None:
        print(f"  q={q}: S135 n={N} rows not found -- skip"); continue
    t0 = time.time()
    c_new, cu = chi_central(q, g135, CHI)
    dt = time.time() - t0
    rel = abs(c_new - c135) / c135
    ok = rel < 1e-3
    ok_all &= ok
    res['cases'][q] = {'g_star_s135': g135, 'chi_F_s135_chi48': c135,
                       'chi_F_chi96': float(c_new), 'rel_diff': float(rel),
                       'chi_used': cu, 'time_s': round(dt, 1), 'pass': bool(ok)}
    print(f"  q={q} n={N} g*={g135:.5f}:  chi48={c135:.5f}  chi96={c_new:.5f}  "
          f"rel={rel:.2e}  [{dt:.0f}s]  {'PASS (<0.1%)' if ok else '*** MOVED >0.1% ***'}")
    record(sprint=137, model='sq_potts', q=q, n=N, quantity='chi_F_open_peak_chi96',
           value=float(c_new), error=None, method='dmrg_canonical_at_s135_peak_chi96',
           notes=f'chi-doubling check of S135 chi48 value {c135:.5f}; rel={rel:.2e}')

res['all_pass'] = ok_all
res['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
with open(OUT, 'w') as f:
    json.dump(res, f, indent=2)
print(f"\n{'ALL PASS -- S135 chi=48 values are converged' if ok_all else '*** S135 chi convergence FAILS -- flag the S135 fit ***'}")
print("DONE ->", OUT)
sys.exit(0 if ok_all else 1)

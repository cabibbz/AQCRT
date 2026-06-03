"""Sprint 135 timing probe v2: REAL-dtype S_q Potts DMRG + chi/entropy/convergence diagnostics."""
import numpy as np, time, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import warnings; warnings.filterwarnings('ignore')
def log(m): print(m, flush=True)

q = 4
from tenpy.models.model import CouplingMPOModel, NearestNeighborModel
from tenpy.networks.site import Site
from tenpy.linalg import np_conserved as npc
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg

class SqPottsSite(Site):
    def __init__(self, q_val):
        leg = npc.LegCharge.from_trivial(q_val)
        Site.__init__(self, leg, [str(a) for a in range(q_val)], sort_charge=False)
        for a in range(q_val):
            P = np.zeros((q_val, q_val)); P[a, a] = 1.0          # REAL
            self.add_op(f'P{a}', P)
        Sq = np.ones((q_val, q_val)) - np.eye(q_val)             # REAL symmetric
        self.add_op('SqField', Sq, hc='SqField')

class SqPottsChain(CouplingMPOModel, NearestNeighborModel):
    def init_sites(self, mp): return SqPottsSite(mp.get('q', 4))
    def init_terms(self, mp):
        J = mp.get('J', 1.0); g = mp.get('g', 0.25); qv = mp.get('q', 4)
        for a in range(qv): self.add_coupling(-J, 0, f'P{a}', 0, f'P{a}', 1)
        self.add_onsite(-g, 0, 'SqField')

def gs(n, g, chi_max, init=None, mE=1e-10, mS=1e-7, maxsw=30, minsw=2):
    model = SqPottsChain({'L': n, 'q': q, 'J': 1.0, 'g': g, 'bc_MPS': 'finite'})
    if init is None:
        np.random.seed(7 + n)
        psi = MPS.from_product_state(model.lat.mps_sites(), [int(np.random.randint(q)) for _ in range(n)], bc='finite')
    else:
        psi = init.copy()
    eng = dmrg.TwoSiteDMRGEngine(psi, model, {'mixer': True, 'max_E_err': mE, 'max_S_err': mS,
        'trunc_params': {'chi_max': chi_max, 'svd_min': 1e-12}, 'min_sweeps': minsw, 'max_sweeps': maxsw})
    E0, _ = eng.run()
    S = psi.entanglement_entropy()
    return float(E0), psi, max(psi.chi), float(np.max(S))

log("=== REAL dtype: cold solve at peak-side g=0.22 ===")
for n, cm in [(10, 64), (16, 96), (24, 128)]:
    t = time.time(); E, psi, cu, S = gs(n, 0.22, cm); dt = time.time() - t
    log(f"  n={n:2d} chi_max={cm}: t={dt:.2f}s chi_used={cu} S_max={S:.3f} E/n={E/n:.6f}")

log("\n=== chi sensitivity at n=16, g=0.22 (energy + state convergence vs chi) ===")
ref = None
for cm in [32, 48, 64, 96, 160]:
    t = time.time(); E, psi, cu, S = gs(16, 0.22, cm); dt = time.time() - t
    tag = ""
    if ref is not None:
        ov = abs(psi.overlap(ref)) ** 2
        tag = f"  |<psi|psi_prevchi>|^2={ov:.8f}  dE/n={(E-refE)/16:.2e}"
    log(f"  chi_max={cm:3d}: t={dt:.2f}s chi_used={cu} S_max={S:.3f} E/n={E/16:.8f}{tag}")
    ref, refE = psi, E

log("\n=== warm-start partner cost + overlap noise (n=16, chi=96) ===")
E, psi, cu, S = gs(16, 0.22, 96)
for dg in [1e-3, 1e-2]:
    t = time.time(); E2, psi2, cu2, S2 = gs(16, 0.22 + dg, 96, init=psi, minsw=2); dt = time.time() - t
    Fp = abs(psi.overlap(psi2)) ** 2
    t2 = time.time(); E3, psi3, _, _ = gs(16, 0.22 - dg, 96, init=psi, minsw=2); dt2 = time.time() - t2
    Fm = abs(psi.overlap(psi3)) ** 2
    chiF = (2 - Fp - Fm) / (dg ** 2 * 16)
    log(f"  dg={dg:.0e}: warm t+={dt:.2f}/{dt2:.2f}s  1-Fp={1-Fp:.3e} 1-Fm={1-Fm:.3e}  chi_F/site={chiF:.5f}")
log("\nDONE")

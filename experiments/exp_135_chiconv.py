"""Sprint 135 chi-convergence: lock DMRG chi_max for the on-peak chi_F. At n=12 (largest exact-
checkable), fix g* to the S134 exact peak and compute DMRG central chi_F vs chi_max; compare to exact.
Goal: smallest chi where chi_F matches exact to <0.1% AND is stable (so the EXPONENT is unbiased)."""
import numpy as np, time, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import warnings; warnings.filterwarnings('ignore')
from db_utils import query
def log(m): print(m, flush=True)

q = 4; g_c = 0.25; DG = 1e-3; n = 12
# S134 exact open peak location:
gstar = {r[4]: r[6] for r in query(quantity='gstar_open', q=q) if r[1] == 134}.get(12, 0.223042)
log(f"n={n}  g*(S134 exact)={gstar:.6f}")

from tenpy.models.model import CouplingMPOModel, NearestNeighborModel
from tenpy.networks.site import Site
from tenpy.linalg import np_conserved as npc
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg

class SqSite(Site):
    def __init__(self, qv):
        Site.__init__(self, npc.LegCharge.from_trivial(qv), [str(a) for a in range(qv)], sort_charge=False)
        for a in range(qv):
            P = np.zeros((qv, qv)); P[a, a] = 1.0; self.add_op(f'P{a}', P)
        self.add_op('SqField', np.ones((qv, qv)) - np.eye(qv), hc='SqField')
class SqChain(CouplingMPOModel, NearestNeighborModel):
    def init_sites(self, mp): return SqSite(mp.get('q', q))
    def init_terms(self, mp):
        for a in range(mp.get('q', q)): self.add_coupling(-1.0, 0, f'P{a}', 0, f'P{a}', 1)
        self.add_onsite(-mp.get('g', g_c), 0, 'SqField')

def gs(g, chi_max, svd_min, init=None):
    model = SqChain({'L': n, 'q': q, 'J': 1.0, 'g': g, 'bc_MPS': 'finite'})
    if init is None:
        np.random.seed(7 + n)
        psi = MPS.from_product_state(model.lat.mps_sites(), [int(np.random.randint(q)) for _ in range(n)], bc='finite')
    else:
        psi = init.copy()
    eng = dmrg.TwoSiteDMRGEngine(psi, model, {'mixer': True, 'max_E_err': 1e-11, 'max_S_err': 1e-8,
        'trunc_params': {'chi_max': chi_max, 'svd_min': svd_min}, 'min_sweeps': 2, 'max_sweeps': 24})
    E0, _ = eng.run(); psi.canonical_form()
    return psi, max(psi.chi)

def dmrg_chi(chi_max, svd_min):
    p0, c0 = gs(gstar, chi_max, svd_min)
    pp, cp = gs(gstar + DG, chi_max, svd_min, init=p0)
    pm, cm = gs(gstar - DG, chi_max, svd_min, init=p0)
    Fp = abs(p0.overlap(pp)) ** 2; Fm = abs(p0.overlap(pm)) ** 2
    return (2 - Fp - Fm) / (DG ** 2 * n), max(c0, cp, cm)

# exact reference at same g*, dg
from scipy.sparse import csr_matrix
from hamiltonian_utils import _decode_states, _build_field
from gpu_utils import eigsh
dim, all_idx, digits, powers = _decode_states(n, q)
diag = np.zeros(dim)
for s in range(n - 1): diag -= (digits[:, s] == digits[:, s + 1]).astype(float)
Hc = csr_matrix((diag, (all_idx, all_idx)), shape=(dim, dim))
Hf = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
def exact_chi(dg):
    def g(gg):
        _, v = eigsh(Hc + gg * Hf, k=1, which='SA'); return np.ascontiguousarray(v[:, 0])
    p0, pp, pm = g(gstar), g(gstar + dg), g(gstar - dg)
    if np.dot(p0, pp) < 0: pp = -pp
    if np.dot(p0, pm) < 0: pm = -pm
    return (2 - float(np.dot(p0, pp)**2) - float(np.dot(p0, pm)**2)) / (dg**2 * n)
ex3 = exact_chi(DG); ex4 = exact_chi(1e-4)
log(f"EXACT chi_F(g*): dg=1e-3 -> {ex3:.5f}   dg=1e-4 -> {ex4:.5f}   (S134 DB=70.5847)")
log(f"\n{'chi_max':>8} {'svd_min':>8} {'chi_used':>9} {'chi_F':>10} {'DMRG/exact_dg3':>16} {'t(s)':>6}")
for chi_max, svd in [(48, 1e-8), (64, 1e-8), (64, 1e-9), (96, 1e-9), (128, 1e-10)]:
    t = time.time(); c, cu = dmrg_chi(chi_max, svd); dt = time.time() - t
    log(f"{chi_max:>8} {svd:>8.0e} {cu:>9} {c:>10.5f} {c/ex3:>16.6f} {dt:>6.1f}")
log("\nDONE")

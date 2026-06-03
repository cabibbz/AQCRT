"""Sprint 135 timing probe: isolate DMRG vs exact-diag cost. Flushed streaming prints."""
import numpy as np, time, sys, os
sys.path.insert(0, os.path.dirname(__file__))
def log(m): print(m, flush=True)

q = 4
from tenpy.models.model import CouplingMPOModel, NearestNeighborModel
from tenpy.networks.site import Site
from tenpy.linalg import np_conserved as npc
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg
import warnings; warnings.filterwarnings('ignore')

class SqPottsSite(Site):
    def __init__(self, q_val):
        leg = npc.LegCharge.from_trivial(q_val)
        Site.__init__(self, leg, [str(a) for a in range(q_val)], sort_charge=False)
        for a in range(q_val):
            P = np.zeros((q_val, q_val), dtype=complex); P[a, a] = 1.0
            self.add_op(f'P{a}', P)
        Sq = np.ones((q_val, q_val), dtype=complex) - np.eye(q_val, dtype=complex)
        self.add_op('SqField', Sq, hc='SqField')

class SqPottsChain(CouplingMPOModel, NearestNeighborModel):
    def init_sites(self, mp): return SqPottsSite(mp.get('q', 4))
    def init_terms(self, mp):
        J = mp.get('J', 1.0); g = mp.get('g', 0.25); qv = mp.get('q', 4)
        for a in range(qv): self.add_coupling(-J, 0, f'P{a}', 0, f'P{a}', 1)
        self.add_onsite(-g, 0, 'SqField')

def dmrg_gs(n, g, chi_max, init_psi=None, max_sweeps=30, min_sweeps=2, max_E_err=1e-12, max_S_err=1e-8):
    model = SqPottsChain({'L': n, 'q': q, 'J': 1.0, 'g': g, 'bc_MPS': 'finite'})
    if init_psi is None:
        np.random.seed(123 + n)
        psi = MPS.from_product_state(model.lat.mps_sites(), [int(np.random.randint(q)) for _ in range(n)], bc='finite')
    else:
        psi = init_psi.copy()
    eng = dmrg.TwoSiteDMRGEngine(psi, model, {
        'mixer': True, 'max_E_err': max_E_err, 'max_S_err': max_S_err,
        'trunc_params': {'chi_max': chi_max, 'svd_min': 1e-14},
        'min_sweeps': min_sweeps, 'max_sweeps': max_sweeps})
    E0, _ = eng.run()
    return float(E0), psi, eng.sweeps if hasattr(eng, 'sweeps') else -1

g_c = 0.25
log("=== DMRG cold ground state, near peak g=0.22 ===")
for n, cm in [(10, 96), (20, 128), (40, 240)]:
    t = time.time(); E, psi, sw = dmrg_gs(n, 0.22, cm); dt = time.time() - t
    log(f"  n={n:2d} chi_max={cm}: t={dt:.2f}s  sweeps={sw}  chi_used={max(psi.chi)}  E/n={E/n:.6f}")

log("\n=== warm-start partner (g+dg from psi(g)) at n=20 ===")
E, psi, sw = dmrg_gs(20, 0.22, 128)
t = time.time(); E2, psi2, sw2 = dmrg_gs(20, 0.221, 128, init_psi=psi, min_sweeps=2); dt = time.time() - t
ov = abs(psi.overlap(psi2)) ** 2
log(f"  warm partner: t={dt:.2f}s sweeps={sw2}  |<psi|psi2>|^2={ov:.10f}  1-F={1-ov:.3e}")

log("\n=== exact eigsh solve cost (validation path) ===")
from scipy.sparse import csr_matrix
from hamiltonian_utils import _decode_states, _build_field
def build_parts_exact(n):
    dim, all_idx, digits, powers = _decode_states(n, q)
    diag = np.zeros(dim)
    for s in range(n - 1): diag -= (digits[:, s] == digits[:, s + 1]).astype(float)
    Hc = csr_matrix((diag, (all_idx, all_idx)), shape=(dim, dim))
    Hf = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
    return Hc, Hf
from gpu_utils import eigsh, gpu_status
log(f"  {gpu_status()}")
for n in [8, 10]:
    Hc, Hf = build_parts_exact(n); H = Hc + 0.22 * Hf
    t = time.time(); ev, _ = eigsh(H, k=1, which='SA'); dt = time.time() - t
    log(f"  exact n={n:2d} dim={q**n:>9,}: 1 solve t={dt:.2f}s  E0={ev[0]:.6f}")
log("\nDONE")

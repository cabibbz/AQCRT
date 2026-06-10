"""Z_q-charge-conserving DMRG for the S_q Potts chain (Sprint 137).

Works in the FOURIER (charge) basis |m> = (1/sqrt q) sum_s omega^{ms} |s>, m=0..q-1:
  - global Z_q symmetry U = prod_i X_i acts as omega^{-sum m_i}  =>  conserved charge
    Q = sum_i m_i (mod q); TeNPy LegCharge('Zq' mod q).
  - field term is DIAGONAL:  sum_{k=1}^{q-1} X^k |m> = (q*delta_{m,0} - 1)|m>
  - coupling delta(s_i,s_j) = (1/q)[ 1 + sum_{k=1}^{q-1} Zk_i Zkd_j ]  where Zk raises the
    site charge by k (REAL permutation matrices => real-dtype DMRG, ~6x faster).

CONVENTION: the MPO drops the constant bond term -J(n-1)/q, so
    E_szbasis = E_mpo - J*(n-1)/q        (gaps are identical).

Charge-0 thermal gap: ground state from an all-m=0 product state; first excited level of the
SAME charge sector via DMRG option orthogonal_to=[psi0]. Both validated against open-BC exact
diagonalization (charge filter <v|P|v|>) in exp_137a before any production use.
"""
import numpy as np
import os, sys
import warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
warnings.filterwarnings('ignore', message='.*unit_cell_width.*')   # tenpy 1.1 deprecation noise

from tenpy.models.model import CouplingMPOModel
from tenpy.networks.site import Site
from tenpy.linalg import np_conserved as npc
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg


class ZqPottsSite(Site):
    """q-dim site in the Z_q-charge (Fourier) basis."""
    def __init__(self, q):
        chinfo = npc.ChargeInfo([q], ['Zq'])
        leg = npc.LegCharge.from_qflat(chinfo, [[m] for m in range(q)])
        Site.__init__(self, leg, [str(m) for m in range(q)], sort_charge=False)
        self.q = q
        F = np.diag([float(q) * (m == 0) - 1.0 for m in range(q)])
        self.add_op('Fdiag', F)                       # sum_{k>=1} X^k, diagonal here
        for k in range(1, q):
            Zk = np.zeros((q, q))
            for m in range(q):
                Zk[(m + k) % q, m] = 1.0
            self.add_op(f'Z{k}', Zk)                  # charge +k
            self.add_op(f'Z{k}d', Zk.T)               # charge -k


class ZqPottsChain(CouplingMPOModel):
    """H = -(J/q) sum_i sum_{k=1}^{q-1} Zk_i Zkd_{i+1}  - g sum_i Fdiag_i   (open chain).
    (= S_q Potts H up to the dropped constant -J(n-1)/q.)"""
    def init_sites(self, mp):
        return ZqPottsSite(mp.get('q', 5))

    def init_terms(self, mp):
        J = mp.get('J', 1.0)
        g = mp.get('g', 0.2)
        q = mp.get('q', 5)
        for k in range(1, q):
            self.add_coupling(-J / q, 0, f'Z{k}', 0, f'Z{k}d', 1)
        self.add_onsite(-g, 0, 'Fdiag')


def dmrg_state(n, q, g, chi_max, J=1.0, init=None, orthogonal_to=None,
               svd_min=1e-9, max_sweeps=40, min_sweeps=2):
    """One DMRG run in the charge-0 sector. Returns (E_mpo, psi, max_chi_used).
    init: MPS to warm-start from (copied), else all-m=0 product state."""
    model = ZqPottsChain({'L': n, 'q': q, 'J': J, 'g': g, 'bc_MPS': 'finite'})
    if init is None:
        psi = MPS.from_product_state(model.lat.mps_sites(), [0] * n, bc='finite')
    else:
        psi = init.copy()
    opts = {'mixer': True, 'max_E_err': 1e-11, 'max_S_err': 1e-8,
            'trunc_params': {'chi_max': chi_max, 'svd_min': svd_min},
            'min_sweeps': min_sweeps, 'max_sweeps': max_sweeps}
    if orthogonal_to and init is None:
        # seed differently from psi0 (all-0) or DMRG can stall in the orthogonal complement:
        # |1, q-1, 0, ...> has total charge q = 0 mod q
        state = [0] * n
        state[0], state[1] = 1, q - 1
        psi = MPS.from_product_state(model.lat.mps_sites(), state, bc='finite')
    # orthogonal_to is a KEYWORD-ONLY constructor arg in tenpy 1.1 (NOT an options key --
    # as an option it is silently ignored and the run reconverges to psi0)
    eng = dmrg.TwoSiteDMRGEngine(psi, model, opts,
                                 orthogonal_to=list(orthogonal_to) if orthogonal_to else None)
    E, _ = eng.run()
    psi.canonical_form()
    return float(E), psi, int(max(psi.chi))


def thermal_gap_charge0(n, q, g, chi_max, warm0=None, warm1=None, **kw):
    """(E0, E1, Delta, psi0, psi1, chi_used) of the two lowest charge-0 states at coupling g.
    E0/E1 are MPO-convention energies (constant offset cancels in Delta)."""
    E0, p0, c0 = dmrg_state(n, q, g, chi_max, init=warm0, **kw)
    E1, p1, c1 = dmrg_state(n, q, g, chi_max, init=warm1, orthogonal_to=[p0], **kw)
    if E1 < E0 - 1e-10:                               # orthogonal run found a lower state:
        raise RuntimeError(f"E1<E0 at g={g}: ground-state run not converged (E0={E0}, E1={E1})")
    return E0, E1, E1 - E0, p0, p1, max(c0, c1)


def mpo_to_szbasis(E_mpo, n, J=1.0, q=None):
    """Convert MPO energy to the s-basis convention (adds the dropped -J(n-1)/q)."""
    return E_mpo - J * (n - 1) / q

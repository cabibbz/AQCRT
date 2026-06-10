"""Thermal-gap exceptional-point (EP) estimator of 1/nu -- shared library.

Extracted from exp_136a/b (audit 2026-06-09) so the sprint-136 headline pipeline has
ONE implementation, importable by experiments AND by the golden gate (test_golden.py
section [5] anchors q=2 against frozen values).

Physics (validated S136 vs a true complex-symmetric diagonalization at q=2, ~2%):
  - thermal gap Delta_eps(g) = E1 - E0 within the Z_q-charge-0 sector of the PERIODIC
    S_q Potts chain (charge filter: P = prod_i X_i cyclic shift, keep <v|P|v> > 0.9 --
    an expectation filter, valid for q <= ~13 since the worst contaminant reads
    cos(2*pi/q) < 0.9; non-degenerate eigenvectors are automatically charge eigenstates).
  - near the gap minimum g*(L), a 2-level avoided crossing
        Delta(g) = sqrt(Delta_min^2 + v^2 (g - g*)^2)
    has curvature Delta'' = v^2/Delta_min at the minimum, so the nearest complex-g
    coalescence (EP / quantum Fisher zero) sits at
        Im(g_EP) = Delta_min / v = sqrt(Delta_min / Delta'').
  - continuous transitions: Im(g_EP) ~ L^{-1/nu}.
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.linalg import eigh as dense_eigh

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gpu_utils import eigsh
from hamiltonian_utils import _decode_states, _build_coupling, _build_field

DENSE_MAX = 1500          # dense eigh subset below this dim; sparse eigsh above


def free_gpu():
    try:
        import cupy as cp
        cp.get_default_memory_pool().free_all_blocks()
    except Exception:
        pass


def build_parts(n, q):
    """Periodic S_q Potts (Hc, Hf) plus the global cyclic-shift operator P = prod X_i."""
    dim, all_idx, digits, powers = _decode_states(n, q)
    H_coup = _build_coupling(all_idx, digits, n, dim)
    H_field = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
    new_idx = (((digits + 1) % q) * powers).sum(axis=1)
    P = csr_matrix((np.ones(dim), (new_idx, all_idx)), shape=(dim, dim))
    return H_coup, H_field, P


def lowest_states(H, dim, K):
    """K lowest (evals, evecs) of real-symmetric H, ascending. Dense subset for tiny
    dim; sparse eigsh (which='SA', large ncv+maxiter) above -- keep the scan window
    narrow and on the disordered side (near g_c) or Lanczos stalls (S136 lesson)."""
    if dim <= DENSE_MAX:
        evals, evecs = dense_eigh(H.toarray(), subset_by_index=[0, min(K, dim) - 1])
        return evals, evecs
    ncv = min(dim - 1, max(4 * K, 80))
    evals, evecs = eigsh(H, k=K, which='SA', ncv=ncv, maxiter=5000, tol=1e-9)
    order = np.argsort(evals)
    return evals[order], evecs[:, order]


def charge0_two_lowest(Hc, Hf, P, g, K):
    """(E0, E1) of the two lowest Z_q-charge-0 states at coupling g. ONE
    diagonalization (audit: the original exp_136b gap_curve diagonalized twice)."""
    dim = Hc.shape[0]
    evals, evecs = lowest_states(Hc + g * Hf, dim, K)
    chexp = np.einsum('ij,ij->j', evecs, (P @ evecs))     # <v|P|v>, real
    c0 = np.where(chexp > 0.9)[0]
    free_gpu()
    if len(c0) < 2:
        raise RuntimeError(f"only {len(c0)} charge-0 states in lowest {K} at g={g:.4f}")
    return evals[c0[0]], evals[c0[1]]


def gap_curve(Hc, Hf, P, gs, K):
    out = []
    for g in gs:
        e0, e1 = charge0_two_lowest(Hc, Hf, P, g, K)
        out.append(e1 - e0)
    return np.array(out)


def parab_min(gs, ys):
    """Vertex (g0, y(g0), y'') of the parabola through 3+ points."""
    a, b, c = np.polyfit(gs, ys, 2)
    g0 = -b / (2 * a)
    return g0, a * g0**2 + b * g0 + c, 2 * a


def im_gEP_estimate(q, n, lo, hi, K=None):
    """Deterministic real-axis EP estimate on a FIXED window [lo, hi] (used by the
    golden gate; production exp_136b plans its window adaptively). Coarse 9-point
    scan, 7-point fine grid around the interior minimum, 3-point parabola.
    Returns dict(g_star, gap_min, gap_curv, im_gEP). Raises if the minimum is not
    bracketed inside the window."""
    K = K if K is not None else 2 * q + 6
    Hc, Hf, P = build_parts(n, q)
    coarse = np.linspace(lo, hi, 9)
    cg = gap_curve(Hc, Hf, P, coarse, K)
    i = int(np.argmin(cg))
    if i in (0, len(coarse) - 1):
        raise RuntimeError(f"q={q} n={n}: gap minimum at window edge (i={i}); widen [lo,hi]")
    fine = np.linspace(coarse[i - 1], coarse[i + 1], 7)
    fg = gap_curve(Hc, Hf, P, fine, K)
    j = int(np.argmin(fg))
    if j in (0, len(fine) - 1):
        raise RuntimeError(f"q={q} n={n}: fine-grid minimum at edge (j={j})")
    g_star, gmin, gpp = parab_min(fine[j - 1:j + 2], fg[j - 1:j + 2])
    return {'g_star': float(g_star), 'gap_min': float(gmin),
            'gap_curv': float(gpp),
            'im_gEP': float(np.sqrt(gmin / gpp)) if gpp > 0 else float('nan')}

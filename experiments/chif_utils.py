"""Canonical fidelity-susceptibility (chi_F) convention + the derived scaling null.

THERE IS ONE canonical chi_F in this project. Document and use it from here so the
factor-2 / per-site confusion (Sprints 121-126) and the inverted-exponent framing
(Sprint 129 audit) cannot recur.

CANONICAL DEFINITION (per-site, "factor-2", central finite difference):

    chi_F(n) = (2 - |<psi0|psi+>|^2 - |<psi0|psi->|^2) / (dg^2 * n)

  evaluated at the self-dual critical point g_c = 1/q, with dg=1e-4 and
  psi+/psi-/psi0 the ground states at g_c +/- dg / g_c. Note:
    - the overlap is SQUARED  -> a built-in factor 2 vs the textbook chi_F = 2(1-F)/dg^2
    - the result is divided by n -> this is a PER-SITE (density) quantity

  Both are constant prefactors that CANCEL in the log-log scaling exponent, so the
  *exponent* is unaffected by them (verified Sprint 129). They DO matter for absolute
  magnitudes and for which literature exponent you compare to.

THE DERIVED NULL (read this before comparing to any exponent):

  The per-site chi_F density at a quantum critical point scales as
        chi_F / L^d  ~  L^{2/nu - d}            (Albuquerque, Alet, Sire, Capponi,
                                                 PRB 81, 064418 (2010), Eq. 21)
  With d=1 and the EXACT Potts correlation-length exponents:
        q=2 (nu=1)   -> 2/nu - d = 1.0
        q=3 (nu=5/6) -> 2/nu - d = 1.4   (= 7/5, the project's verified q=3 value)
        q=4 (nu=2/3) -> 2/nu - d = 2.0   <-- THE CORRECT q=4 EXPONENT, *not* a hypothesis
                                              to reject. A measured ~1.77 at n<=11 is the
                                              finite-size value below 2 (marginal-operator
                                              log), NOT evidence against 2. (Sprint 129.)

  Do NOT compare a per-site exponent to a *total*-quantity or *different-observable*
  literature value (e.g. the 2D-classical specific-heat log power p=3/2 is NOT a chi_F
  prediction). Use expected_persite_exponent(q) as the reference.
"""
import numpy as np

# Exact 2D Potts / 1+1D quantum correlation-length exponents (continuous cases q<=4).
# q>4 is weakly first-order ("walking") with no simple nu -> no closed-form null.
POTTS_NU = {2: 1.0, 3: 5.0 / 6.0, 4: 2.0 / 3.0}


def expected_persite_exponent(q, d=1):
    """Derived leading exponent of the per-site chi_F density: 2/nu - d.

    Returns the EXACT asymptotic target the measured per-site exponent should approach
    (q=2->1.0, q=3->1.4, q=4->2.0). Returns None for q>4 (walking, no simple nu)."""
    nu = POTTS_NU.get(q)
    return None if nu is None else 2.0 / nu - d


def chi_F_q2_closed_form(n):
    """Exact per-site chi_F of the q=2 (TFIM) critical chain in the canonical convention.

    Total chi_F = N(N-1)/8; canonical = 2 * total / n = (n-1)/4. Used as a golden anchor
    that simultaneously pins the factor-2, the per-site /n, and the absolute scale."""
    return (n - 1) / 4.0


def chi_F_exact(H_coup, H_field, g_c, n, dg=1e-4, eigsh=None):
    """Canonical exact chi_F (see module docstring). Reproduces the stored results.db
    `chi_F_exact` values to ~5 significant figures (dg=1e-4 carries a smooth ~1e-6 bias;
    the 6th stored decimal is below the noise floor)."""
    if eigsh is None:
        from gpu_utils import eigsh
    Hp = H_coup + (g_c + dg) * H_field
    Hm = H_coup + (g_c - dg) * H_field
    H0 = H_coup + g_c * H_field
    _, v0 = eigsh(H0, k=1, which='SA')
    _, vp = eigsh(Hp, k=1, which='SA')
    _, vm = eigsh(Hm, k=1, which='SA')
    psi0, psip, psim = v0[:, 0], vp[:, 0], vm[:, 0]
    if np.dot(psi0, psip) < 0:
        psip = -psip
    if np.dot(psi0, psim) < 0:
        psim = -psim
    ov_p = np.dot(psi0, psip) ** 2
    ov_m = np.dot(psi0, psim) ** 2
    return (2.0 - ov_p - ov_m) / (dg ** 2 * n)

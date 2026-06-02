"""FSS curve + data-collapse utilities for the per-site fidelity susceptibility.

Sprint 130. We scan chi_F(g, N) on a window placed in the FSS *scaling variable*
x = (g - g_c) * N^kappa0 (kappa0 = literature 1/nu), so every system size covers
the same physical region and the curves overlap when rescaled. From each curve we
read off three exponents and feed the full set into a one-parameter data collapse.

Why a fixed-x (scaling) window matters: the consecutive-overlap chi_F uses a finite
grid step h = dx * N^{-kappa0}, which scales exactly as the FSS width N^{-1/nu}.
The leading finite-h bias on chi_F is therefore an (approximately) N-INDEPENDENT
multiplicative factor -> it cancels in every *exponent* (height, at-g_c, collapse),
even though the absolute chi_F is offset from the h->0 value. We only ever quote
exponents, so this is harmless (verified on q=2: height exponent -> 1.0).

chi_F convention: per-site, overlap-squared (same as exp_127a / peak_utils):
    chi_F(mid) = (1 - <psi(g)|psi(g+h)>^2) / (h^2 * n).
Constant prefactors are irrelevant for exponents and for the collapse shape.

Usage:
    from collapse_utils import scan_curve, peak_from_curve, chi_at, collapse_scan
"""
import numpy as np
from gpu_utils import eigsh


def scan_curve(H_coup, H_field, n, gs):
    """Ground state on the g-grid; per-site chi_F at the midpoints.

    Returns (mids, chi) with len = len(gs) - 1. Uses overlap-squared so the
    eigenvector sign/phase is irrelevant. gs must be uniformly spaced.
    """
    gs = np.asarray(gs, float)
    vecs = []
    for g in gs:
        _, v = eigsh(H_coup + g * H_field, k=1, which='SA')
        vecs.append(v[:, 0])
    h = np.diff(gs)
    mids = 0.5 * (gs[:-1] + gs[1:])
    chi = np.empty(len(mids))
    for i in range(len(mids)):
        ov = float(np.dot(vecs[i], vecs[i + 1]))
        chi[i] = (1.0 - ov * ov) / (h[i] * h[i] * n)
    return mids, chi


def peak_from_curve(mids, chi):
    """Locate the chi_F maximum: grid argmax + parabolic vertex refinement.

    Returns dict {gstar, chi_peak, k, edge}. 'edge' True if the argmax is at a
    window boundary (peak not bracketed -> widen the window and rescan).
    """
    k = int(np.argmax(chi))
    edge = (k == 0 or k == len(chi) - 1)
    if edge:
        return {'gstar': float(mids[k]), 'chi_peak': float(chi[k]), 'k': k, 'edge': True}
    y0, y1, y2 = chi[k - 1], chi[k], chi[k + 1]
    denom = y0 - 2.0 * y1 + y2
    if denom >= 0:  # not concave -> fall back to grid point
        return {'gstar': float(mids[k]), 'chi_peak': float(chi[k]), 'k': k, 'edge': False}
    dx = mids[k + 1] - mids[k]
    delta = 0.5 * (y0 - y2) / denom
    gstar = mids[k] + delta * dx
    ystar = y1 - 0.125 * (y0 - y2) ** 2 / denom
    return {'gstar': float(gstar), 'chi_peak': float(ystar), 'k': k, 'edge': False}


def chi_at(mids, chi, g):
    """Linear-interpolate chi_F at coupling g (used to read the at-g_c value,
    g = g_c, directly off the same curve for comparison with prior sprints)."""
    return float(np.interp(g, mids, chi))


def _collapse_cost(curves, g_c, kappa, a):
    """Leave-one-size-out collapse residual (Houdayer-Hartmann / Bhattacharjee-
    Seno style). curves: list of dicts {n, mids, chi}.

    x' = (g - g_c) * n^kappa ;  y' = chi / n^a. For each point, predict y' by
    linear interpolation of the pooled points from the OTHER sizes, inside the
    common x'-overlap window. Cost = mean squared residual / Var(y'). Dimensionless
    (the /Var removes the trivial a->+-inf scale degeneracy). Lower = better.
    """
    xs, ys, sid = [], [], []
    for i, c in enumerate(curves):
        xp = (np.asarray(c['mids']) - g_c) * (c['n'] ** kappa)
        yp = np.asarray(c['chi']) / (c['n'] ** a)
        xs.append(xp); ys.append(yp); sid.append(np.full(len(xp), i))
    xs = np.concatenate(xs); ys = np.concatenate(ys); sid = np.concatenate(sid)
    # common overlap window across sizes
    los, his = [], []
    for i in range(len(curves)):
        xi = xs[sid == i]
        los.append(xi.min()); his.append(xi.max())
    lo, hi = max(los), min(his)
    if hi <= lo:
        return np.inf
    var = ys.var()
    if var <= 0:
        return np.inf
    sse, cnt = 0.0, 0
    for i in range(len(xs)):
        if xs[i] < lo or xs[i] > hi:
            continue
        m = sid != sid[i]
        xo, yo = xs[m], ys[m]
        order = np.argsort(xo)
        xo, yo = xo[order], yo[order]
        if xs[i] < xo[0] or xs[i] > xo[-1]:
            continue
        ypred = np.interp(xs[i], xo, yo)
        sse += (ys[i] - ypred) ** 2
        cnt += 1
    if cnt == 0:
        return np.inf
    return (sse / cnt) / var


def collapse_scan(curves, g_c, a, kappa_grid):
    """One-parameter collapse: fix the height exponent a, scan kappa (=1/nu).

    Returns dict with kappa_best, cost_min, a parabolic-vertex error estimate
    from the cost curve, and the full (kappa, cost) trace.
    """
    costs = np.array([_collapse_cost(curves, g_c, k, a) for k in kappa_grid])
    j = int(np.argmin(costs))
    kbest = float(kappa_grid[j])
    # parabolic refinement + width (curvature) error if we have interior minimum
    kerr = None
    kref = kbest
    if 0 < j < len(kappa_grid) - 1:
        y0, y1, y2 = costs[j - 1], costs[j], costs[j + 1]
        denom = y0 - 2 * y1 + y2
        if denom > 0:
            dk = kappa_grid[j + 1] - kappa_grid[j]
            kref = kbest + 0.5 * (y0 - y2) / denom * dk
            # width where cost rises by ~ its min (very rough scale)
            curv = denom / (dk * dk)
            kerr = float(np.sqrt(abs(y1) / curv)) if curv > 0 else None
    return {
        'kappa_best': kbest,
        'kappa_refined': float(kref),
        'cost_min': float(costs[j]),
        'kappa_err': kerr,
        'grid': [float(k) for k in kappa_grid],
        'costs': [float(c) for c in costs],
    }


def collapse_scan_2d(curves, g_c, kappa_grid, a_grid):
    """Two-parameter collapse (kappa, a both free) -> independent 1/nu and height
    exponent, as a cross-check of the Albuquerque relation a = 2/nu - d."""
    best = (np.inf, None, None)
    for k in kappa_grid:
        for a in a_grid:
            c = _collapse_cost(curves, g_c, k, a)
            if c < best[0]:
                best = (c, float(k), float(a))
    return {'cost_min': float(best[0]), 'kappa_best': best[1], 'a_best': best[2]}

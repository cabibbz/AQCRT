"""Sprint 136a: VALIDATION of the thermal-gap exceptional-point (EP) method on q=2 (Ising).

 1. charge-0 (Z_q-symmetric) thermal gap Delta_eps(g) = E1c0 - E0c0, P=prod X_i filter.
 2. real-axis EP estimate Im(g_EP) = sqrt(Delta_min / Delta''(g*))  (2-level avoided-crossing).
 3. CROSS-CHECK (n<=10, dense): complex-symmetric H(g*+iy); find y where the two charge-0
    eigenvalues coalesce (the actual EP). Must match (2).
 4. q=2 exactly solvable: g_c=1/q=0.5, continuous, 1/nu=1 -> Im(g_EP) ~ L^{-1} -> 0.

PERIODIC BC. DENSE eigh throughout (small n, bulletproof vs near-degeneracy).
Saves results/sprint_136a_validate_q2.json.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scipy.sparse import csr_matrix
from hamiltonian_utils import _decode_states, _build_coupling, _build_field

q = 2
g_c = 1.0 / q
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_136a_validate_q2.json')


def build_parts(n, q):
    dim, all_idx, digits, powers = _decode_states(n, q)
    Hc = _build_coupling(all_idx, digits, n, dim).toarray()
    Hf = _build_field(all_idx, digits, powers, n, q, dim, range(1, q)).toarray()
    new_idx = (((digits + 1) % q) * powers).sum(axis=1)
    P = csr_matrix((np.ones(dim), (new_idx, all_idx)), shape=(dim, dim)).toarray()
    return Hc, Hf, P


def charge0_two_lowest(Hc, Hf, P, g):
    evals, evecs = np.linalg.eigh(Hc + g * Hf)          # ascending
    chexp = np.einsum('ji,jk,ki->i', evecs, P, evecs)   # <v|P|v>, real
    c0 = np.where(chexp > 0.9)[0]
    return evals[c0[0]], evals[c0[1]]


def gap_curve(Hc, Hf, P, gs):
    return np.array([np.subtract(*charge0_two_lowest(Hc, Hf, P, g)[::-1]) for g in gs])


def parab_min(gs, ys):
    a, b, c = np.polyfit(gs, ys, 2)
    g0 = -b / (2 * a)
    return g0, a * g0**2 + b * g0 + c, 2 * a


def complex_ep_scan(Hc, Hf, P, g_star, y_max, ny=41):
    ys = np.linspace(0.0, y_max, ny)
    gaps = []
    for y in ys:
        ev, evec = np.linalg.eig(Hc + (g_star + 1j * y) * Hf)
        nrm = np.einsum('ji,ji->i', evec.conj(), evec).real
        chexp = (np.einsum('ji,jk,ki->i', evec.conj(), P, evec) / nrm).real
        c0 = np.where(chexp > 0.9)[0]
        evc0 = ev[c0]
        order = np.argsort(evc0.real)
        gaps.append(abs(evc0[order[1]] - evc0[order[0]]))
    gaps = np.array(gaps)
    k = int(np.argmin(gaps))
    return ys[k], gaps[k]


results = {'experiment': '136a_validate_q2', 'sprint': 136, 'q': q, 'g_c': g_c,
           'BC': 'periodic', 'sizes': {}}
print("=" * 78)
print(f"Sprint 136a: q={q} (Ising) thermal-gap EP method VALIDATION, g_c={g_c}")
print("=" * 78)

for n in [6, 8, 10, 12]:
    t0 = time.time()
    dim = q ** n
    Hc, Hf, P = build_parts(n, q)
    coarse = np.linspace(0.34, 0.66, 13)                 # around g_c=0.5
    cg = gap_curve(Hc, Hf, P, coarse)
    i = max(1, min(int(np.argmin(cg)), len(coarse) - 2))
    fine = np.linspace(coarse[i - 1], coarse[i + 1], 9)
    fg = gap_curve(Hc, Hf, P, fine)
    j = max(1, min(int(np.argmin(fg)), len(fine) - 2))
    g_star, gmin, gpp = parab_min(fine[j - 1:j + 2], fg[j - 1:j + 2])
    im_est = float(np.sqrt(gmin / gpp)) if gpp > 0 else float('nan')
    rec = {'n': n, 'dim': dim, 'g_star': float(g_star), 'gap_min': float(gmin),
           'gap_curv': float(gpp), 'im_gEP_estimate': im_est, 'gapmin_times_L': float(gmin * n)}
    if n <= 10:
        y_ep, gap_ep = complex_ep_scan(Hc, Hf, P, g_star, max(3 * im_est, 0.05))
        rec['im_gEP_complexscan'] = float(y_ep)
        rec['gap_at_ep'] = float(gap_ep)
    results['sizes'][n] = rec
    cs = f"  complex-scan={rec.get('im_gEP_complexscan', float('nan')):.5f}" if n <= 10 else ""
    print(f"\n n={n:2d} dim={dim:>7,}  g*={g_star:.5f}  Dmin={gmin:.5f}  Dmin*L={gmin*n:.4f}")
    print(f"     Im(g_EP) est={im_est:.5f}{cs}  [{time.time()-t0:.1f}s]")
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2, default=str)

ns = sorted(results['sizes'])
ims = np.array([results['sizes'][n]['im_gEP_estimate'] for n in ns])
slope = float(np.polyfit(np.log(ns), np.log(ims), 1)[0])
results['loglog_slope_im_vs_L'] = slope
print("\n" + "=" * 78)
print(f"Im(g_EP) log-log slope vs L = {slope:.3f}   (Ising expects -1/nu = -1.0)")
print(f"Dmin*L (-> 2*pi*v*x_eps): {[round(results['sizes'][n]['gapmin_times_L'],3) for n in ns]}")
print("=" * 78)
with open(OUT, 'w') as f:
    json.dump(results, f, indent=2, default=str)
print("DONE ->", OUT)

"""Sprint 140b: magnon dispersion cross-check -- velocity v and disordered gap Delta_d of
the q=10 chain near the transition, via CHARGE-RESOLVED periodic ED in the Fourier basis.

Why charge-resolved: at g ~ g_c the ordered-tower near-degeneracy makes plain-eigsh
eigenvectors mix charge sectors (the <P> filter finds nothing). In the Fourier (charge)
basis |m_1..m_n>, total charge Q = sum m_i (mod q) is BASIS-diagonal, so the charge-0 and
charge-1 blocks are built and diagonalized exactly:
  field (diagonal):  -g * sum_i (q*delta_{m_i,0} - 1)
  bond  (i,i+1):     -(1/q) * [ 1 + sum_{k=1}^{q-1} (m_i += k, m_j -= k) ]   (periodic)
Momentum from <v|T|v> = cos k (T = cyclic site shift; commutes with H and charge).
Ordered-tower intruder states are identified (and excluded from the band) by their field
expectation <F> = sum_i <q delta_{m_i,0} - 1>: disordered-branch states have LARGE <F>
(~n(q-1)*0.6-ish at g~g_c/dis side), ordered-tower states small/negative.

Fit: E(k)^2 = Delta_d^2 + 4 v^2 sin^2(k/2)  ->  xi_x^ED = v/Delta_d, compared with
exp_140a's direct correlator xi_x at the SAME g.

Usage:  python exp_140b_magnon_dispersion.py [n] [g]   (default n=6, g=0.105)
Writes results/sprint_140b_dispersion_q10.json; DB: v_magnon, gap_disordered, xi_x_from_vgap.
"""
import numpy as np
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
from scipy.sparse import csr_matrix
from gpu_utils import eigsh
from db_utils import record

q = 10
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
g = float(sys.argv[2]) if len(sys.argv) > 2 else 0.105
KB = 12                                       # states per charge block
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_140b_dispersion_q10.json')

t0 = time.time()
dim_full = q ** n
all_m = np.arange(dim_full, dtype=np.int64)
powers = q ** np.arange(n, dtype=np.int64)
digits = (all_m[:, None] // powers[None, :]) % q          # m-string per basis state
charge = digits.sum(axis=1) % q


def block(Q):
    """Sparse H and helpers restricted to total charge Q."""
    sel = np.where(charge == Q)[0]
    pos = -np.ones(dim_full, dtype=np.int64)
    pos[sel] = np.arange(len(sel))
    dg = digits[sel]
    fdiag = ((q * (dg == 0) - 1).sum(axis=1)).astype(float)        # sum_i (q d_{m,0} - 1)
    rows, cols, vals = [], [], []
    d = len(sel)
    # diagonal: field + bond constant -n/q
    rows.append(np.arange(d)); cols.append(np.arange(d))
    vals.append(-g * fdiag - n / q)
    # off-diagonal bond hops: (m_i += k, m_j -= k), amplitude -1/q
    for i in range(n):
        j = (i + 1) % n
        for k in range(1, q):
            nd = dg.copy()
            nd[:, i] = (nd[:, i] + k) % q
            nd[:, j] = (nd[:, j] - k) % q
            tgt = pos[(nd * powers).sum(axis=1)]
            rows.append(tgt); cols.append(np.arange(d))
            vals.append(np.full(d, -1.0 / q))
    H = csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                   shape=(d, d))
    # translation within the block
    tgtT = pos[(np.roll(dg, 1, axis=1) * powers).sum(axis=1)]
    T = csr_matrix((np.ones(d), (tgtT, np.arange(d))), shape=(d, d))
    return H, T, fdiag


def lowest(H, k):
    evals, evecs = eigsh(H, k=k, which='SA', maxiter=5000, tol=1e-10)
    o = np.argsort(evals)
    return evals[o], evecs[:, o]


print("=" * 78)
print(f"Sprint 140b: q={q} n={n} g={g} periodic, charge-resolved (block dims ~{dim_full//q:,})")

H0, T0, f0 = block(0)
e0, v0 = lowest(H0, 4)
F0 = [float(v0[:, i] @ (f0 * v0[:, i])) for i in range(v0.shape[1])]
i_dis = int(np.argmax(F0[:2]))                 # disordered state = larger field expectation
E0 = float(e0[i_dis])
print(f"  charge-0: E = {[round(float(x),5) for x in e0]}  <F> = {[round(x,1) for x in F0]}")
print(f"  disordered E0 = {E0:.6f} (state {i_dis}; <F>={F0[i_dis]:.1f}; ordered-tower <F> small)")

H1, T1, f1 = block(1)
e1, v1 = lowest(H1, KB)
band = []
F_dis = F0[i_dis]
for i in range(KB):
    Fi = float(v1[:, i] @ (f1 * v1[:, i]))
    ck = float(np.clip(v1[:, i] @ (T1 @ v1[:, i]), -1, 1))
    dE = float(e1[i] - E0)
    is_ord = Fi < 0.5 * F_dis                   # ordered-tower intruder
    band.append({'dE': dE, 'cos_k': ck, 'k': float(np.arccos(ck)), 'F': Fi,
                 'ordered_intruder': bool(is_ord)})
    print(f"    dE={dE:+.5f}  cos k={ck:+.4f}  |k|={np.arccos(ck):.3f}  <F>={Fi:7.1f}"
          f"  {'ORDERED-TOWER (excluded)' if is_ord else 'magnon'}")

pts = {}
for b in band:
    if b['ordered_intruder']:
        continue
    key = round(b['k'], 3)
    if key not in pts or b['dE'] < pts[key]['dE']:
        pts[key] = b
pts = sorted(pts.values(), key=lambda b: b['k'])
ks = np.array([b['k'] for b in pts])
Es = np.array([b['dE'] for b in pts])
A = 4 * np.sin(ks / 2)**2
coef = np.polyfit(A, Es**2, 1)
v = float(np.sqrt(max(coef[0], 0)))
Dd = float(np.sqrt(max(coef[1], 0)))
xi_ed = v / Dd if Dd > 0 else float('nan')
print(f"\n  band points (k, E): {[(round(float(k),3), round(float(E),4)) for k, E in zip(ks, Es)]}")
print(f"  fit E^2 = Dd^2 + 4 v^2 sin^2(k/2):  Delta_d = {Dd:.4f}   v = {v:.4f}")
print(f"  ==> xi_x^ED = v/Delta_d = {xi_ed:.2f}   (H_A ~ 10.6, H_B ~ 21.1)   [{time.time()-t0:.0f}s]")

out = {'experiment': '140b_dispersion_q10', 'sprint': 140, 'q': q, 'n': n, 'g': g,
       'E0_disordered': E0, 'charge0_F': F0, 'band': band,
       'fit': {'Delta_d': Dd, 'v': v, 'xi_ed': xi_ed},
       'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')}
with open(OUT, 'w') as f:
    json.dump(out, f, indent=2)
record(sprint=140, model='sq_potts', q=q, n=n, quantity='v_magnon', value=v, error=None,
       method='periodic_ED_charge1_block_momentum', notes=f'g={g}; Delta_d={Dd:.4f}')
record(sprint=140, model='sq_potts', q=q, n=n, quantity='gap_disordered', value=Dd, error=None,
       method='periodic_ED_charge1_block_momentum', notes=f'g={g}; charge-1 band k=0')
record(sprint=140, model='sq_potts', q=q, n=n, quantity='xi_x_from_vgap', value=xi_ed,
       error=None, method='periodic_ED_v_over_gap', notes=f'g={g}; cross-check of exp_140a')
print("DONE ->", OUT)

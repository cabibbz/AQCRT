"""Sprint 133a: q=4 S_q Potts per-site chi_F, OPEN vs PERIODIC boundary conditions,
CANONICAL convention (central diff, dg=1e-4, factor-2, /n), matched sizes n=4..12.

STATE Top-Next #1 (the asymptote blocker). Prior open-BC data (S113/S124 DMRG, results.db
quantity 'chi_F_open') used a DIFFERENT estimator: forward diff (1-F^2)/dg^2, dg=1e-3, NO
factor-2 -> ~1/2 the canonical magnitude. So the headline "periodic 1.78 vs open 1.52" was
never apples-to-apples (and only reached n<=9, exp_113c). Here we compute OPEN BC with the
IDENTICAL canonical estimator used for the periodic series (chif_utils convention), to the
n=12 GPU frontier, so the two BC can be compared exponent-for-exponent AND value-for-value.

The ONLY difference between our periodic and open builders is the single wrap bond (n-1,0):
both share the identical basis (_decode_states) and identical transverse field (_build_field),
so any periodic/open difference is purely the boundary condition.

Validation chain (printed + asserted-soft):
  (1) reproduce S113 open forward-diff value (dg=1e-3) at n=6,8 -> match results.db chi_F_open
      (4.169510 @ n=6, 6.432503 @ n=8)
  (2) canonical_open / forward_open ~ 2.0 (central = 2 x forward for squared overlap)
  (3) periodic canonical at n=4,6,8,10 -> match results.db chi_F_exact (golden anchors)
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scipy.sparse import csr_matrix
import gpu_utils
from gpu_utils import eigsh, gpu_status, GPU_ENABLED
from hamiltonian_utils import _decode_states, _build_field, build_sq_potts_parts
from db_utils import record, query

q = 4
g_c = 1.0 / q
dg = 1e-4
dg_fwd = 1e-3                      # S113 convention, for the reproduction check
OPEN_SIZES = list(range(4, 13))   # 4..12
PER_SIZES  = list(range(4, 12))   # 4..11 (n=12 periodic taken from results.db = 93.747642)

results = {
    'experiment': '133a_bc_canonical_q4',
    'sprint': 133, 'q': q, 'g_c': g_c, 'dg': dg,
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'gpu_status': gpu_status(),
    'convention': 'canonical central (2-F2p-F2m)/(dg^2 n), dg=1e-4, g_c=1/q',
    'open': {}, 'periodic': {}, 'validation': {},
}

def save():
    outpath = os.path.join(os.path.dirname(__file__), '..', 'results',
                           'sprint_133a_bc_canonical_q4.json')
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2, default=str)

print("=" * 78)
print(f"Sprint 133a: q={q} open vs periodic canonical chi_F, n=4..12")
print(f"  {gpu_status()}")
print("=" * 78)
if not GPU_ENABLED:
    print("  *** GPU disabled -- n=12 (16.78M) infeasible on CPU. ABORT. ***")
    sys.exit(1)

# ---------- builders: shared field, only the wrap bond differs ----------
def build_parts(n, periodic):
    """Return (H_coup, H_field). Field is BC-independent; coupling drops wrap bond if open."""
    dim, all_idx, digits, powers = _decode_states(n, q)
    diag = np.zeros(dim, dtype=np.float64)
    n_bonds = n if periodic else (n - 1)
    for site in range(n_bonds):
        nxt = (site + 1) % n
        diag -= (digits[:, site] == digits[:, nxt]).astype(np.float64)
    H_coup = csr_matrix((diag, (all_idx, all_idx)), shape=(dim, dim))
    H_field = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
    return H_coup, H_field

def _free_gpu():
    try:
        import cupy as cp
        cp.get_default_memory_pool().free_all_blocks()
    except Exception:
        pass

def ground_state(H_coup, H_field, g):
    H = H_coup + g * H_field
    _, v = eigsh(H, k=1, which='SA')
    psi = np.ascontiguousarray(v[:, 0])
    del H
    _free_gpu()
    return psi

def chi_canonical(H_coup, H_field, n):
    """Canonical central-diff squared-overlap per-site chi_F at g_c, dg=1e-4."""
    psi0 = ground_state(H_coup, H_field, g_c)
    psip = ground_state(H_coup, H_field, g_c + dg)
    psim = ground_state(H_coup, H_field, g_c - dg)
    if np.dot(psi0, psip) < 0: psip = -psip
    if np.dot(psi0, psim) < 0: psim = -psim
    ov_p = float(np.dot(psi0, psip) ** 2)
    ov_m = float(np.dot(psi0, psim) ** 2)
    chi = (2.0 - ov_p - ov_m) / (dg ** 2 * n)
    return chi, ov_p, ov_m

def chi_forward_s113(H_coup, H_field, n):
    """S113 estimator: forward diff (1-F^2)/dg^2/n, dg=1e-3 (for the reproduction check)."""
    psi0 = ground_state(H_coup, H_field, g_c)
    psi1 = ground_state(H_coup, H_field, g_c + dg_fwd)
    ov = float(abs(np.dot(psi0, psi1)) ** 2)
    return (1.0 - ov) / (dg_fwd ** 2 * n), ov

# DB anchors for validation
db_open_fwd = {6: 4.169510244030524, 8: 6.432502960826425}
db_per_canon = {int(r[4]): float(r[6]) for r in query(quantity='chi_F_exact', model='sq', q=q)
                if r[4] is not None}

# ---------------------- main sweep ----------------------
for n in range(4, 13):
    dim = q ** n
    t_n = time.time()
    print(f"\n  n={n:2d} (dim={dim:,}) ...", flush=True)

    # OPEN canonical (always)
    Hc_o, Hf = build_parts(n, periodic=False)
    chi_o, ovp_o, ovm_o = chi_canonical(Hc_o, Hf, n)
    print(f"    OPEN  canonical chi_F = {chi_o:.6f}")
    results['open'][n] = {'n': n, 'dim': dim, 'chi_F': chi_o,
                          'ov_p': ovp_o, 'ov_m': ovm_o}
    record(sprint=133, model='sq', q=q, n=n, quantity='chi_F_open_exact',
           value=chi_o, method='exact_central_dg1e-4_g=1/q',
           notes='canonical convention, OPEN BC, GPU TITAN RTX')

    # validation (1)+(2): forward-diff open at n=6,8 -> match DB; canonical/forward ~2
    if n in (6, 8):
        chi_o_fwd, ov_fwd = chi_forward_s113(Hc_o, Hf, n)
        ref = db_open_fwd[n]
        reldiff = abs(chi_o_fwd - ref) / ref
        ratio_cf = chi_o / chi_o_fwd
        print(f"    [valid] open forward(dg=1e-3) = {chi_o_fwd:.6f}  vs DB {ref:.6f}"
              f"  reldiff={reldiff:.2e}  | canonical/forward = {ratio_cf:.4f}")
        results['validation'][f'open_fwd_n{n}'] = {
            'forward': chi_o_fwd, 'db_ref': ref, 'reldiff': reldiff,
            'canonical_over_forward': ratio_cf}
    del Hc_o

    # PERIODIC canonical (n<=11; reuse the same shared field Hf)
    if n in PER_SIZES:
        Hc_p, _ = build_parts(n, periodic=True)
        chi_p, ovp_p, ovm_p = chi_canonical(Hc_p, Hf, n)
        ref = db_per_canon.get(n)
        tag = ""
        if ref is not None:
            rd = abs(chi_p - ref) / ref
            tag = f"  vs DB {ref:.6f}  reldiff={rd:.2e}"
            results.setdefault('periodic_validation', {})[n] = {'db_ref': ref, 'reldiff': rd}
        print(f"    PERIO canonical chi_F = {chi_p:.6f}{tag}")
        results['periodic'][n] = {'n': n, 'dim': dim, 'chi_F': chi_p,
                                  'ov_p': ovp_p, 'ov_m': ovm_p}
        del Hc_p
    del Hf
    _free_gpu()
    save()
    print(f"    [n={n} done in {time.time()-t_n:.1f}s]")

# n=12 periodic from DB
if 12 in db_per_canon:
    results['periodic'][12] = {'n': 12, 'dim': q ** 12, 'chi_F': db_per_canon[12],
                               'source': 'results.db (S132 exp_132b)'}

# ---------------------- quick inline summary ----------------------
def series(d):
    ns = sorted(d.keys())
    return np.array(ns, float), np.array([d[n]['chi_F'] for n in ns], float)

print("\n" + "=" * 78)
print("MATCHED CANONICAL SERIES (per-site chi_F at g_c=1/q)")
print("=" * 78)
print(f"  {'n':>3} {'periodic':>12} {'open':>12} {'open/per':>10}")
all_n = sorted(set(results['open']) | set(results['periodic']))
for n in all_n:
    p = results['periodic'].get(n, {}).get('chi_F')
    o = results['open'].get(n, {}).get('chi_F')
    rs = f"{o/p:.4f}" if (p and o) else "--"
    ps = f"{p:.6f}" if p else "--"
    os_ = f"{o:.6f}" if o else "--"
    print(f"  {n:>3} {ps:>12} {os_:>12} {rs:>10}")

def pairwise(nv, cv):
    return [( int(nv[i]), int(nv[i+1]),
              (np.log(cv[i+1])-np.log(cv[i]))/(np.log(nv[i+1])-np.log(nv[i])) )
            for i in range(len(nv)-1)]

no, co = series(results['open'])
npd, cpd = series(results['periodic'])
print("\n  OPEN pairwise local exponents (consecutive n):")
for a, b, al in pairwise(no, co):
    print(f"    ({a:2d},{b:2d}) = {al:.4f}")
print("\n  PERIODIC pairwise local exponents:")
for a, b, al in pairwise(npd, cpd):
    print(f"    ({a:2d},{b:2d}) = {al:.4f}")

results['summary'] = {
    'open_pairwise': [[a, b, al] for a, b, al in pairwise(no, co)],
    'periodic_pairwise': [[a, b, al] for a, b, al in pairwise(npd, cpd)],
    'open_full_alpha': float(np.polyfit(np.log(no), np.log(co), 1)[0]),
    'periodic_full_alpha': float(np.polyfit(np.log(npd), np.log(cpd), 1)[0]),
}
save()
print(f"\n  OPEN full-series alpha     = {results['summary']['open_full_alpha']:.4f}")
print(f"  PERIODIC full-series alpha = {results['summary']['periodic_full_alpha']:.4f}")
print(f"  (null 2/nu-d = 2.0; prior open DMRG ~1.52, periodic ~1.79)")
print("\n" + "=" * 78)
print("DONE -- results/sprint_133a_bc_canonical_q4.json")
print("=" * 78)

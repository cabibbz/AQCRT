"""Sprint 132b: q=4 S_q Potts per-site chi_F at the n=12 frontier (dim 16.78M, GPU).

The first new q=4 data point past the CPU wall. STATE Top-Next #1.
Physics question: the per-site chi_F effective exponent at g_c=1/q sat at ~1.79 for
n<=11 (KNOWLEDGE table, "oscillating ~1.79"). The marginal-operator (dilution, c=1)
log-correction hypothesis predicts a SLOW climb toward the Albuquerque null 2/nu-d = 2.0
(nu=2/3). n=12 tests whether the top-end local exponent moves up.

Canonical estimator: chi_F = (2 - |<0|+>|^2 - |<0|->|^2)/(dg^2 n), dg=1e-4, g_c=1/q
(chif_utils convention). Memory-frugal: build H_coup/H_field ONCE, solve the three
ground states sequentially, free the GPU pool between solves.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import gpu_utils
from gpu_utils import eigsh, gpu_status, GPU_ENABLED
from hamiltonian_utils import build_sq_potts_parts
from fss_utils import fit_power_law, pairwise_exponents
from db_utils import record, query

q = 4
n_new = 12
g_c = 1.0 / q
dg = 1e-4

results = {
    'experiment': '132b_q4_n12_frontier',
    'sprint': 132, 'q': q, 'n': n_new, 'g_c': g_c, 'dg': dg,
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'gpu_status': gpu_status(),
    'frontier_point': {}, 'series': {}, 'fits': {},
}

def save():
    outpath = os.path.join(os.path.dirname(__file__), '..', 'results',
                           'sprint_132b_q4_n12_frontier.json')
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2, default=str)

print("=" * 78)
print(f"Sprint 132b: q=4 n={n_new} frontier chi_F (dim {q**n_new:,})")
print("=" * 78)
print(f"  {gpu_status()}")
if not GPU_ENABLED:
    print("  *** GPU disabled -- n=12 (16.78M) is infeasible on CPU. ABORT. ***")
    sys.exit(1)

# ---- frugal ground state: build parts once, solve sequentially, free GPU pool ----
def ground_state(H_coup, H_field, g):
    H = H_coup + g * H_field
    _, v = eigsh(H, k=1, which='SA')
    psi = np.ascontiguousarray(v[:, 0])
    del H
    try:
        import cupy as cp
        cp.get_default_memory_pool().free_all_blocks()
    except Exception:
        pass
    return psi

t_build0 = time.time()
print(f"\n  building H_coup, H_field for q={q} n={n_new} ...", flush=True)
H_coup, H_field = build_sq_potts_parts(n_new, q)
t_build = time.time() - t_build0
nnz = H_field.nnz + H_coup.nnz
print(f"  built in {t_build:.1f}s  (H_field nnz={H_field.nnz:,}, ~{nnz*12/1e9:.1f}GB CSR)")

t0 = time.time()
print("  solving psi0 (g_c) ...", flush=True)
psi0 = ground_state(H_coup, H_field, g_c)
print(f"    done {time.time()-t0:.1f}s")
t0b = time.time()
print("  solving psi+ (g_c+dg) ...", flush=True)
psip = ground_state(H_coup, H_field, g_c + dg)
print(f"    done {time.time()-t0b:.1f}s")
t0c = time.time()
print("  solving psi- (g_c-dg) ...", flush=True)
psim = ground_state(H_coup, H_field, g_c - dg)
print(f"    done {time.time()-t0c:.1f}s")

# sign-align then canonical squared-overlap finite difference
if np.dot(psi0, psip) < 0: psip = -psip
if np.dot(psi0, psim) < 0: psim = -psim
ov_p = float(np.dot(psi0, psip) ** 2)
ov_m = float(np.dot(psi0, psim) ** 2)
chi_n12 = (2.0 - ov_p - ov_m) / (dg ** 2 * n_new)
t_total = time.time() - t_build0

print(f"\n  chi_F(q=4, n=12) = {chi_n12:.6f}   (overlaps: +{ov_p:.10f} -{ov_m:.10f})")
print(f"  total time {t_total:.1f}s")

results['frontier_point'] = {
    'n': n_new, 'dim': q ** n_new, 'chi_F_exact': chi_n12,
    'ov_p': ov_p, 'ov_m': ov_m, 'time_s': round(t_total, 1),
    'build_s': round(t_build, 1)}
save()

# Record to DB immediately
record(sprint=132, model='sq', q=q, n=n_new, quantity='chi_F_exact',
       value=chi_n12, method='finite_diff',
       notes='GPU TITAN RTX cupy13.6.0; dg=1e-4; g_c=1/q')
print("  recorded to results.db (sprint=132, sq q=4 n=12 chi_F_exact)")

# ---- assemble full series from DB + new point ----
db_rows = query(quantity='chi_F_exact', model='sq', q=q)
series = {}
for r in db_rows:                      # (id,sprint,model,q,n,quantity,value,error,method,notes)
    n_r, v_r = r[4], r[6]
    if n_r is not None:
        series[int(n_r)] = float(v_r)  # latest (query ORDER BY sprint DESC) -> but dedupe by n; keep any
series[n_new] = chi_n12
sizes = np.array(sorted(series.keys()), dtype=float)
chi = np.array([series[int(s)] for s in sizes])
print(f"\n  full q=4 series ({len(sizes)} sizes): " +
      ", ".join(f"n={int(s)}:{series[int(s)]:.4f}" for s in sizes))
results['series'] = {int(s): series[int(s)] for s in sizes}

# ---- fits: full series, with vs without n=12, windowed local exponents ----
def fit(sz, ch):
    f = fit_power_law(sz, ch)
    return f['alpha'], f['alpha_err'], f['r_squared']

a_full, ae_full, r2_full = fit(sizes, chi)
mask_no12 = sizes < 12
a_no12, ae_no12, r2_no12 = fit(sizes[mask_no12], chi[mask_no12])
print(f"\n  power-law fit (full n=4..12): alpha = {a_full:.4f} +/- {ae_full:.4f}  (R2={r2_full:.8f})")
print(f"  power-law fit (n=4..11 only): alpha = {a_no12:.4f} +/- {ae_no12:.4f}  (R2={r2_no12:.8f})")
print(f"  -> adding n=12 shifts full-series alpha by {a_full - a_no12:+.4f}")

pairs = pairwise_exponents(sizes, chi)
print(f"\n  pairwise local exponents (consecutive sizes):")
for p in pairs:
    print(f"    ({p['n1']:2d},{p['n2']:2d}) = {p['alpha']:.4f}")

# windowed power-law over the top-k points, to see the local exponent vs <N>
print(f"\n  windowed power-law over the largest-k sizes (local effective exponent):")
window_fits = []
for k in (3, 4, 5):
    if len(sizes) >= k:
        sw, cw = sizes[-k:], chi[-k:]
        aw, aew, r2w = fit(sw, cw)
        meanlnN = float(np.mean(np.log(sw)))
        print(f"    top-{k} (n={int(sw[0])}..{int(sw[-1])}): alpha = {aw:.4f} +/- {aew:.4f}  (R2={r2w:.7f})")
        window_fits.append({'k': k, 'n_lo': int(sw[0]), 'n_hi': int(sw[-1]),
                            'alpha': aw, 'alpha_err': aew, 'r_squared': r2w,
                            'mean_lnN': meanlnN})

# the headline trend: top-3 local exponent WITH vs WITHOUT n=12
top3_with = fit(sizes[-3:], chi[-3:])[0]                 # n=10,11,12
top3_prev = fit(sizes[-4:-1], chi[-4:-1])[0]             # n=9,10,11
print(f"\n  HEADLINE -- top-3 local exponent:")
print(f"    n=9,10,11  = {top3_prev:.4f}  (previous frontier)")
print(f"    n=10,11,12 = {top3_with:.4f}  (new frontier)")
print(f"    climb = {top3_with - top3_prev:+.4f}   (toward null 2/nu-d = 2.0)")

results['fits'] = {
    'alpha_full': a_full, 'alpha_full_err': ae_full, 'r2_full': r2_full,
    'alpha_no12': a_no12, 'alpha_no12_err': ae_no12, 'r2_no12': r2_no12,
    'd_alpha_adding_n12': a_full - a_no12,
    'pairwise': [{'n1': p['n1'], 'n2': p['n2'], 'alpha': p['alpha']} for p in pairs],
    'windowed': window_fits,
    'top3_local_prev_9_10_11': top3_prev,
    'top3_local_new_10_11_12': top3_with,
    'top3_climb': top3_with - top3_prev,
    'null_2_over_nu_minus_d': 2.0,
}
save()

# update the canonical alpha_exact (full-series power law) in DB
record(sprint=132, model='sq', q=q, n=n_new, quantity='alpha_exact',
       value=a_full, error=ae_full, method='exact_chif_power_law',
       notes=f"sizes={[int(s) for s in sizes]} (n=12 frontier added)")
print(f"\n  recorded alpha_exact={a_full:.4f} to DB (sprint=132)")
print("\n" + "=" * 78)
print("DONE -- results/sprint_132b_q4_n12_frontier.json")
print("=" * 78)

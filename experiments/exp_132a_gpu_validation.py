"""Sprint 132a: Validate the RESTORED GPU chi_F pipeline.

The GPU outage (cupy ABI mismatch vs numpy 1.26.4) was fixed by pinning
cupy-cuda12x==13.6.0. This experiment proves the restored pipeline reproduces
the canonical exact chi_F before we trust it on the n=12 frontier (exp_132b).

Checks:
  1. gpu_status() reports GPU enabled (TITAN RTX, CuPy 13.6.0).
  2. Recompute q=4 sq chi_F_exact at n=9,10,11 (all route to GPU, dim>50k) and
     compare to the stored results.db values. Must match to ~1e-5 (dg=1e-4 carries
     a smooth ~1e-6 bias; the exact estimator is otherwise deterministic).
  3. CPU-vs-GPU cross-check at n=9 (dim 262k): same chi_F from scipy eigsh and
     gpu_utils eigsh. Independent confirmation the GPU solve is not silently wrong.

This writes NO new DB rows (pure reproduction); JSON only.
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scipy.sparse.linalg import eigsh as cpu_eigsh
import gpu_utils
from gpu_utils import eigsh as gpu_eigsh, gpu_status, GPU_ENABLED
from hamiltonian_utils import build_sq_potts_parts
from chif_utils import chi_F_exact

results = {
    'experiment': '132a_gpu_validation',
    'sprint': 132,
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'gpu_status': gpu_status(),
    'gpu_enabled': bool(GPU_ENABLED),
    'reproduction': [],
    'cpu_vs_gpu': {},
    'all_pass': None,
}

def save():
    outpath = os.path.join(os.path.dirname(__file__), '..', 'results',
                           'sprint_132a_gpu_validation.json')
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2, default=str)

print("=" * 78)
print("Sprint 132a: GPU pipeline validation")
print("=" * 78)
print(f"  {gpu_status()}")
if not GPU_ENABLED:
    print("  *** GPU NOT ENABLED -- this validation is meaningless on CPU. ABORT. ***")
    results['all_pass'] = False
    save()
    sys.exit(1)

q = 4
g_c = 1.0 / q
# Canonical stored values from results.db (sprint 126/127, finite_diff).
DB_REF = {9: 56.183728, 10: 67.784201, 11: 80.310875}

print(f"\n[1] Reproduce q=4 sq chi_F_exact at n=9,10,11 (GPU) vs results.db")
all_pass = True
for n in (9, 10, 11):
    dim = q ** n
    t0 = time.time()
    H_coup, H_field = build_sq_potts_parts(n, q)
    chi_val = chi_F_exact(H_coup, H_field, g_c, n, eigsh=gpu_eigsh)
    dt = time.time() - t0
    ref = DB_REF[n]
    reldiff = abs(chi_val - ref) / ref
    ok = reldiff < 1e-5
    all_pass &= ok
    tag = "PASS" if ok else "*** FAIL ***"
    print(f"  [{tag}] n={n:2d} dim={dim:>10,}  chi_F={chi_val:.6f}  vs DB {ref:.6f}  "
          f"reldiff={reldiff:.1e}  ({dt:.1f}s)")
    results['reproduction'].append({
        'n': n, 'dim': dim, 'chi_F_gpu': float(chi_val), 'db_ref': ref,
        'reldiff': float(reldiff), 'pass': bool(ok), 'time_s': round(dt, 1)})
    del H_coup, H_field
    save()

print(f"\n[2] CPU-vs-GPU cross-check at n=9 (dim {q**9:,})")
n = 9
H_coup, H_field = build_sq_potts_parts(n, q)
t0 = time.time()
chi_cpu = chi_F_exact(H_coup, H_field, g_c, n, eigsh=cpu_eigsh)
t_cpu = time.time() - t0
t0 = time.time()
chi_gpu = chi_F_exact(H_coup, H_field, g_c, n, eigsh=gpu_eigsh)
t_gpu = time.time() - t0
cross_reldiff = abs(chi_cpu - chi_gpu) / chi_cpu
cross_ok = cross_reldiff < 1e-6
all_pass &= cross_ok
tag = "PASS" if cross_ok else "*** FAIL ***"
print(f"  [{tag}] CPU chi_F={chi_cpu:.8f} ({t_cpu:.1f}s)  GPU chi_F={chi_gpu:.8f} ({t_gpu:.1f}s)  "
      f"reldiff={cross_reldiff:.1e}")
print(f"         GPU speedup vs CPU at n=9: {t_cpu/t_gpu:.1f}x")
results['cpu_vs_gpu'] = {
    'n': n, 'dim': q**n, 'chi_F_cpu': float(chi_cpu), 'chi_F_gpu': float(chi_gpu),
    'reldiff': float(cross_reldiff), 'pass': bool(cross_ok),
    't_cpu_s': round(t_cpu, 1), 't_gpu_s': round(t_gpu, 1),
    'speedup': round(t_cpu / t_gpu, 1)}

results['all_pass'] = bool(all_pass)
save()

print("\n" + "=" * 78)
print(f"VALIDATION: {'ALL PASS -- GPU pipeline trustworthy for n=12 frontier' if all_pass else '*** FAILURES -- do NOT trust n=12 ***'}")
print("=" * 78)
sys.exit(0 if all_pass else 1)

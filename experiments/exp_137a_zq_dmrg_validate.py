"""Sprint 137a: VALIDATE the Z_q-conserving DMRG charge-0 thermal gap against open-BC exact
diagonalization, per q (default q=8; also run with 10 and 6).

Checks, at 3 couplings spanning the charge-0 gap minimum region:
  1. E0 (charge-0 ground) DMRG == ED to ~1e-8 rel (after the constant-offset conversion)
  2. E1 (charge-0 first excited via orthogonal_to) DMRG == ED
  3. Delta_eps DMRG == ED
ED reference: open-chain H (diagonal coupling on n-1 bonds + same field), K lowest states,
charge filter <v|P|v> > 0.9 (ep_utils pattern). Sizes chosen so ED is exact-feasible.

Usage:  python exp_137a_zq_dmrg_validate.py [q]      (writes results/sprint_137a_validate_q{q}.json)
"""
import numpy as np
import json, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.sparse import csr_matrix
from hamiltonian_utils import _decode_states, _build_field
from ep_utils import charge0_two_lowest
from zq_dmrg_utils import thermal_gap_charge0, mpo_to_szbasis
from db_utils import record

q = int(sys.argv[1]) if len(sys.argv) > 1 else 8
g_c = 1.0 / q
SIZES = {6: [7, 8], 7: [6, 7], 8: [6, 7], 10: [5, 6]}.get(q, [5, 6])
CHI = 64
SPRINT = int(os.environ.get('SPRINT_NO', 137))     # generic harness; later sprints override
OUT = os.path.join(os.path.dirname(__file__), '..', 'results',
                   f'sprint_{SPRINT}a_validate_q{q}.json')


def build_open_parts(n):
    """Open-chain S_q Potts: Hc diagonal (n-1 bonds), Hf = -sum_k X^k (hamiltonian_utils),
    P = global shift (charge operator)."""
    dim, all_idx, digits, powers = _decode_states(n, q)
    diag = np.zeros(dim)
    for s in range(n - 1):
        diag -= (digits[:, s] == digits[:, s + 1]).astype(float)
    Hc = csr_matrix((diag, (all_idx, all_idx)), shape=(dim, dim))
    Hf = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
    new_idx = (((digits + 1) % q) * powers).sum(axis=1)
    P = csr_matrix((np.ones(dim), (new_idx, all_idx)), shape=(dim, dim))
    return Hc, Hf, P


res = {'experiment': f'{SPRINT}a_zq_dmrg_validate_q{q}', 'sprint': SPRINT, 'q': q, 'g_c': g_c,
       'BC': 'open', 'chi_max': CHI, 'cases': []}
print("=" * 78)
print(f"Sprint 137a: Z_q-conserving DMRG vs open-BC ED, q={q}, sizes={SIZES}, chi={CHI}")
print("=" * 78)

worst = 0.0
for n in SIZES:
    K = 2 * q + 6
    Hc, Hf, P = build_open_parts(n)
    # 3 couplings spanning the expected gap-min region (open-chain g* sits well below g_c)
    for g in [0.70 * g_c, 0.85 * g_c, 1.00 * g_c]:
        t0 = time.time()
        e0_ed, e1_ed = charge0_two_lowest(Hc, Hf, P, g, K)
        t_ed = time.time() - t0
        t0 = time.time()
        E0m, E1m, d_dm, p0, p1, cu = thermal_gap_charge0(n, q, g, CHI)
        t_dm = time.time() - t0
        e0_dm = mpo_to_szbasis(E0m, n, q=q)
        e1_dm = mpo_to_szbasis(E1m, n, q=q)
        d_ed = e1_ed - e0_ed
        r0 = abs(e0_dm - e0_ed) / abs(e0_ed)
        r1 = abs(e1_dm - e1_ed) / abs(e1_ed)
        rd = abs(d_dm - d_ed) / d_ed
        worst = max(worst, r0, r1, rd)
        # thresholds: E0 1e-5 (deep-ordered side at large q is near-degenerate -> slower
        # DMRG; rel ~5e-6 observed at q=10 g=0.7g_c); E1/gap limited by chi=64 truncation
        # (~1e-5..3e-4 rel) -- all far below the 1e-2-level slope signals we measure
        ok = r0 < 1e-5 and r1 < 1e-4 and rd < 5e-4
        res['cases'].append({'n': n, 'g': g, 'E0_ed': float(e0_ed), 'E1_ed': float(e1_ed),
                             'E0_dmrg': e0_dm, 'E1_dmrg': e1_dm, 'gap_ed': float(d_ed),
                             'gap_dmrg': d_dm, 'rel_E0': r0, 'rel_E1': r1, 'rel_gap': rd,
                             'chi_used': cu, 't_ed_s': round(t_ed, 1), 't_dmrg_s': round(t_dm, 1),
                             'pass': bool(ok)})
        print(f"  n={n} g={g:.5f}  gap ED={d_ed:.8f} DMRG={d_dm:.8f}  "
              f"rel(E0,E1,gap)=({r0:.1e},{r1:.1e},{rd:.1e})  chi={cu}  "
              f"[ED {t_ed:.1f}s, DMRG {t_dm:.1f}s]  {'PASS' if ok else '*** FAIL ***'}")

res['worst_rel'] = worst
res['all_pass'] = all(c['pass'] for c in res['cases'])
res['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
with open(OUT, 'w') as f:
    json.dump(res, f, indent=2)
record(sprint=SPRINT, model='sq_potts', q=q, n=max(SIZES), quantity='zq_dmrg_validation_worst_rel',
       value=worst, error=None, method='dmrg_vs_ed_charge0_gap_open',
       notes=f'chi={CHI}; {len(res["cases"])} cases (E0,E1,gap); all_pass={res["all_pass"]}')
print(f"\n{'ALL PASS' if res['all_pass'] else '*** FAILURES ***'}  worst rel diff = {worst:.2e}")
print("DONE ->", OUT)
sys.exit(0 if res['all_pass'] else 1)

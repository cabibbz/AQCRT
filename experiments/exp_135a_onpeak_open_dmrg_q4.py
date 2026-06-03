"""Sprint 135a: q=4 S_q Potts per-site chi_F at the PEAK g*(L), OPEN BC, via DMRG to large L.

WHY: S134 showed the ON-PEAK peak-height chi_F is the correct FSS observable and open kappa_eff
ASCENDS monotonically 0.657->1.281 (n=4..12) toward 2/nu-d=2.0. n=12 is the exact-diag frontier.
S124 did open DMRG chi_F to n=20 but at the WRONG coupling (fixed g_c, deep off the open peak) --
S134 proved the off-peak penalty pollutes the exponent. Here we redo it ON-PEAK and push past n=12.

LITERATURE: 4-state Potts has a marginal (dilution) operator => log corrections (Salas-Sokal 1997).
Cardy (1986) + Hamer (1988, quantum chain Bethe ansatz) predict finite-size corrections ~ x + d/ln L
for THIS model. So expect kappa_eff(L) = 2 + sigma/ln L (linear in 1/ln L, intercept 2.0).

CONVENTION: canonical central per-site chi_F (chif_utils / exp_134a):
    chi_F(g) = (2 - |<psi(g)|psi(g+dg)>|^2 - |<psi(g)|psi(g-dg)>|^2)/(dg^2 n).
DMRG uses dg=1e-3 (vs exact 1e-4) to stay above overlap noise; exponent is dg-insensitive.

PERF (probe v2): REAL float64 ops (~6x vs complex). Warm-start: psi(g) from previous scan point;
psi(g+-dg) from psi(g) -> fast + low overlap noise. Peak located by a forward-diff scan around the
predicted g* (S134 gstar trend), parabola vertex; canonical CENTRAL chi reported at the vertex.

Usage:  python exp_135a_onpeak_open_dmrg_q4.py [n1 n2 ...]   (default 10; ACCUMULATES across runs)
Saves results/sprint_135a_onpeak_open_dmrg_q4.json; records chi_F_open_peak / gstar_open to DB.
"""
import numpy as np, json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import warnings; warnings.filterwarnings('ignore')
from db_utils import record, query

q = 4
g_c = 1.0 / q
DG = 1e-3
DG_EXACT = 1e-4
SVD_MIN = 1e-8             # chiconv@n=12: chi=48 already gives DMRG/exact_dg3=1.000000 (chi_F=70.5227
                          # vs exact 70.5227); chi=64 identical. So cap chi LOW for speed.
sizes = [int(x) for x in sys.argv[1:]] or [10]

def chi_max_for(n):        # chi=48 converges chi_F to ~1e-6 (n=12); entanglement grows only ~log (S:1.1->1.42 n=10->24)
    if n <= 30: return 48
    if n <= 38: return 64
    return 80

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'sprint_135a_onpeak_open_dmrg_q4.json')
if os.path.exists(OUT):
    with open(OUT) as f:
        results = json.load(f)
    results['peaks'] = {int(k): v for k, v in results.get('peaks', {}).items()}
else:
    results = {'experiment': '135a_onpeak_open_dmrg_q4', 'sprint': 135, 'q': q, 'g_c': g_c,
               'dg_dmrg': DG, 'svd_min': SVD_MIN,
               'convention': 'canonical central per-site chi_F at peak g*(L), OPEN BC, DMRG real-dtype',
               'peaks': {}}

def save():
    results['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2, default=str)

# ============================ DMRG (open BC, REAL dtype) ============================
from tenpy.models.model import CouplingMPOModel, NearestNeighborModel
from tenpy.networks.site import Site
from tenpy.linalg import np_conserved as npc
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg

class SqPottsSite(Site):
    def __init__(self, q_val):
        leg = npc.LegCharge.from_trivial(q_val)
        Site.__init__(self, leg, [str(a) for a in range(q_val)], sort_charge=False)
        for a in range(q_val):
            P = np.zeros((q_val, q_val)); P[a, a] = 1.0
            self.add_op(f'P{a}', P)
        Sq = np.ones((q_val, q_val)) - np.eye(q_val)         # real symmetric
        self.add_op('SqField', Sq, hc='SqField')

class SqPottsChain(CouplingMPOModel, NearestNeighborModel):
    def init_sites(self, mp): return SqPottsSite(mp.get('q', q))
    def init_terms(self, mp):
        J = mp.get('J', 1.0); g = mp.get('g', g_c); qv = mp.get('q', q)
        for a in range(qv): self.add_coupling(-J, 0, f'P{a}', 0, f'P{a}', 1)
        self.add_onsite(-g, 0, 'SqField')

def dmrg_gs(n, g, chi_max, init=None, minsw=2, maxsw=24):
    model = SqPottsChain({'L': n, 'q': q, 'J': 1.0, 'g': g, 'bc_MPS': 'finite'})
    if init is None:
        np.random.seed(7 + n)
        psi = MPS.from_product_state(model.lat.mps_sites(),
                                     [int(np.random.randint(q)) for _ in range(n)], bc='finite')
    else:
        psi = init.copy()
    eng = dmrg.TwoSiteDMRGEngine(psi, model, {
        'mixer': True, 'max_E_err': 1e-11, 'max_S_err': 1e-8,
        'trunc_params': {'chi_max': chi_max, 'svd_min': SVD_MIN},
        'min_sweeps': minsw, 'max_sweeps': maxsw})
    E0, _ = eng.run()
    psi.canonical_form()           # ensure proper normalization for accurate overlaps (probe saw norm_err~2e-5)
    return float(E0), psi, max(psi.chi)

_NS = [0]
def chi_forward(n, g, chi_max, base):
    """Forward-diff per-site chi_F (textbook, no factor-2) -- for LOCATING the peak only."""
    _, p0, cu0 = dmrg_gs(n, g, chi_max, init=base)
    _, p1, cu1 = dmrg_gs(n, g + DG, chi_max, init=p0)
    _NS[0] += 2
    F = abs(p0.overlap(p1)) ** 2
    return (1.0 - F) / (DG ** 2 * n), p0, max(cu0, cu1)

def chi_central(n, g, chi_max, base):
    """Canonical central per-site chi_F (factor-2) -- the reported value."""
    _, p0, cu0 = dmrg_gs(n, g, chi_max, init=base)
    _, pp, cup = dmrg_gs(n, g + DG, chi_max, init=p0)
    _, pm, cum = dmrg_gs(n, g - DG, chi_max, init=p0)
    _NS[0] += 3
    Fp = abs(p0.overlap(pp)) ** 2; Fm = abs(p0.overlap(pm)) ** 2
    return (2.0 - Fp - Fm) / (DG ** 2 * n), p0, max(cu0, cup, cum)

def predict_gstar(n):
    rows = query(quantity='gstar_open', q=q)
    data = {r[4]: r[6] for r in rows if r[4] <= 12}     # anchor on exact S134 (n<=12)
    ns = sorted(data)
    if len(ns) >= 3:
        lN = np.log(ns); lsh = np.log([g_c - data[m] for m in ns])
        c = np.polyfit(lN, lsh, 1)                       # ln(shift) = c0*lnN + c1
        return g_c - float(np.exp(c[1]) * n ** c[0])
    return g_c - 0.03

def find_peak(n, chi_max):
    center = min(predict_gstar(n), g_c - 0.004)
    hw = 0.014 if n <= 20 else 0.010
    for attempt in range(2):
        grid = np.linspace(center - hw, min(center + hw, g_c - 0.001), 5)
        base = None; chis = []; cu = 0
        for g in grid:
            c, base, cuu = chi_forward(n, g, chi_max, base); chis.append(c); cu = max(cu, cuu)
        chis = np.array(chis); i = int(np.argmax(chis))
        if 0 < i < 4: break
        center = grid[i]                                 # recenter once if edge
    k = max(1, min(i, 3))
    a, b, _ = np.polyfit(grid[k - 1:k + 2], chis[k - 1:k + 2], 2)
    # forward-diff chi_F(g) peaks at g_peak - dg/2 (probes the midpoint) -> correct the vertex by +dg/2
    gstar = float(-b / (2 * a)) + DG / 2.0; gstar = min(gstar, g_c - 0.0003)
    chi_peak, _, cu2 = chi_central(n, gstar, chi_max, base)
    return {'g_star': gstar, 'chi_peak': float(chi_peak), 'chi_used': int(max(cu, cu2)),
            'scan_grid': grid.tolist(), 'scan_chi_fwd': chis.tolist()}

# ---- cheap exact validation (n<=10) ----
def exact_validate(n, gstar):
    from scipy.sparse import csr_matrix
    from hamiltonian_utils import _decode_states, _build_field
    from gpu_utils import eigsh
    dim, all_idx, digits, powers = _decode_states(n, q)
    diag = np.zeros(dim)
    for s in range(n - 1): diag -= (digits[:, s] == digits[:, s + 1]).astype(float)
    Hc = csr_matrix((diag, (all_idx, all_idx)), shape=(dim, dim))
    Hf = _build_field(all_idx, digits, powers, n, q, dim, range(1, q))
    def chi_at(g, dg):
        def gs(gg):
            _, v = eigsh(Hc + gg * Hf, k=1, which='SA'); return np.ascontiguousarray(v[:, 0])
        p0, pp, pm = gs(g), gs(g + dg), gs(g - dg)
        if np.dot(p0, pp) < 0: pp = -pp
        if np.dot(p0, pm) < 0: pm = -pm
        return (2.0 - float(np.dot(p0, pp) ** 2) - float(np.dot(p0, pm) ** 2)) / (dg ** 2 * n)
    return {'exact_chi_dg3': chi_at(gstar, DG), 'exact_chi_dg4': chi_at(gstar, DG_EXACT)}

# ============================ run ============================
print("=" * 80, flush=True)
print(f"Sprint 135a: q={q} OPEN on-peak chi_F via DMRG, sizes={sizes}, dg={DG}, svd_min={SVD_MIN}", flush=True)
print("=" * 80, flush=True)

for n in sizes:
    t0 = time.time(); _NS[0] = 0
    cm = chi_max_for(n)
    pk = find_peak(n, cm)
    dt = time.time() - t0
    val = {}
    if n <= 10:
        try:
            v = exact_validate(n, pk['g_star'])
            v['dmrg_over_exact_dg3'] = pk['chi_peak'] / v['exact_chi_dg3']
            v['dg_sys_e3_over_e4'] = v['exact_chi_dg3'] / v['exact_chi_dg4']
            val = v
        except Exception as e:
            val = {'exact_error': str(e)}
    rec = {'n': n, 'g_star': pk['g_star'], 'shift': pk['g_star'] - g_c, 'chi_peak': pk['chi_peak'],
           'chi_max': cm, 'chi_used': pk['chi_used'], 'n_solves': _NS[0], 'time_s': round(dt, 1),
           'scan': {'grid': pk['scan_grid'], 'chi_fwd': pk['scan_chi_fwd']}, 'validation': val}
    results['peaks'][n] = rec
    msg = (f"\n  n={n:2d}  g*={pk['g_star']:.5f} (shift {pk['g_star']-g_c:+.5f})  "
           f"chi_peak={pk['chi_peak']:.5f}  chi_used={pk['chi_used']}/{cm}  "
           f"[{_NS[0]} solves, {dt:.1f}s]")
    if 'dmrg_over_exact_dg3' in val:
        msg += (f"\n       VALIDATION DMRG/exact(dg=1e-3)={val['dmrg_over_exact_dg3']:.6f}  "
                f"exact_chi(dg1e-4)={val['exact_chi_dg4']:.5f}  dg-sys={val['dg_sys_e3_over_e4']:.5f}")
    print(msg, flush=True)
    record(sprint=135, model='sq', q=q, n=n, quantity='chi_F_open_peak', value=float(pk['chi_peak']),
           method='dmrg_canonical_at_peak_dg1e-3',
           notes=f'OPEN DMRG chi={cm}/used{pk["chi_used"]} svd1e-10 g*={pk["g_star"]:.5f}; on-peak')
    record(sprint=135, model='sq', q=q, n=n, quantity='gstar_open', value=float(pk['g_star']),
           method='dmrg_parabola_vertex', notes=f'open peak (DMRG); shift {pk["g_star"]-g_c:+.5f}')
    save()

# ---- pairwise kappa over full accumulated DMRG series ----
pk = results['peaks']
if len(pk) >= 3:
    ns = sorted(pk)
    print("\n" + "=" * 80, flush=True)
    print("PAIRWISE kappa_eff (OPEN on-peak DMRG):", flush=True)
    print(f"  {'pair':>9} {'L_mid':>6} {'1/lnL':>7} {'kappa':>8}", flush=True)
    for i in range(len(ns) - 1):
        a, b = ns[i], ns[i + 1]
        ka = (np.log(pk[b]['chi_peak']) - np.log(pk[a]['chi_peak'])) / (np.log(b) - np.log(a))
        Lm = (a * b) ** 0.5
        print(f"  ({a:2d},{b:2d}) {Lm:6.2f} {1/np.log(Lm):7.4f} {ka:8.4f}", flush=True)
print("\nDONE -- results/sprint_135a_onpeak_open_dmrg_q4.json", flush=True)

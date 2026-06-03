# Current State -- Rewrite this completely each sprint

## Last Sprint
Sprint 132 -- **GPU RESTORED + q=4 n=12 frontier reached.** sprints/sprint_132.md (also unpublished/);
results/sprint_132{a-e}*.json.
- GPU fix: pinned **cupy-cuda12x 13.6.0** + numpy==1.26.4 (14.0.1 needed numpy>=2 = the ABI break).
  Bit-faithful (q=4 n=9/10/11 reproduce DB ~1e-9; CPU-vs-GPU 8e-10). **chi_F(q=4 n=12)=93.747642** (59.9s).
- **Finding (POTENTIALLY NOVEL, hardens S128/129 chi_F-q=4 flag):** full n=4..12 power-law alpha=1.790;
  pairwise local exp DECREASES 1.846->1.778, moving AWAY from null 2.0 (|gap| 0.154->0.222) -- wrong-sign
  for a marginal-log climb to 2. Non-circular (132d synthetic recovery: true-2.0+log gives *increasing*
  local exp; data decrease). q=3 control (132e): q=3 descends ONTO null 1.40, q=4 away from 2.0. NOT a
  refutation of 2.0 -- asymptote NOT quoted (q=3 calibrates 1/lnN extrap unreliable: fabricates -0.18 vs
  true 0). Robust claim = TREND DIRECTION only.

## CRITICAL: standing framework (unchanged, respected this sprint)
- nu(q=4)=2/3 CONFIRMED (S130 collapse) + Albuquerque 2/nu-d=2 (proven identity) => theoretical leading
  exp is **2.0**. Golden test gate enforces this; do NOT record "q=4 asymptote=1.78, reject 2" (S129).
- Use EXACT finite-diff chi_F (chif_utils canonical: per-site, factor-2, dg=1e-4, g_c=1/q). Spectral
  chi_F has neg-alpha bias (S126). All sprints 076+ are the STANDARD S_q Potts (not a novel hybrid).

## Active Research Thread
q=4 per-site chi_F: theory says leading exp 2.0; measured effective exp ~1.78 (L<=12) and its trend is
moving AWAY from 2.0, not toward it. Tension is now SHARP (was "indistinguishable" at L<=11, S129).
Resolving it needs to beat the BC problem (below) or reach L>>12.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty). ~90+ sprints unused. Strongest sim
prediction for HW: q=2 Ising chi_F at g_c on 5-10 qubits. Needs credentials restored.

## Top 3 Next Experiments
1. **Reconcile periodic-vs-open BC at q=4 (THE asymptote blocker).** Periodic exact drifts DOWN to 1.78;
   open-BC DMRG (S124) drifts UP to ~1.52 -- opposite direction AND far lower. Isolate the boundary
   contribution (open-BC exact diag at small n vs periodic; or subtract surface term) so the two BCs can
   be compared. Until reconciled the L->inf asymptote is unknowable.
2. **Cross-check the wrong-sign trend with an INDEPENDENT observable.** S130 peak-HEIGHT amplitude exp
   (1.75, also <2) already agrees; extend it + the gap/z_m decomposition to L=12 (GPU) and ask if it too
   moves away from 2. Two independent probes agreeing = robust.
3. **CHANGELOG.md compression** (511 > 300 trigger) -- compress sprints older than last ~10. Housekeeping.

## Ruled Out / Retracted
- n=13 (q=4, 67M) infeasible: int64 CSR ~42GB > 24GB GPU. n=12 is the exact-diag frontier; beyond => DMRG.
- 1/lnN / no-log extrapolations of chi_F local exp: UNRELIABLE for the asymptote (q=3 control S132
  fabricates -0.18 deficit where truth=0). Use only for trend DIRECTION. (q=5/7 RESOLVED S131; peak-SHIFT dead S130.)

## Key Tools
GPU restored: `from gpu_utils import eigsh` (auto-GPU dim>50k, cupy 13.6.0). chif_utils.chi_F_exact (canonical),
collapse_utils (S130), fss_utils, hamiltonian_utils, db_utils. Exact chi_F GPU reach: q=3 n<=14, q=4 n<=12,
q=5 n<=10. Pre-sprint BLOCKING gates: test_golden.py + db_check.py.

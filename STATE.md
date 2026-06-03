# Current State -- Rewrite this completely each sprint

## Last Sprint
Sprint 134 -- **q=4 χ_F "wrong-sign" tension RESOLVED: it was a fixed-g_c (off-peak) artifact.**
sprints/sprint_134.md (+unpublished/); results/sprint_134{a,b,c,d,e}*.json; DB chi_F_open_peak,
chi_F_periodic_peak, gstar_open, kappa_{open,periodic}_peak.
- **Falsification test of S133's "non-monotonic open κ_eff":** S132/S133 measured χ_F at the FIXED
  periodic g_c=1/q, but the finite-size χ_F PEAK sits at g*(L)≠g_c (open: far below, shift −0.097→−0.027;
  periodic: tiny −0.022→−0.0014). Re-measured at the peak (standard FSS observable), both BC, n=4..12.
- **Result OPEN:** the S133 dip+turnaround is GONE on-peak -- κ_eff rises MONOTONICALLY 0.657→1.281
  (no interior min). **RETRACT the non-monotonic-κ_eff claim.** Identity κ_fixed=κ_onpeak+d ln r/d ln L
  holds to 5e-15; the dip was entirely the off-peak penalty term.
- **Result PERIODIC:** the S132 "descent away from 2.0" is ALSO a fixed-g_c effect -- on-peak κ ASCENDS
  1.683→1.761 toward 2.0 while fixed-g_c descends 1.86→1.78.
- **VALIDATION (linchpin):** q=2,3 (no marginal op) PERIODIC on-peak ascends-from-below to the exact null
  while fixed-g_c descends-from-above to the SAME null (q=2:1.022/1.072→1.0; q=3:1.414/1.444→1.4). So a
  descending fixed-g_c κ is NOT evidence of a sub-null asymptote; q=4's on-peak↑/fixed↓ share dest 2/ν−d=2.0.

## CRITICAL: standing framework (unchanged hard answer, cleaner evidence now)
- nu(q=4)=2/3 CONFIRMED (S130) + Albuquerque 2/ν−d=2 (proven) => leading exp is **2.0**. Golden gate
  enforces this; never record "q=4 asymptote=1.78, reject 2".
- Canonical χ_F = chif_utils (per-site, factor-2, central dg=1e-4). **NEW S134 rule:** when a BC shifts the
  pseudo-critical point (esp. OPEN), evaluate χ_F effective exponents AT the peak g*(L), not at fixed g_c --
  fixed-g_c adds a moving off-peak-penalty term that flips the apparent drift direction.

## Active Research Thread
q=4 per-site χ_F asymptote. The standard peak-height estimator ASCENDS toward 2.0 for BOTH BC (S134),
same validated direction as q=2,3 toward their exact nulls -- the S129–S133 "evidence against 2.0" was a
fixed-coupling artifact. Asymptote still NOT numerically pinned at L≤12 (q=4 on-peak ~1.76 periodic / 1.28
open; marginal-log slow). To pin it: reach L≫12 at the peak.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty). ~90+ sprints unused. Strongest sim
prediction for HW: q=2 Ising χ_F at g_c on 5-10 qubits. Needs credentials restored.

## Top 3 Next Experiments
1. **Periodic DMRG AT THE PEAK past L=12.** Now that on-peak is the right observable and ascends toward 2.0,
   extend periodic on-peak χ_F to L=16-30 via TeNPy (locate g*(L), peak-height). Does κ_onpeak keep climbing
   past 1.76 toward 2.0? This is the cleanest path to finally pinning (or bounding) the asymptote.
2. **Second on-peak observable.** Peak-HEIGHT amplitude exponent (S130 a=1.75) and the peak CURVATURE both
   ~L^{2/ν−d}; check they ascend consistently with κ_onpeak (independent cross-check at n≤12, cheap).
3. **CHANGELOG.md compression** (~445 > 300). Compress sprints older than last ~10 to one-liners. Housekeeping.

## Ruled Out / Retracted
- **S133 "open κ_eff non-monotonic (dip+turnaround)"** -- RETRACTED (S134): off-peak (fixed-g_c) artifact;
  on-peak is monotone. **S132 "periodic descends AWAY from 2.0 (wrong-sign)"** -- CORRECTED (S134): on-peak
  ascends toward 2.0; fixed-g_c descent is not evidence against the null (q=2,3 fixed-g_c descend TO null).
- n=13 (q=4, 67M) exact-diag infeasible (int64 CSR ~42GB > 24GB GPU). n=12 is the exact-diag frontier => DMRG.
- 1/lnN extrapolations of χ_F local exp for the asymptote: UNRELIABLE (S132 q=3 control). Naive geometric
  increment extrapolation likewise underestimates (marginal log). Direction, not value, is the robust signal.

## Key Tools
GPU: `from gpu_utils import eigsh` (auto dim>50k, cupy 13.6.0). chif_utils.chi_F_exact (canonical, FIXED g);
for on-peak use a g-sweep + parabola vertex (see exp_134a). collapse_utils (S130), fss_utils,
hamiltonian_utils (`_decode_states`,`_build_field`; open=drop wrap bond), db_utils. Exact χ_F GPU reach:
q=3 n<=14, q=4 n<=12, q=5 n<=10. Pre-sprint BLOCKING gates: test_golden.py + db_check.py. python = system
Python311 (NOT ~/quantum-env venv, which lacks numpy).

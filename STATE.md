# Current State -- Rewrite this completely each sprint

## Last Sprint
Sprint 133 -- **Reconciled periodic vs open BC for q=4 chi_F (canonical convention, n=4..12).**
sprints/sprint_133.md (+unpublished/); results/sprint_133{a,b}*.json; DB chi_F_open_exact n=4..12.
- **Pre-sprint audit caught a convention bug:** prior open data (S113/124 `chi_F_open`) used forward
  diff/dg=1e-3/no-factor-2; periodic used canonical central/dg=1e-4/factor-2. The "1.78 vs 1.52" was
  never apples-to-apples. Recomputed OPEN with the IDENTICAL canonical estimator to n=12.
- **Result 1:** BC gap is REAL (convention-independent): open kappa_eff(n=12)=1.537 vs periodic 1.778.
- **Result 2 (NEW, POTENTIALLY NOVEL, hardens S128/129/132 flag):** open kappa_eff is NON-MONOTONIC --
  minimum 1.520 at n~7.5 then ACCELERATING climb (post-min increments grow +0.0023->+0.0054). S124 DMRG
  saw only the rising tail; canonical exact-diag reveals the full dip+turnaround. Periodic = decelerating
  descent (decrements shrink geometrically x0.56) toward apparent plateau ~1.776.
- **Reconciliation:** ratio chi_O/chi_P decreases AWAY from 1 => vanishing 1/L boundary REFUTED, BC don't
  converge by n=12, joint shared-bulk fit non-identifiable (S132 degeneracy stands). BUT the open
  turnaround NEUTRALIZES the S132 "wrong-sign descent vs 2.0" argument: a finite-window apparent plateau
  demonstrably reverses (open did it), so periodic's descent to ~1.78 is NOT evidence against 2.0.

## CRITICAL: standing framework (unchanged, respected this sprint)
- nu(q=4)=2/3 CONFIRMED (S130 collapse) + Albuquerque 2/nu-d=2 (proven identity) => theoretical leading
  exp is **2.0**. Golden test gate enforces this; do NOT record "q=4 asymptote=1.78, reject 2".
- Canonical chi_F = chif_utils (per-site, factor-2, central dg=1e-4, g_c=1/q). ALWAYS use this convention
  for BOTH BC now (S133 fixed the open mismatch). S_q standard Potts, sprints 076+.

## Active Research Thread
q=4 per-site chi_F asymptote. Theory=2.0; measured effective exps in window: periodic 1.78 (descending),
open 1.53 (dipped@n~7, now climbing). NEITHER is asymptotic at L<=12. Tension is no longer "wrong-sign"
(S133 defused it) but ALSO not resolved: 2.0-with-logs and a sub-2 plateau remain degenerate. Need L>>12.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty). ~90+ sprints unused. Strongest sim
prediction for HW: q=2 Ising chi_F at g_c on 5-10 qubits. Needs credentials restored.

## Top 3 Next Experiments
1. **Does periodic also turn around?** Push periodic toward its predicted minimum. Exact-diag dead at
   n=13 (67M > 24GB). Options: (a) periodic DMRG (hard, chi^2 cost) at n=14-24 to extend the periodic
   series past 12 and look for the κ_eff minimum the reconciliation predicts; (b) q=4 chi_F with a
   2nd independent observable (peak-HEIGHT amp exp, S130=1.75) extended to n=12 -- does it ALSO dip+rise?
2. **Locate the open turnaround mechanism.** Open evaluated at periodic g_c=1/q is OFF the open chain's
   own pseudo-critical peak. Re-measure open chi_F at the open-chain peak g*(L) (cheap g-sweep, n<=10):
   does evaluating on-peak remove the dip or shift it? Distinguishes "boundary" from "off-peak" cause.
3. **CHANGELOG.md compression** (438 > 300 trigger) -- compress sprints older than last ~10. Housekeeping.

## Ruled Out / Retracted
- n=13 (q=4, 67M) infeasible: int64 CSR ~42GB > 24GB GPU. n=12 is the exact-diag frontier => DMRG beyond.
- Open chi_F "drifts up monotonically" (implied by S124 DMRG): WRONG -- it DIPS to a min at n~7.5 first
  (S133 canonical exact-diag); DMRG started at n=6 and missed the descent.
- Shared-bulk + multiplicative-1/L-boundary model for q=4 BC: REFUTED (ratio moves away from 1, S133).
- 1/lnN extrapolations of chi_F local exp for the asymptote: UNRELIABLE (S132 q=3 control). Trend only.

## Key Tools
GPU: `from gpu_utils import eigsh` (auto dim>50k, cupy 13.6.0). chif_utils.chi_F_exact (canonical),
collapse_utils (S130), fss_utils, hamiltonian_utils, db_utils. Exact chi_F GPU reach: q=3 n<=14, q=4
n<=12, q=5 n<=10. Pre-sprint BLOCKING gates: test_golden.py + db_check.py. python = system Python311
(NOT the ~/quantum-env venv, which lacks numpy); science stack is in Python311.

# Current State -- Rewrite this completely each sprint

## Last Sprint
Sprint 129 -- AUDIT (user-requested external scrutiny). Machinery verified sound: g_c=1/q is exact
self-dual (to 1e-15); finite-diff chi_F good to ~5 sig figs (dg=1e-4 bias shifts alpha by 5e-6); AIC
procedure recovers truth in synthetic tests. But the q=4 HEADLINE WAS INVERTED -- see below. Full
report: sprints/sprint_129_audit.md.

## CRITICAL: q=4 framing corrected (Sprint 129)
We measure PER-SITE chi_F, whose correct leading exponent at a QCP is 2/nu - d (Albuquerque et al.,
PRB 81 064418, Eq.21). 4-state Potts nu=2/3 => **2/nu-d = 2.0 is the CORRECT answer, not a hypothesis
to reject.** Our own q=3 anchor confirms the convention: nu=5/6 => 2/nu-d = 7/5 = 1.40 (our "exact"
q=3 value). Measured q=4 = 1.77 is the FINITE-SIZE value below 2; q=4 has the marginal operator =>
slow log-corrected approach to 2 (q=3 has none => converges cleanly).
- exp_128c extrapolation "ruling out 2" is CIRCULAR: its no-log ansatz returns 1.60-1.89 when fed
  true alpha=2-with-logs data. Retired as evidence.
- "Salas-Sokal p=3/2" was MISLABELED: 3/2 is the 2D-classical specific-heat log power, not a chi_F
  prediction. Drop the comparison.
- At L<=11 (ln N x1.73) data CANNOT distinguish "1.77 forever" from "2 with marginal logs."
  Open-BC DMRG drifts UP toward 2.

## CRITICAL: Standing corrections
Use EXACT finite-difference chi_F (spectral has negative-alpha bias, S126). All sprints 076+ use the
STANDARD S_q Potts model (not a novel hybrid; Apr 2026 audit). See KNOWLEDGE.md.

## Active Research Thread
**S_q q=4: is the per-site exponent the expected 2 (with marginal logs) or a true sub-2 value? --
UNRESOLVED at accessible sizes.** Authoritative exact-chi_F effective exponents (n<=11):

| q | nu | expected 2/nu-d | measured | status |
|---|----|-----------------|----------|--------|
| 3 | 5/6 | 1.400 | 1.41->1.407 | Converged (no marginal op) |
| 4 | 2/3 | 2.000 | ~1.77-1.79 | Finite-size below 2; needs L>>11 |
| 5 | -- | (walking) | 2.094 / 2.139* | *INCONSISTENT -- reconcile |
| 6 | -- | (walking) | 2.375 | increasing |
| 7 | -- | (walking) | 2.58-2.64 | increasing |

## QPU Budget
580s remaining -- BLOCKED (qiskit-ibm.json empty).

## Top 3 Next Experiments
1. **Resolve q=4: periodic-BC chi_F at L>>11.** Only larger sizes distinguish 2-with-logs from sub-2.
   Symmetry-reduced ED or periodic DMRG. Fit chi_F = A*N^2*(ln N)^{-p}*(1+c/N^2) (needs n>=12).
2. **Reconcile q=5 alpha** (2.094 vs 2.139) -- trace which sizes/fit produced each, pick one.
3. **Fix results.db factor-2 split** -- absolute chi_F pre/post S125 differ x2; choose canonical
   convention and annotate (exponents unaffected).

## What's Been Ruled Out / Retracted
- ~~"q=4 alpha=1.77 asymptotic, Salas-Sokal rejected"~~ -- INVERTED (S129). 2 is correct; 1.77 is finite-size.
- ~~exp_128c power-law extrapolation as evidence against logs~~ -- circular (S129).
- Spectral chi_F as primary method (S126); alpha(q)=1.86 ln q-0.96 (S127); iDMRG overlap for S_q (S124).

## Key Literature
- **Albuquerque, Alet, Sire, Capponi, PRB 81 064418 (2010):** chi_F density ~ L^{2/nu-d}. THE correct null.
- **Salas & Sokal (1997):** 2D CLASSICAL Potts; p=3/2 is SPECIFIC HEAT (chi log power is 1/8). Not chi_F.
- Jacobsen-Wiese, Ma-He, GRZ: standard S_q Potts exponents.

## Key Tools
- Exact chi_F (periodic): q=3 n<=14, q=4 n<=11, q=5 n<=10, q=6 n<=9, q=7 n<=8
- chi_F DMRG (open BC): q=2 n<=24, q=4 n<=20; hamiltonian_utils.py, fss_utils.py, gpu_utils.py
- IBM QPU: 580s remaining (credentials needed)

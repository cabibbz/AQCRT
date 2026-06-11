# Current State -- Rewrite this completely each sprint

## Last Sprint
**Sprint 140 — VELOCITY TEST: both registered hypotheses REFUTED; S139 interpretation
downgraded; a two-length structure discovered.** sprints/sprint_140.md (+unresolved/).
- Direct ξ_x (Z_q-DMRG correlator, OZ, disordered branch, size-converged n=48→64 to 1%):
  **ξ_x(q=10 at g_c) ≲ 4.3 sites** (2.2 at g=0.103; exact-g_c value carries a tower-admixture
  caveat). ED dispersion cross-check (charge-resolved blocks — plain ⟨P⟩ filtering FAILS near
  coexistence, Lanczos mixes the degenerate tower): band nearly flat, v/Δ~0.9, order-consistent.
- NOT 10.6 (H_A amplitude reading), NOT 21 (H_B rescaled duality). σ̃·ξ_x = 0.05-0.10 — no
  special value. **S139's "σ̃=σ_od/2 amplitude" reading: units-blind → downgraded to OPEN**
  (addendum in sprint_139.md). The numerical match σ̃=0.02367 vs σ_od^cl/2=0.02368 stands as an
  unexplained, possibly numerological coincidence at ONE q.
- **What survives (untouched):** Λ_Im = (1.65±0.09)·ξ_d^cl(q) blind-confirmed; all coexistence
  phenomenology ordered by the exact classical ξ_d. New puzzle: the quantum first-order point
  carries TWO decoupled lengths — microscopic ξ_x (2-4 sites) vs tunneling scale Λ (~17 sites,
  ∝ classical ξ_d). Classically these are LOCKED (σ_od·ξ_d=1/2); quantum-side they are not.

## CRITICAL: standing framework
- χ_F null = 2/ν−d (proven, golden-gated); q=4 marginal-log: q4-vs-q3 deficit contrast.
- Walking: shadow exponents valid ONLY at q=5; crossover onset Λ_Im≈1.65ξ_d^cl (blind, S138);
  asymptotic decay rate σ̃·ξ_d^cl = 1/4 at q=10 (S139, MEASURED) — interpretation OPEN (S140).

## Active Research Thread
The σ̃·ξ_d^cl=1/4 law-or-coincidence question + the two-length puzzle. ONE decisive experiment:

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty; needs human). Log predictions only.

## Top 3 Next Experiments
1. **q=8 asymptotic universality check (THE decisive test):** extend q=8 to n=44,48,52
   (L/ξ=1.8-2.2; ~3-5h/size, chi 128-160) → tail σ_loc·ξ_d^cl plateau. If it also flattens at
   ~1/4: σ̃·ξ_d^cl=1/4 is a LAW of the quantum-classical correspondence (publishable mystery,
   theory needed). If not: S139's 1/4 was accidental and dies. Registered prediction BEFORE
   running: under "law", plateau at 0.25±0.04 setting in by L/ξ≈2.
2. **ξ_x(q) mini-survey** (cheap): repeat exp_140a at q=7,8 (g_c+0.003 clean points, n=48) —
   does ξ_x(q) ALSO scale ∝ ξ_d^cl(q) (with small coefficient ~0.2-0.4), or is it q-flat?
   Distinguishes "uniform length compression" from "genuine decoupling".
3. **Write-up sprint** (S136-140 arc): now even better shaped — estimator → crossover + control
   → blind prediction → asymptotic constant → two-length puzzle. Draft in unresolved/.

## Ruled Out / Retracted (recent)
- S139 amplitude-factor duality INTERPRETATION (S140; measured laws unchanged).
- H_B rescaled-duality (ξ_x≈2ξ_d^cl): off by ≥5x.
- Plain ⟨P⟩ charge filtering near phase coexistence (Lanczos tower mixing) — use exact charge
  BLOCKS in the Fourier basis (exp_140b pattern).
- ξ=v/Δ from coarse-k dispersion when the band is flat (deep first-order): use the direct
  correlator (OZ-corrected).

## Key Tools
exp_140a (direct ξ_x via Z_q-DMRG correlator + OZ fit; ~10 min/point at n=64 chi=64).
exp_140b (charge-resolved periodic ED blocks: exact charge sectors + momentum via ⟨T⟩ + tower
ID via field expectation — the robust pattern near coexistence). zq_dmrg_utils; exp_137a/b
harnesses (SPRINT_NO env). Gates: test_golden 18 + db_check A/B/D pre+post via loop.sh.
python = system Python311; CuPy PINNED 13.6.0. Novel-findings dir renamed: **unresolved/**
(was unpublished/; 2026-06-11, all references updated).

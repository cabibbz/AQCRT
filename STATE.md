# Current State -- Rewrite this completely each sprint

## Last Sprint
**Sprint 141 — q=8 UNIVERSALITY TEST: the 1/4 constant RECURS. Law, not numerology.**
sprints/sprint_141.md (+unresolved/). Extended q=8 to n=36,40,44,48 (L/ξ=2.01; ~10.5h).
- **P1 (registered, fit-free) PASSED:** σ_loc·ξ_d^cl tail-window mean (L/ξ≥1.3) = **0.256**
  vs q=10 plateau **0.259** — same plateau to 1% across ξ differing 2.26x; the L/ξ≈2 window
  reads 0.277 ∈ 0.25±0.04 as predicted.
- **P2:** q=8-only tail fit UNDERPOWERED (4 pts, s=0.71±0.52 — admitted). **Joint q=8+q=10
  tails, shared s = 0.213 ± 0.029:** 1/4 inside 1.3σ; s=0.40 excluded 6.4σ; s=0.50 excluded
  9.9σ. Precision caveat: whether the shared constant is exactly 1/4 or ~0.21-0.25 is open;
  its q-INDEPENDENCE and scale are established.
- **Standing puzzle (the project's sharpest):** the quantum OBC tunneling rate locks to half
  the exact classical Borgs-Janke tension per CLASSICAL ξ_d, across q — while the quantum
  chain's own ξ_x is 2-4 sites and decoupled (S140), and both duality explanations are
  experimentally removed (S139/S140). No mechanism known.

## CRITICAL: standing framework
- χ_F null = 2/ν−d (proven, golden-gated); q=4 marginal-log: q4-vs-q3 deficit contrast.
- Walking arc: shadow exponents valid ONLY at q=5; crossover onset Λ_Im≈1.65ξ_d^cl (blind,
  S138); **asymptotic σ̃·ξ_d^cl = 0.24±0.03 at BOTH q=8 and q=10 (S139+S141) — q-independent,
  mechanism unknown**; quantum ξ_x decoupled (2-4 sites, S140).

## Active Research Thread
S136-141 arc COMPLETE as an experimental program. The mystery constant is theory-shaped.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty; needs human). Log predictions only.

## Top 3 Next Experiments
1. **WRITE-UP SPRINT (now clearly the highest value):** the S136-141 arc is a complete,
   self-contained experimental story (validated EP estimator → crossover + null control →
   blind Λ∝ξ prediction → asymptotic constant → velocity test removing explanations → two-q
   universality). Draft a paper-style manuscript in unresolved/ with 3-4 figures (matplotlib;
   data all in results/*.json + DB).
2. **Theory probe of the 1/4:** small dedicated study — compute the quantum chain's OWN
   order-disorder interface free energy directly (e.g., fixed-BC DMRG: disordered left edge /
   ordered right edge, ground-energy excess vs n → σ_interface^quantum) and compare to σ̃ and
   to σ_od^cl. Could identify WHERE the classical normalization enters.
3. **ξ_x(q) mini-survey** (cheap, supports #2): exp_140a at q=7,8 → is ξ_x ∝ ξ_d^cl with small
   coefficient, or q-flat? Distinguishes uniform compression vs genuine decoupling.

## Ruled Out / Retracted (recent)
- "S139's 1/4 is numerology" — KILLED by S141 (recurs at q=8 to 1%).
- S139 amplitude-duality reading (S140); naive duality (S139); plain ⟨P⟩ filtering near
  coexistence; ξ=v/Δ on flat bands; <7-point hyperbola fits; importing exp scripts.

## Key Tools
exp_137a/b harnesses (SPRINT_NO env; per-size cost q=8 n=48 chi=128 ≈ 2.9h). exp_141a
(universality verdict: plateau windows + joint shared-s tails). exp_140a (direct ξ_x),
exp_140b (charge-resolved ED blocks). zq_dmrg_utils. Gates: test_golden 18 + db_check A/B/D
pre+post via loop.sh. python = system Python311; CuPy PINNED 13.6.0. Novel findings →
unresolved/ (renamed from unpublished/ 2026-06-11).

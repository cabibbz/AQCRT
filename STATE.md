# Current State -- Rewrite this completely each sprint

## Last Activity
**SYSTEM AUDIT 2026-06-09** (between sprints): 48-agent deep audit; 29 confirmed findings, all
fixed. Full report sprints/audit_2026-06-09.md. Code: gpu_utils ordering trap, fss_utils r²,
exp_136b 2x-diagonalization + edge-clamp, collapse_utils half-convention, db_utils canonicalization
+ newest-wins query, format_stream crash path. DB migrated (one spelling per model family; S84
c_eff retagged). Gates upgraded: golden 11→18 checks (EP anchors via NEW experiments/ep_utils.py,
hybrid anchor, GPU/CPU parity); db_check fails on fragmentation/new method conflicts; loop.sh
gates now run pre+post sprint, halts after 2 consecutive claude failures, auto-pushes.
Sprint 136 before that: thermal-gap EP estimator of 1/ν (see KNOWLEDGE.md, now audit-hedged).

## CRITICAL: standing framework (audit-hedged wording — use THIS framing)
- Per-site χ_F null exponent = 2/ν−d (proven, golden-gated). q=4: collapse 1/ν=1.45-1.49,
  consistent with exact ν=2/3 ⇒ asymptote 2.0; finite-size values sit below it.
- q=4 marginal-log: q4-vs-q3-control DEFICIT CONTRAST (0.30 vs 0.00) is the robust datum; "log
  detected" is conditional on the 2.0 asymptote. EP estimator is NOT χ_F-independent
  (χ_F^peak·Im² ≈ const ~2% — single-multiplet dominance; that constancy IS the result).
- Walking q≥5: 1/ν_eff 1.51/1.65/1.78 = "consistent with complex-CFT shadow", NOT established.
  PRELIMINARY Re(1/ν_complex)=1.534/1.563/1.588 (q5/6/7) — q6,7 measured values rise PAST it.

## Active Research Thread
Walking crossover hunt, RETARGETED (audit): exact ξ_d = 2512/159/48/24/10.6 for q=5/6/7/8/10 —
q=5,6 unreachable at DMRG n≤40; **q=8-10 is where L~ξ is bracketable**.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty; needs human). Log predictions only.

## Top 3 Next Experiments
1. **Sprint 137: Z_q-conserving DMRG thermal-gap EP at q=8,10 (+q=6 shadow control), n≈8-32.**
   Charge-0 ground + first-excited (orthogonal_to) in a Z_q-charge MPS (Fourier basis: field
   diagonal −g(qδ_{m,0}−1); coupling = (1/q)Σ_k Z_i^k Z_j^{-k}, TeNPy 1.1 site smoke-tested).
   Validate vs ED at n≤7. Hunt the power-law→steeper crossover of Im(g_EP) near L~ξ (24 / 10.6).
2. **Jacobsen-Wiese comparison done properly** (Coulomb-gas continuation, validate on q≤4 exact)
   → does 1/ν_eff(q) track Re(1/ν_complex) or cross toward d=2? Discriminates shadow vs crossover.
3. **S135 rigor: chi-doubling check** (q=4 & q=3, n=24, chi 48→96, svd 1e-9; expect <0.1% move).

## Ruled Out / Retracted (recent)
- "Two INDEPENDENT observables agree" (S136 wording) — near-tautological, hedged (audit).
- "ξ>12" as walking budget anchor — exact ξ values above; q=5,6 DMRG crossover hunt infeasible.
- Pre-data guess "walking ⇒ Im(g_EP) plateau γ>0" — wrong (sat-fit γ≈0 ∀q, γ at fit bound).
- Naive 1/lnL extrapolation of OPEN-BC κ_eff; wide-window eigsh scans into ordered phase (stall).

## Key Tools
experiments/ep_utils.py (EP estimator, shared w/ golden gate) | exp_136b (production imEP, arg=q)
| chif_utils.chi_F_exact | DMRG: exp_135a/b (SqPottsChain, TRIVIAL legs — S137 needs the NEW
Z_q-charge site) | db_utils (canonicalizes models, query=newest-wins) | fss_utils | gates:
test_golden.py (18 checks) + db_check.py (A drift/B fragmentation/D method-conflicts), run
pre+post sprint by loop.sh. python = system Python311; CuPy PINNED 13.6.0 (no v14).

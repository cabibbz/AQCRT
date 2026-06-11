# Changelog — Quantum Explorer

## QPU Budget
- Used: 20s of 600s (Sprint 025)
- Remaining: 580s (BLOCKED — credentials file empty; needs human)

## Sprint 140 -- Velocity test: BOTH hypotheses refuted; S139 interpretation downgraded; two-length structure found
The S139 "σ̃ = σ_od/2 (amplitude factor)" reading required the quantum chain's own spatial correlation length ξ_x to be ~ξ_d^cl=10.56 (H_A) -- or ~2ξ_d^cl=21 for the rescaled-duality alternative (H_B). Registered both BEFORE measuring. **exp_140a (direct):** Z_q-DMRG disordered-branch correlator C(r)=⟨Z1_i Z1d_j⟩ at the transition, OZ-corrected fits, n=48 and 64 (size-converged to 1%): **ξ_x(g_c) ≲ 4.3 sites** (exact-g_c value is an upper estimate -- local-ξ drift from tower admixture at coexistence; clean nearby points: 2.15 at g=0.103, 1.65 at g=0.106). **exp_140b (cross-check):** charge-RESOLVED periodic ED (exact charge blocks in the Fourier basis -- the plain ⟨P⟩-filter approach FAILS near coexistence because Lanczos mixes the near-degenerate ordered tower across charge sectors; ordered intruder identified by field expectation and excluded): magnon band nearly FLAT at small k (deep first-order ≈ product state), so ξ=v/Δ (~0.9) is order-consistent but unreliable -- the correlator is authoritative. **VERDICT: H_A NO, H_B NO; σ̃·ξ_x = 0.05-0.10, no special value.** The S139 amplitude interpretation was units-blind (compared per-site vs per-classical-unit tensions without shared normalization) -- DOWNGRADED to open question via addenda in sprint_139.md; the eerily exact numerical identity σ̃=0.02367 vs σ_od^cl/2=0.02368 stands unexplained at one q. **What survives untouched:** Λ_Im=(1.65±0.09)ξ_d^cl (blind-confirmed S138) and all measured S139 facts. **The real finding: a two-length structure at the quantum first-order point** -- microscopic ξ_x (2-4 sites) decoupled from the tunneling scale Λ (~17 sites ∝ classical ξ_d), whereas classically duality+wetting LOCK them (σ_od·ξ_d=1/2). Decisive next test queued and registered: does σ̃(q=8)·ξ_d^cl(8)=1/4 recur (law) or not (numerology)? DB: xi_x_disordered, v_magnon, gap_disordered, xi_x_from_vgap. unresolved/sprint_140.md. (Also this date: unpublished/ renamed unresolved/ repo-wide.)

## Sprint 139 -- Interface-tension test: asymptotic gap decay = σ_od/2 (naive duality transfer EXCLUDED)
Resolved the S138 bonus observation (ξ/Λ_Dm ≈ 0.40 const). Exact theory anchor: Borgs-Janke duality+wetting gives **2σ_od = 1/ξ_d exactly** for the 2D classical Potts model (MC-verified at q=10: 2σ_od=0.094701=1/10.56). Registered hypotheses BEFORE fitting: H_dual σ̃ξ=1/2 (naive transfer), H_2int σ̃ξ=1, H_onset σ̃ξ≈0.40. Extended q=10 to n=32,36 (L/ξ=3.03,3.41; 3.2h/size at chi=128; n=36 hyperbola relres 3.8e-4; DB rows sprint=139, accumulate-file seeding documented in results/sprint_139b_crossover_q10.json). **Verdict (exp_139a, joint fit ln Δm = lnA_q − a lnL − (s/ξ_q)L over q=6,7,8,10, 32 pts):** s=1/2 EXCLUDED (dAIC +135 joint, +16.8 q=10-tail-only; the local rate σ_loc·ξ flattens at 0.23-0.27 over L/ξ=2.5-3.4 where H_dual demands 0.51-0.55); s=0 excluded (+141); **q=10 tail s = 0.213±0.035, and s≡1/4 fits as well as the free fit (dAIC −0.1)**. Interpretation: the avoided-crossing gap is a tunneling AMPLITUDE, classical interface free energy suppresses the WEIGHT ∝ amplitude² ⇒ **Δ_min ~ (1/L)·e^{−σ_od L/2} ⇒ σ̃·ξ_d = 1/4** (prefactor a≈0.9-1.0 across q). Caveat flagged honestly: the τ-continuum velocity factor is not independently fixed (v(q=10) measurement queued). Reconciliation: S137/138's Λ_Dm≈2.5-2.7ξ is the crossover-ONSET law (what the blind q=7 prediction tested — unchanged); the asymptotic constant is Λ_∞=4ξ, with the flow between them visible in windowed fits. POTENTIALLY NOVEL (sharp, exact-anchored): first quantum-chain measurement of this asymptotic constant; CNPV 1410.8662 established exponential closing, the σ_od/2 identification vs the exact value appears new. The S136→139 arc is now complete: estimator → crossover+null control → blind Λ∝ξ prediction → exact-anchored asymptotics. DB: sigma_xi_product; unresolved/sprint_139.md.

## Sprint 138 -- Λ ∝ ξ CONFIRMED: the q=7 blind prediction test lands dead center
The S137 crossover law made a registered, parameter-free prediction (written into sprints/sprint_138.md BEFORE any q=7 data): with ξ_d(q=7)=48.1 exact, **Λ_Im = 1.65ξ = 79±5 and Λ_Dm = 2.61ξ = 126±7**, plus three falsifiers (wrong-scale Λ, no decay despite the q=8 matched-window calibration, broken Λ_Dm/Λ_Im ratio). Ran the validated harness (exp_137a/b with new SPRINT_NO provenance env): q=7 ED validation worst rel 1.1e-6; production n=8..40 (10 sizes, every size refined to ≥7 fit points, chi 64/96/128, ~6.5h; Δm·L 2.17→1.84). **Result (exp_138a): Λ_Im = 79 ± 25 — the predicted central value to 0.4% (1.64ξ vs 1.65ξ predicted); Λ_Dm = 118 ± 24 (0.3σ from 126).** The decay term is independently demanded by the data (dAIC +13.0 Δm / +7.0 Im vs pure power), and the T2 variant — Λ FIXED at the predicted value, zero extra parameters — still beats pure power by +14.9/+9.0, so the prediction itself does explanatory work. Matched-window calibration: q=8 restricted to L/ξ≤0.84 gives dAIC +12.5 (Δm) vs q=7's +13.0 — exactly the expected signal strength. Internal ratio Λ_Dm/Λ_Im = 1.50 (q=8: 1.58, q=10: 1.59). All three falsifiers evaded. **The crossover law Λ_Im ≈ 1.65 ξ_d now spans q=7,8,10 (ξ from 10.6 to 48.1, a 4.6x range) with the q=7 point earned blind — S137's POTENTIALLY NOVEL upgraded to CONFIRMED** (novelty-hardening #1: 10 sizes; #2: two series Δm+Im; #3: falsification test passed as registered prediction). Honest caveat: the Im channel's matched-window q=8 calibration is weak (+0.8) — the conclusion rests primarily on the cleaner Δm channel, Im concurring. Bonus observation logged: σ_eff·ξ_d = ξ/Λ_Dm ≈ 0.41/0.40/0.37 at q=7/8/10 — near-constant, smells like an exact interface-tension/ξ duality relation (queued). DB: crossover_Lambda (q=7 both channels w/ prediction noted), im_gEP_open/thermal_gap_min_open/gstar_thermal_open q=7 n=8..40, zq_dmrg_validation_worst_rel. unresolved/sprint_138.md.

## Sprint 137 -- WALKING CROSSOVER OBSERVED: Im(g_EP) leaves the conformal shadow at Λ ∝ ξ (Z_q-conserving DMRG, audit-retargeted)
The audit retarget paid off in one sprint. **NEW experiments/zq_dmrg_utils.py:** Z_q-charge-conserving DMRG in the Fourier (charge) basis — field term diagonal −g(qδ_{m0}−1), coupling (1/q)ΣZk_i Zkd_j (real permutation ops); charge-0 ground + first excited via TeNPy `orthogonal_to` (KEYWORD-ONLY constructor arg in 1.1 — silently ignored as an options key, the first failure mode found); validated vs open-BC ED at q=6/8/10 to worst rel 3.1e-4 (chi=64; exp_137a). **Production (exp_137b):** thermal-gap avoided crossing fitted with the ASYMMETRIC 2-level form Δ=sqrt(Δm²+(c1δ+c2δ²)²) (open-chain wings have unequal slopes; the symmetric form left 20% residuals), Im(g_EP)=Δm/c1; refinement until ≥7 fit points AND relres<5e-3 (a 4-param fit through ~5 points passes any residual gate while hiding 5-18% parameter noise — caught by re-measurement); n=8..28 at q=8,10, n=8..24 control at q=6. **Result (exp_137c):** both Δ_min(L) and Im(g_EP)(L) require an exponential factor beyond the shadow power law — A·L^{−p}e^{−L/Λ} beats pure power by dAIC +16.8/+37.4 (Δm, q=8/q=10) and +11.2/+31.4 (Im) — exactly and only where L crosses the EXACT classical ξ_d (Buffenoir-Wallon: 23.9, 10.56); the q=6 control (ξ=158.9) needs none (dAIC≈0, Δm·L flat ≈2.4). **Λ tracks ξ: Λ_Im=1.59ξ/1.71ξ, Λ_Dm=2.51ξ/2.71ξ across a 2.26x change in ξ.** q=10 local slopes run away −1.80→−2.64 (monotone). Truncation artifacts excluded by the control (same chi ladder 64/96/128) + slope smoothness across tiers. **Coulomb-gas comparison (closes the audit question):** den Nijs continuation (exact on Q≤4) gives Re(1/ν_complex)=1.534/1.563/1.588/1.609/1.646 (q=5..8,10); S136's effective 1/ν matches ONLY at q=5 (1.505) — q=6,7 (1.648/1.775) rise past it toward d=2, so the "conformal shadow" reading is licensed only at q=5. **S135 rigor closed (exp_137d):** chi-doubling 48→96 at n=24 moves chi_F by 3.1e-8 (q=3) / 5.0e-5 (q=4) — S135 production was converged. DB: im_gEP_open/thermal_gap_min_open/gstar_thermal_open (BC-qualified per audit rule), crossover_Lambda, inv_nu_complex_re, chi_F_open_peak_chi96, zq_dmrg_validation_worst_rel. Ops notes: TeNPy max_trunc_err hard-error disabled (ED-validated accuracy); one JSON record (q=10 n=28) briefly lost to a parallel-invocation write race, restored from results.db + log, save() now merge-on-saves. POTENTIALLY NOVEL (strongest yet): first quantum-chain EP-observable measurement of the walking→first-order crossover with Λ ∝ ξ_d(exact) and a null control. unresolved/sprint_137.md.

## SYSTEM AUDIT 2026-06-09 (between sprints 136 and 137) — 29 confirmed findings fixed
48-agent multi-dimension audit (code, data, docs, infra, science; every medium+ finding adversarially verified). **Code fixes:** gpu_utils.eigsh now returns ASCENDING eigenvalues on BOTH backends when return_eigenvectors=False (was CPU-descending/GPU-ascending — a silent sign-flip trap at the 50k threshold); fss_utils.fit_power_law r² computed from unweighted residuals + scale_covar=False when errors given (was returning r²=-334 on good fits); exp_136b gap_curve diagonalizes ONCE per g (was 2x GPU cost) and fails loudly on window-edge minima (was silently fitting a parabola around a non-minimum); collapse_utils.scan_curve raised to the canonical factor-2 chi_F convention (was exactly half; exponents unaffected); format_stream.py no longer crashes on valid-JSON non-dict lines. **NEW experiments/ep_utils.py:** the S136 EP estimator extracted into one shared implementation. **DB migration:** model spellings canonicalized (sq/S_q_potts/S_q_Potts→sq_potts 469 rows, hybrid_2D→hybrid_2d; db_utils.record() canonicalizes on write); S84 'c_eff' retagged c_eff_spectrum_s084 (was an incompatible observable under the same key, 7x scale); query() now orders sprint ASC so dict-comprehension consumers get newest-wins (was silently oldest-wins); S135 svd notes metadata corrected. **Gates upgraded:** test_golden 11→18 checks (frozen EP anchors q=2 n=6/8/10 via ep_utils, hybrid-builder anchor 13.064844, GPU/CPU parity at dim 65536); db_check now FAILS on model fragmentation and on NEW (sprint≥137) cross-method >1% conflicts; loop.sh runs gates pre+POST sprint (corruption was previously caught one sprint late, after push), halts on 2 consecutive claude failures, auto-pushes unpushed commits at sprint start, MODEL env var. **Docs:** TASK.md environment rewritten (Windows/Python311, CuPy PINNED 13.6.0 — the doc previously instructed installing CuPy 14, the exact version that caused the S129-131 GPU outage; util paths fixed to experiments/; IBM-credentials BLOCKED note; gates documented). **Science hedges (KNOWLEDGE.md/STATE.md rewritten, ARCHIVE holds detail):** (1) S136 "two INDEPENDENT observables agree" was near-tautological — chi_F^peak·Im(g_EP)²≈const (~2%, single-multiplet dominance) ties them by construction; the product-constancy is the actual result. (2) S135 "marginal log detected" is conditional on the 2.0 asymptote; the robust datum is the q4-vs-q3 deficit contrast (0.30 vs 0.00); s is parametrization-unstable (−1.3..−1.8). (3) "Walking = complex-CFT shadow" softened to "consistent with"; PRELIMINARY Coulomb-gas check: Re(1/ν_complex)=1.534/1.563/1.588 (q5/6/7) — q=6,7 measured values rise PAST it toward d=2. (4) Exact ξ_d recorded (2512/159/48/24/10.6 for q=5/6/7/8/10): the planned q=5,6 DMRG crossover hunt was UNREACHABLE (ξ(q5)≈2500 vs n≤40); Sprint-137 retargeted to q=8-10. **Hygiene:** newer sprint_116a data promoted to results/ (stray experiments/results/ copy removed, exp_116a path fixed); .gitattributes added (LF for .sh/.py); .claude/settings.local.json untracked; sprint-136 commits pushed. Full report: sprints/audit_2026-06-09.md.

## Sprint 136 -- PIVOT: thermal-gap EXCEPTIONAL-POINT estimator of 1/nu; q=4 marginal log cross-checked OFF chi_F
Pivoted from the (near-closed) q=4 chi_F asymptote thread to a fresh observable: the EXCEPTIONAL POINT (EP) of the Z_q-charge-0 THERMAL gap in the COMPLEX transverse-field plane -- the quantum-chain analogue of a Fisher zero / the location of the GRZ complex-CFT fixed point. **Method:** charge-0 thermal gap Delta_eps(g)=E1c0-E0c0 (charge filter P=prod X_i, <v|P|v>~+1) on the PERIODIC S_q chain; at the gap minimum g*(L) the two charge-0 levels form a 2-level avoided crossing, so the nearest complex-g coalescence sits at **Im(g_EP)=sqrt(Delta_min/Delta_eps'')** (real-axis-only estimate). **Validated** vs an actual complex-symmetric diagonalization H(g*+iy) at q=2 (estimate==true EP to ~2%; exp_136a). GPU eigsh to dim~2M; robust solver = dense-subset (scipy eigh subset_by_index) for dim<=1500 else sparse with large ncv/maxiter on a NARROW disordered-side scan window (wide scans into the ordered phase STALL Lanczos on near-degeneracy). DB: im_gEP/thermal_gap_min/gstar_thermal (q2..7 per n) + imEP_exponent (power-fit p). **Results (exp_136b, exp_136_analysis):** (1) the EP estimator RECOVERS exact 1/nu -- local slope of Im(g_EP)~L^{-1/nu} -> q2=1.0 (p=0.95), q3=1.2 (p=1.17); Delta_min*L->2*pi*v*x_eps (CFT const). A 2nd g_c-free, chi_F-independent nu route. (2) **q=4: 1/nu_eff climbs MONOTONE from below toward 1.5** (slopes 1.336->1.369, p=1.354<1.5) and Delta_min*L drifts down 3.68->3.49 -- the marginal (c=1 dilution) operator's suppression, the SAME thing the chi_F thread (S129-135) found, now in a COMPLETELY different observable. Two independent observables agree (novelty-hardening #2). (3) **Walking q=5,6,7 = complex-CFT "conformal shadow":** effective 1/nu_eff rises smoothly across the q=4 boundary -- 1.51, 1.65, 1.78 -- still CLIMBING with L (slopes don't settle, unlike q<=3), steeper/more persistent for larger q (xi_q shrinks). The GRZ complex fixed point's thermal exponent continued analytically through q=4. (4) sat-fit gamma+A*L^{-p} gives **gamma=0 for ALL q** -> Im(g_EP)->0 everywhere; the walking signature is the SCALING crossover (power-law->faster at L>~xi), NOT a gamma>0 plateau (I corrected my pre-data guess). q=5 xi>12 => the crossover is BEYOND exact diag; reaching it needs **Z_q-conserving DMRG to L>>12** (charge-0 excited state) = the clean next step. POTENTIALLY NOVEL (modest/methodological): quantum-chain thermal-gap-EP 1/nu estimator + the q=4 marginal-log cross-check + the complex-CFT shadow map; classical Fisher zeros/complex CFT for Q>4 Potts are established (GRZ 1808.04380; Jacobsen-Wiese PRL 133 077101 (2024)) but the transverse-field quantum-chain EP route was not found. unresolved/sprint_136.md.

## Sprint 135 -- q=4 on-peak chi_F pushed to n=24 via DMRG; marginal-operator LOG detected in chi_F (q=3 control)
Extended the S134 **on-peak** peak-height chi_F (the correct FSS observable) past the n=12 exact-diag frontier using TeNPy DMRG, OPEN BC. S124 did open DMRG chi_F to n=20 but at the WRONG coupling (fixed g_c, off-peak); S134 proved the off-peak penalty pollutes the exponent -- so on-peak DMRG beyond n=12 is new. **Method (heavily validated):** real-dtype S_q ops (~6x vs complex); chi=48 converges chi_F to 1e-6 at n=12 (chiconv vs exact); svd_min=1e-8; warm-started central-diff dg=1e-3; forward-diff peak located then **+dg/2 location correction** (forward chi_F peaks at g*-dg/2). DMRG reproduces S134 exact on-peak chi_F to <=0.06% at n=8,10,12 (exact_chi at the corrected g* hits the S134 DB peak values 43.37186/56.11520 exactly). New DB: chi_F_open_peak + gstar_open, q=4 n=8..24 and q=3 n=8..24 (sprint 135). **q=4 result:** open on-peak kappa_eff ASCENDS MONOTONICALLY 0.66->1.49 over n=4..24 (pairs 0.73,1.00,1.15,1.26,1.33,1.38,1.43,1.46,1.49), no plateau/turnover, joins exact seamlessly; lnL 1.39->3.18 (doubled L past the frontier). **q=3 CONTROL (n=8..24, no marginal op, null 1.40) -- the linchpin:** no-log surface fit `kappa=K+d/L` recovers **K=1.401, R2=1.0000** = exact null; fixed-null fit log coeff **s=+0.003 (ZERO)** -- q3 needs no log. **q=4 same fits:** no-log `K+d/L` gives **K=1.70** (UNDERSHOOTS 2.0 = finite-size effective exp), fixed-null `2.0+s/lnL+d/L` gives **s=-1.26** (max|resid|=0.02) -- consistent with proven 2.0 once log+surface included. Direct fit `L^2 (lnL)^sigma` (sigma=-1.84) beats pure power by 14x SSR. **DISCRIMINATOR:** marginal-operator log PRESENT at q=4 (s~-1.2), ABSENT at q=3 (s~0) -- the Cardy(1986)/Hamer(1988) 1/lnL correction (derived for GAPS) now seen in chi_F. **Caveat (rigorous):** naive K+s/lnL and free 3-param fits OVERSHOOT for BOTH q (q3->1.94 not 1.4, q4->2.3-2.5) => unreliable; only fixed-null + no-log-control fits trustworthy. Asymptote NOT pinned at L<=24 (marginal log slow; open surface term blocks a clean 1/lnL pin). POTENTIALLY NOVEL (modest/methodological): chi_F marginal-log measurement for the 4-state Potts chain isolated by the q=3 control; extends S134. unresolved/sprint_135.md. (Periodic DMRG past n=12 not pursued -- finite-periodic MPS poorly supported in TeNPy.)

## Sprint 134 -- q=4 chi_F "wrong-sign" tension RESOLVED: it was a fixed-g_c (off-peak) artifact
Falsification test of S133's POTENTIALLY-NOVEL "open kappa_eff is non-monotonic". S132/S133 measured chi_F at the FIXED periodic g_c=1/q, but the finite-size chi_F PEAK sits at a pseudo-critical g*(L)!=g_c (boundary/rounding shift) that ->g_c as L->inf; the standard FSS observable is the peak height (Albuquerque uses the peak). Re-measured per-site chi_F AT the self-located peak g*(L) (adaptive g-sweep + parabola vertex, canonical estimator), both BC, n=4..12. Validation: the chi_F(g_c) recomputed at fixed g_c reproduces results.db chi_F_open_exact/chi_F_exact to <=3e-9. New DB: chi_F_open_peak, chi_F_periodic_peak, gstar_open, kappa_{open,periodic}_peak. (134a OPEN) the open peak is FAR below g_c (shift -0.097->-0.027, chi_peak 3-5x chi(g_c)); on-peak kappa_eff rises **MONOTONICALLY 0.657->1.281 with NO interior minimum** -- the S133 dip+turnaround is GONE. **RETRACT the non-monotonic-kappa_eff claim.** (134c PERIODIC) shift tiny (-0.022->-0.0014); on-peak kappa **ASCENDS 1.683->1.761 toward 2.0** while fixed-g_c DESCENDS 1.86->1.78 -- the S132 "descent away from 2.0" is ALSO a fixed-g_c effect. (134b/e VALIDATION, the linchpin) for q=2,3 (no marginal op, exact nulls) PERIODIC on-peak ascends-from-below to the null while fixed-g_c descends-from-above to the SAME null, both bracketing it (q=2: 1.022/1.072->1.0; q=3: 1.414/1.444->1.4). So a descending fixed-g_c kappa is NOT evidence of a sub-null asymptote; q=4's on-peak^/fixed-v share destination 2/nu-d=2.0. (134d synthesis) the identity **kappa_fixed = kappa_onpeak + d ln r/d ln L** (r=chi_gc/chi_peak) holds to 5e-15 -- the dip/descent live entirely in the off-peak-penalty term, the bulk (peak-height) term ascends. Open peak-shift local exp ~-1.23 (boundary-1/L-dominated; not a clean nu probe). **NET:** the standard peak-height estimator ascends toward 2/nu-d=2.0 for BOTH BC, the same validated direction as q=2,3 -- the S129-S133 apparent evidence against 2.0 was a fixed-coupling artifact. Asymptote still NOT pinned at L<=12 (q=4 on-peak ~1.76 periodic / 1.28 open; marginal-log slow) but no standard-estimator feature suggests a sub-2 plateau. POTENTIALLY NOVEL (modest/methodological): opposite fixed-v/peak-^ drift at the marginal q=4 point manufacturing an apparent wrong-sign tension; no prior report. unresolved/sprint_134.md.

## Sprint 133 -- Reconciled periodic vs open BC for q=4 chi_F; open kappa_eff is non-monotonic [SUPERSEDED by S134: the dip is a fixed-g_c off-peak artifact]
**Pre-sprint audit caught a convention bug:** prior open-BC data (S113/S124 results.db `chi_F_open`) used forward-diff/dg=1e-3/no-factor-2; the periodic series uses canonical central/dg=1e-4/factor-2 (canonical = ~2x forward). So the standing "periodic 1.78 vs open 1.52" was NEVER apples-to-apples. (133a) Recomputed OPEN with the IDENTICAL canonical estimator (g_c=1/q, n=4..12, GPU; only the wrap bond differs from periodic). Validation: periodic reproduces results.db `chi_F_exact` to <=5e-9; open forward-diff reproduces DB `chi_F_open` exactly; canon/forward=2.03. New DB series `chi_F_open_exact` q=4 n=4..12. **Result 1: the BC gap is REAL (convention-independent)** -- open kappa_eff(n=12)=1.537 vs periodic 1.778. **Result 2 (NEW): open kappa_eff is NON-MONOTONIC** -- minimum 1.5199 at n~7.5 then an ACCELERATING climb (post-min increments GROW +0.0023->+0.0054, still rising at the frontier, NOT plateauing). S124 DMRG computed n>=6 and saw only the rising tail ("drifts up"); canonical exact-diag from n=4 reveals the full dip+turnaround. Cross-method: S124 DMRG n=12..20 pairwise 1.515->1.524 (also rising) confirms the rise direction across both convention and method. Periodic = decelerating descent (decrements shrink geometrically x0.56) toward apparent plateau ~1.776. (133b, model-free) ratio chi_O/chi_P DECREASES away from 1 (0.352->0.260) => a vanishing multiplicative 1/L boundary is REFUTED; BC don't converge by n=12; joint shared-bulk fit non-identifiable (S132 degeneracy stands). Clean power laws: periodic alpha=1.791+/-0.004, open 1.527+/-0.001 (both R^2>0.9999, both far below 2.0 -- face-value sub-2, as S132). **Verdict:** asymptote still UNQUOTABLE at L<=12, BUT the open turnaround NEUTRALIZES the S132 "wrong-sign descent vs 2.0" argument -- a finite-window apparent plateau demonstrably reverses (open did it), so periodic's descent to ~1.78 is not evidence against 2.0. The two BCs' opposite drift directions are reconciled as one non-monotonic finite-size flow (open ahead of periodic). POTENTIALLY NOVEL (hardening via independent-BC cross-check, novelty-rule #2); no prior report of non-monotonic chi_F kappa_eff or open/periodic chi_F reconciliation for 4-state Potts. unresolved/sprint_133.md.

## Sprint 132 -- GPU restored; q=4 n=12 frontier; chi_F local-exp trend is wrong-sign for marginal-log->2 [CORRECTED by S134: the "wrong-sign descent" is a fixed-g_c off-peak artifact; on-peak ascends toward 2.0]
Fixed the ~3-sprint GPU outage: pinned **cupy-cuda12x 13.6.0** + numpy==1.26.4 (the installed 14.0.1 needed numpy>=2 = ABI break vs the validated CPU stack). Validated bit-faithful: q=4 n=9/10/11 reproduce results.db to ~1e-9, CPU-vs-GPU agree to 8e-10, 9.2x speedup (132a). **Frontier point: chi_F(q=4 n=12, dim 16.78M)=93.747642 in 59.9s on GPU** (132b); recorded to DB; full n=4..12 power-law alpha=1.790. **Headline:** the pairwise local exponent DECREASES monotonically 1.846->1.778 and moves AWAY from the null 2/nu-d=2.0 (|gap| grows 0.154->0.222) -- the WRONG SIGN for a marginally-irrelevant log climbing to 2. (132c) dlnL2=alpha_loc-2 does not flatten to 0; leading-2 forms fit worse than pure power and predict an *increasing* local exp. (132d synthetic recovery) a true-2.0xmarg-log endpoint-matched to the data gives an *increasing* local exp (1.773->1.853) while real data decrease (RMS 0.060 vs 0.005) => the diagnostic is NON-circular (unlike S129's no-log chi-extrapolation) and the data sit on the a<2 side. (132e q=3 control) q=3 (no marginal op) descends ONTO its null 1.40 while q=4 descends away from 2.0; the control ALSO calibrates the 1/lnN gap-extrapolation as unreliable (fabricates -0.18 deficit where truth=0), so **the asymptote is deliberately NOT quoted** -- robust claim = TREND DIRECTION only. NOT a refutation of 2.0 (nu=2/3+Albuquerque still predict leading 2; a turnaround at L>>12 can't be excluded). POTENTIALLY NOVEL (hardens S128/129 chi_F-q=4 flag); unresolved/sprint_132.md. Open-vs-periodic BC tension (periodic down to 1.78 vs open DMRG up to 1.52, S124) flagged for next sprint.

## Sprint 131 -- DATA-INTEGRITY FIX: reconciled q=5/q=7 chi_F walking exponents
The "q=5 alpha 2.094 vs 2.139" and "q=7 2.636 vs 2.584" discrepancies (flagged S129) RESOLVED: canonical = results.db alpha_exact (q=5->2.094+/-0.002, q=7->2.636+/-0.018); raw chi_F recomputed CPU-vs-GPU to 4.8e-9. The 2.139/2.584 were stale sprint-128 alpha(q)-table transcriptions reproduced by NO standard fit; sprint-127.md and CHANGELOG already held the correct values. Corrected alpha(q) effective curve is convex in ln q (super-log), not S128's "nearly linear". Not load-bearing (q=3,4 are finite-size effective exps). DB unchanged; only KNOWLEDGE.md was stale.

## Sprint 130 -- Independent nu + marginal-log signature from chi_F FSS (q=4 hardening)
Two calibrated, g_c-free observables from the full chi_F(g,N) curve (calibration q=2->1/nu=1, q=3->1.2). **Data collapse (location scaling, marginal-log-insensitive): 1/nu(q=4)=1.49 after q=2,3 calibration => nu=2/3 confirmed from our own data**, excludes 1/nu<=1.2. **Self-locating peak-HEIGHT amplitude exp** recovers 2/nu-d to <=1.3% at q=2,3 (unbiased) but a(q=4)=1.75 = 12.7% below 2.0 => the deficit is physical (the marginal log). Given nu=2/3 + Albuquerque the amplitude exp must ->2 asympt.; measured ~1.77-1.81 is finite-size. Peak-SHIFT exp UNUSABLE for nu (dead end). Report: sprints/sprint_130.md.

## Sprint 129 -- AUDIT: q=4 chi_F headline corrected (machinery sound, interpretation inverted)
External user-requested multi-agent scrutiny; no new physics, all numbers reproduced from code/DB read-only. Full report: sprints/sprint_129_audit.md. **Verdict: the machinery is sound but the q=4 headline was inverted.** (1) g_c=1/q verified exact self-dual (1e-15); finite-diff chi_F good to ~5 sig figs (dg=1e-4 bias shifts alpha 5e-6); the AIC procedure passes a synthetic recovery test. (2) DECISIVE: we measure PER-SITE chi_F, whose correct leading exponent is 2/nu-d (Albuquerque et al., PRB 81 064418). For q=4 nu=2/3 => 2/nu-d=2.0 is the CORRECT value, not a hypothesis to reject; our own q=3=7/5 (nu=5/6) anchor proves the convention. Measured 1.77 is the finite-size value below 2 (marginal operator => slow log approach). (3) DECISIVE: exp_128c's no-log extrapolation is circular (returns 1.60-1.89 on true-alpha=2-with-logs data) and L<=11 cannot resolve logs; open-BC DMRG drifts UP toward 2. (4) "Salas-Sokal p=3/2" mislabeled (it is the 2D-classical specific-heat log power, not a chi_F prediction). Retracted "q=4 alpha=1.77 asymptotic / Salas-Sokal rejected". Also flagged: q=5 alpha inconsistency (2.094 vs 2.139), results.db factor-2 convention split, idle QPU. Reframed STATE.md and KNOWLEDGE.md.

## Sprint 128 -- q=6 gap filled, q=4 log corrections tested, hybrid thread closed
(a) S_q q=6: alpha=2.375+/-0.006 (6 sizes, GPU). (b) Hybrid q=6: g_c=0.474, alpha=1.186. (c) Extrapolation fixed: DB-sourced, inf-guarded. S_q q=4 alpha_inf=1.771+/-0.001. (d) q=4 log corrections with exact chi_F: Power+1/N^2 wins (dAIC=41 over Salas-Sokal log). Best alpha=1.760. Salas-Sokal p=3/2 rejected (measured p=0.41). Model ranking same as spectral data. (e) Hybrid log vs power: power wins q<=4, log wins q>=6 (dAIC=20). Hybrid thread closed.

## Sprint 127 -- Extended exact chi_F to GPU sizes (up to 10M dim)
12 new data points across S_q and hybrid models at q=3,4,5,7. GPU-accelerated eigsh at dim up to 9.8M. Error bars reduced 17-62%. S_q q=5: alpha=2.094+/-0.002 (62% tighter). S_q q=4: alpha=1.795, pairwise (10,11)=1.779, still drifting below 2.0. S_q q=7: alpha=2.636, pairwise increasing. Hybrid alpha(q) confirmed non-monotonic (peaks q~3-4, drops to 0.96 at q=7). Prior alpha(q)=1.86*ln(q) fit obsolete -- new slope 1.306.

## Compressed Sprint History (Sprints 125-126)
- **125** — Spectral chi_F factor-2 prefactor bug found (captures 50% of true chi_F; missing Lehmann factor-2). After fix matches exact to 0-2.2%; k-truncation not the issue; exponents UNAFFECTED.
- **126** — Corrected spectral chi_F still 0.5-4% alpha-low (non-dominant fraction grows with size). Authoritative exponents via EXACT chi_F (finite-diff) w/ error bars; S_q alpha 1.48→2.61 monotone in q; model comparison >10sigma at q>=4. (Use exact chi_F for all exponent claims.)
Full details: sprints/sprint_12{5,6}.md.

## Compressed Sprint History (Sprints 001-024)

- **001** — Bell states & CHSH. S=2.834 matches Tsirelson bound. GHZ scaling timed out (partial_trace limit).
- **002** — CHSH landscape (19.9% of angles violate), noise kills at p≈9.5%, cluster states gain entropy under qubit loss.
- **003** — Cluster state qubit loss: position-dependent, two-qubit loss unlocks 3 bits of hidden entanglement.
- **004** — MI and I3 distinguish all archetypes. GHZ has I3=+1 (redundant), Cluster has I3=-1 (irreducible).
- **005** — Discord: GHZ=0 (classical pairwise), W=0.28 (most quantum), Cluster=0. Three archetypes confirmed.
- **006** — Concurrence, negativity, monogamy. Cluster has 7x GHZ entanglement at certain bipartitions.
- **007** — 2D cluster: topological entanglement, position-independent qubit loss, 3x baseline entropy.
- **008** — Phi/IIT: 2D cluster 100% Phi retention under loss. Phi measures structure not quantumness.
- **009** — Structured noise fingerprints: each state has unique 6D signature. Cluster weakest to dephasing.
- **010** — GME witnesses, body-order hierarchy, 4-measurement classifier (182x compression vs tomography).
- **011** — Entanglement dynamics: CZ gates can destroy MI. 2D cluster annihilates ALL pairwise MI.
- **012** — Scrambling & OTOCs: GHZ has OTOC=1 despite MI=15. Entanglement ≠ scrambling.
- **013** — Hayden-Preskill: scrambling democratizes recovery. Page curve visible. Light cone in 1D.
- **014** — QEC = static scrambling. [[5,1,3]] Page curve matches Hayden-Preskill. Code distance = body-order.
- **015** — Code families: distance ≠ topology. Democratic/Selective/Hierarchical code archetypes.
- **016** — Structured noise breaks topology-blindness. "Keep and correct" vs "filter and project" strategies.
- **017** — Threshold as phase transition. Holevo is the order parameter. Concatenation sharpens transition.
- **018** — Syndrome information: lossy compression. Fault tolerance is emergent collective phenomenon.
- **019** — Channel capacity: depolarizing threshold p≈0.20. Codes far from capacity. Phase damping non-monotonic.
- **020** — Toric code: zero I3, local indistinguishability, bimodal Page curve. Fourth archetype (Topological).
- **021** — Combined T1+T2: basis isotropy is everything. [[5,1,3]] asymmetry 0.005 vs 3-qubit 0.680.
- **022** — Noise-adapted codes: isotropy always wins for quantum computation at small scale.
- **023** — Concatenated bias-tailoring: figure of merit determines winner. Min-basis Holevo → [[5,1,3]] 81%.
- **024** — Surface code at d=3: never wins. Boundary tax breaks isotropy. Advantage is architectural, not informational.

- **025** — Real hardware QPU test (20s ibm_kingston). [[5,1,3]] isotropy confirmed: asymmetry 0.040 vs 3-qubit 0.254.
- **026** — Active syndrome extraction: non-FT always hurts at all error rates.
- **027** — Flag-FT syndrome: solves the wrong problem, still never beats passive.
- **028** — Repeated syndrome: 48 2Q gate overhead kills. QEC active correction arc closed.
- **029** — TFIM phase transition: Scale-Free archetype discovered. MI-CV as order parameter.
- **030** — XXZ archetype loop. MI-CV classifies transition type (crossing/step/dome).
- **031** — Entanglement spectrum: three levels of description (scalar/correlation/spectral).
- **032** — Bisognano-Wichmann: symmetry controls BW accuracy. Fourth level (Hamiltonian).
- **033** — Potts BW: local dimension matters more than group size.
- **034** — BW operator algebra: H/G-inv ratio perfectly predicts BW locality.

Full details for all compressed sprints are in sprints/sprint_NNN.md.

---

## Compressed Sprint History (Sprints 035-070)

- **035-048** — BW scaling, MI-CV FSS/classification, Potts phase transitions. Sprints 044-047 INVALIDATED (wrong g_c).
- **049-053** — g_c correction (true g_c from self-duality). g_c(q) formula. ν(q) ≈ 0.82-0.86.
- **054-060** — c(q) ≈ 0.40·ln(q-1)+0.55. CFT operator content. x₁ peaks at q=3. OPE coefficients.
- **061-064** — Large-q limit. c·x₁ ≈ 0.112. BW locality degrades with q.
- **065-067** — Hybrid ≠ clock universality (3 probes). No first-order signal. No floating phase in hybrid.
- **068-070** — 2D hybrid model. g_c(2D) measured. q=2 continuous confirmed. q=5 inconclusive.
- **071** — Ly=2 cylinder: g_c(q=2)=0.451, g_c(q=5)=0.714. DMRG impractical for q≥5 cylinder.
- **072** — q=3 cylinder g_c=0.565. Cyl/1D ratio monotonically decreasing. Ly=3 q=2: g_c=0.655.
- **073** — q=3 Ly=3: g_c=0.797 (49.7% to 2D). q=2 Ly=4: g_c=0.688. q=3 converges 1.9× slower.
- **074** — q=3 Ly=4 infeasible. q=5 Ly=3: g_c=0.974. Convergence saturates for q≥3.
- **075** — q=2 Ly=5: g_c=0.701 (86.6% to 2D). Power-law 1/Ly² convergence, not exponential.

Full details for all compressed sprints are in sprints/sprint_NNN.md.

- **076** — S_q Potts vs hybrid head-to-head at q=5. g_c(S_q)=0.200. 4-fold vs 2+2 degeneracy. S_q FSS 10x larger.
- **077** — S_q at q=7,10: g_c=0.144/0.101. No first-order signal at n≤8. Δ·N≈0.6 q-independent.
- **078** — Self-duality: g_c=1/q exact. DMRG walking holds at n≤12. c(q=5)=1.15 matches Re(c)=1.138.
- **079** — c_eff at q=7,10: walking breaks down. c_eff/Re(c) degrades monotonically. q=5 unique sweet spot.

Full details for sprints 076-079 are in sprints/sprint_NNN.md.

- **080** — c_eff at q=6,8,9: walking boundary mapped. c_eff/Re(c) = 1.004·exp(−0.105(q−5)). q=5 exact walking threshold. gap×N increases with q even as walking breaks.
- **081** — q=6 marginal breaking: c_eff drops 2.9% n=8→12, drift dc/d(ln n)=-0.048. Walking boundary is smooth crossover. ξ*≈38 for q=6.

- **082** — x_σ(q) ≈ 0.13 nearly universal for q=2-8. v(q) monotonically decreasing. Walking invisible in correlators. Open-BC power law inflates η by 5×.
- **083** — Casimir c_implied/Re(c) ≈ 1.00±0.03 for ALL q=2-8. Energy tracks Re(c) even where entropy deviates 40%. Walking is exclusively an entropy phenomenon.
- **084** — Entanglement spectrum: (q-1)-fold degenerate multiplet. Level 1 absorbs 48%→69% of entropy (q=2→8). Entropy concentration as microscopic walking breakdown mechanism.

- **085** — Rényi c_α(q,α) mapping. α=1 best for walking (q≤6), optimal α shifts to 2 for broken (q≥7). ~~α=3 recovery~~ RETRACTED in Sprint 086. Rényi spread is monotonic walking discriminator.

- **086** — Rényi DMRG: α=3 recovery was extraction artifact. Corrected: optimal α = 0.5 (real) → 1 (walking) → 2 (broken). q=7 tail grows 8×. No Rényi index recovers Re(c) for broken walking.
- **087** — Entanglement spectrum DMRG: tail weight unbounded power law ~n^b. c_eff size pairs confirm walking vs breakdown. NOTE: exponents corrected in Sprint 088.
- **088** — Tail exponent UNIVERSAL b≈2.0 for q=2,3,5. Walking breakdown NOT in tail growth — must be in level redistribution.
- **089** — q=7 b≈3.0 resolved (pre-asymptotic). M/[(q-1)/q] crosses 1.0 at walking boundary. Democracy index flips at q≈4.
- **090** — q=4 M/[(q-1)/q]=1.003 at n=16. q_cross→4.0 in thermodynamic limit. b=2.024 confirms universal.
- **091** — BW fidelity across walking: non-Potts grows ~exp(1.6q). Biggest jump at q=3→4. BW alpha discontinuity at q=4.
- **092** — Non-Potts operators = mixed clock-shift (XZ-type). Walking amplifies but doesn't change type. Flat at nA=3.
- **093** — BW temperature profile: sin-envelope correct, residual bulk-concentrated (real CFT) vs uniform (walking). 34× amplification at q=5.
- **094** — BW threshold nA*(q): two-regime, B(q)=0.48q+1.09. Walking shifts nA* down by 1 site. NOTE: nA*=5 was artifact (Sprint 095).

Full details for sprints 086-094 are in sprints/sprint_NNN.md.

### Sprint 095 — BW R² vs n at Fixed nA: Equal-Bipartition Anomaly Discovered
**Status:** Complete (3 experiments).

**q=2 BW R² with varying n at fixed nA (095a).** Periodic exact diag, nA=3-6, n up to 18. Key: 1-R² is flat in n for nA≤4 (varies <2× as n doubles). nA=6 collapses at ALL n (1-R²≈0.17 at n=18, nA/n=0.33). nA=5 at n≥16: 1-R²=5.6e-4 (20× better than Sprint 094's n=10).

**q=5 periodic nA=3 (095b).** n=7: 1-R²=1.66e-3, n=8: 2.11e-3. Walking amplification 10-15× at matched nA/n. DMRG attempt at chi≥125 too expensive (251s at n=10).

**Equal-bipartition penalty discovered (095c).** At nA/n=0.5, BW accuracy is systematically worse: 2× (nA=3), 2.1× (nA=4), **18× (nA=5)**, 1.4× (nA=6). Sprint 094's "threshold at nA=5" was an ARTIFACT. True threshold: nA*=6 for q=2.

**Surprises:**
- nA=5 is NOT at the BW threshold — 18× equal-bipartition artifact inflated Sprint 094's result
- BW corrections are UV (lattice), not IR — increasing n doesn't help
- nA=6 threshold is genuine: persists at nA/n=0.33
- Equal-bipartition penalty peaks at threshold nA — most dangerous where it matters most
- Walking amplification (q=5/q=2) is ~10-15× regardless of nA/n ratio

**POTENTIALLY NOVEL:** First BW fidelity vs subsystem-to-system ratio mapping. Discovery of equal-bipartition anomaly in BW accuracy. Revision of BW threshold from nA*=5 to nA*=6 for q=2.

[Full report: sprints/sprint_095.md]

### Sprint 096 — BW Threshold Mechanism: Non-Potts Operators, Not Spectrum
**Status:** Complete (4 experiments).

**Entanglement spectrum smooth across BW threshold (096a-b).** q=2 n=14 nA=3-7: tail weight changes 8% from nA=5→6, but 1-R² jumps 212×. Confirmed for q=3,5. Spectrum does NOT predict BW breakdown.

**BW residual dominated by max-range operators (096c).** At nA=6, 96% of residual in operators spanning ≥4 sites. Top operators: ZIIIXI, ZIIXXI — non-Potts mixed types.

**Adding longer-range Potts operators barely helps (096d).** Free-fit 21 Potts ops: 1-R² improves from 0.171 to 0.163 (5%). Non-Potts fraction itself has 244× threshold jump at nA=6. BW envelope is optimal for Potts subspace.

**Mechanism:** BW breaks when H_E develops significant non-Potts operators (mixed clock×shift). Threshold is in EIGENVECTORS of ρ_A, not eigenvalues. UV lattice effect.

[Full report: sprints/sprint_096.md]

### Sprint 097 — H_E Operator Compactness: BW Breakdown is Fundamental
**Status:** Complete (3 experiments).

**Pre-threshold H_E is maximally compact (097a).** q=2 n=14, full Pauli decomposition. nA=3-5: exactly 2nA-1 BW operators capture >99.9%. PR=4-7. At nA=6 (threshold): need 206 ops for 90%, 1052 for 99%. PR jumps to 12.

**Non-BW content is DIFFUSE at threshold (097b).** nA=6: non-BW PR=357, need 743 operators for 90% of non-BW weight. XZ-mixed 44%, XYZ 21%. High-body (4-6) long-range (3-5) operators dominate. No compact "BW + corrections" ansatz exists.

**Universal across q (097c).** q=3 n=10 clock-shift basis: nA=3,4 compact (10-14 BW ops, >99.9%). nA=5 threshold: non-Potts 22.4% (even larger than q=2 at 16.3%). Free-fit all Potts ops only 3% improvement.

**BW is the optimal compact H_E approximation.** Beyond threshold, H_E requires exponentially many parameters — fundamentally beyond any local Hamiltonian ansatz.

[Full report: sprints/sprint_097.md]

### Sprint 098 — Harden Casimir Finding: CONFIRMED NOVEL
**Status:** Complete (2 experiments).

**GPU-extended Casimir fit (098a).** Vectorized Hamiltonian builder for large matrices. New sizes: q=3 n=12 (531k), q=5 n=10 (9.8M, 159s), q=7 n=8 (5.7M, 148s), q=8 n=7 (2.1M). All q now have 4-5 data points.

**Pairwise convergence analysis (098b).** Pairwise c_implied/Re(c) from consecutive (N₁,N₂) pairs: q=7 (7,8)→1.000 (exact!), q=8 (6,7)→0.992. Extrapolated ∞: mean=0.998±0.012. 1/N⁴ corrections systematic (|d|/q≈0.044, q-independent).

**Casimir 16× more consistent with Re(c) than entropy.** Pairwise-last spread 0.009 vs entropy spread 0.145. At q=7: Casimir off by 0.0%, entropy off by 21.6%.

**Upgraded from POTENTIALLY NOVEL to CONFIRMED NOVEL.** Five checks passed: 5+ points, pairwise convergence, 16× consistency, systematic corrections, independence from entropy.

[Full report: sprints/sprint_098.md]

### Sprint 099 — Complex CFT: Im(c) Oscillation Detection (NEGATIVE)
**Status:** Complete (3 experiments).

**Dense Casimir scan (099a).** E₀(N) at all integer N: q=2 N=4-14 (11 pts), q=5 N=4-10 (7 pts, GPU for N=9,10), q=7 N=4-8 (5 pts, GPU for N=8). Odd sizes (N=5,7,9) newly measured for q=5.

**Oscillatory vs monotonic fit (099b).** Compared 3 models at same parameter count. Monotonic 1/N⁶ correction beats oscillatory cos(ω·ln N)/N⁴ for ALL q (M3/M2 = 5051 for q=2, 1.54 for q=5, 1.61 for q=7). Complex CFT oscillation period (6.53 in ln N for q=5) requires N ratio ~684 — our N=4-10 range covers only 14% of one cycle.

**Pairwise separation (099c).** q=5 pairwise c/Re(c) is non-monotonic (first decreases, then increases from N≈6). Traced to VELOCITY effect: pairwise vc itself is monotonically decreasing for all q. Detrended vc RMS: q=2 4.75e-5, q=5 3.97e-4 (8×), q=7 9.96e-4 (21×). Richardson extrapolation drifts for q>4.

**Im(c) oscillations undetectable at exact diag sizes.** Would need DMRG at N=10-100 or non-Hermitian formulation.

[Full report: sprints/sprint_099.md]

### Sprint 100 — DMRG Casimir: Open vs Periodic BC
**Status:** Complete (3 experiments).

**DMRG Casimir q=2 open BC (100a).** 7 points N=8-24. DMRG matches exact diag to 10⁻¹⁴ at N≤14. Open-BC 4-param fit: c=0.485 (c/0.5=0.971). Boundary corrections ~3% at N~24. Pairwise converges slowly: 0.88→0.93.

**Open-BC Casimir for q=5,7 — FAILS (100b).** q=5 (6 pts N=6-12): c/Re(c)=0.64. q=7 (5 pts N=4-8): c/Re(c)=0.36. Boundary corrections scale with q: 3% (q=2), 36% (q=5), 64% (q=7). Open-BC extraction is impractical for q≥5 at accessible DMRG sizes.

**Periodic-BC reanalysis — confirms Re(c) tracking (100c).** Sprint 099a dense periodic data reanalyzed. Pairwise c/Re(c): q=2 (5,6)→1.000, q=5 (7,8)→1.002, q=7 (5,6)→1.000. Periodic BC 10-100× more accurate than open BC at same N (1/N² vs 1/N corrections).

**Key finding:** Casimir-Re(c) result CANNOT be extended to DMRG sizes via open BC. Periodic exact diag (Sprint 098) remains definitive. Literature confirms Im(c) detection impossible from real Hamiltonian Casimir energy.

[Full report: sprints/sprint_100.md]

### Sprint 101 — Symmetry-Resolved Entanglement Entropy (SREE)
**Status:** Complete (3 experiments, 101a partially retracted).

**SREE for S_q Potts q=2-10 at g_c=1/q (101b).** Charge-sector decomposition via Z_q projectors. Charge-0 enrichment increases with q: p(0)*q from 1.55 (q=2) to 5.15 (q=10). p(0)→1/2 as q→∞ (not 1/q). S_n/S_t ≈ 0.908 universal across q at n=6.

**Size scaling (101c).** S_n/S_t is q-INDEPENDENT at fixed geometry: 0.953 (n=4), 0.908 (n=6), 0.875 (n=8) for all q tested. Implies S_number ∝ c(q). p(0)*q decreases slowly with n but stays >>1 at accessible sizes.

**101a RETRACTED:** Used hybrid field (X+X†) with S_q critical coupling g_c=1/q. For q≥4 this put the system far from criticality. Corrected in 101b.

**SREE is NOT a walking discriminator** at accessible sizes — all q-dependence is smooth and monotonic. No feature at q=4 or q=5.

**POTENTIALLY NOVEL:** Universal q-independent S_n/S_t ratio at fixed geometry for critical S_q Potts. First SREE measurement for q=4-10 Potts model.

[Full report: sprints/sprint_101.md]

### Sprint 102 — Fidelity Susceptibility Across the Walking Boundary
**Status:** Complete (3 experiments).

**χ_F scan near g_c for q=2,3,5,7 (102a).** S_q Potts periodic chain, δg=10⁻⁴. Peak heights at n=6: 0.73 (q=2), 4.09 (q=3), 36.29 (q=5), 166.88 (q=7) — 228× range. Peak at exact g_c for q≥5 (no FSS shift). Peak converges from below for q=2,3.

**FSS analysis + q=2 n=14 (102b).** χ_F_max ~ N^α. q=2: α=0.98 → ν=1.009 (exact 1.0). q=3: α=1.38 → ν=0.841 (exact 0.833). q=5: α=2.09 → ν_eff=0.648 (gap-derived 0.83). q=5 exponent matches first-order prediction (α=2 in 1D).

**q=4 crossover (102c).** n=6,8: α=1.69, ν=0.743 (exact 2/3). χ_F at n=6 grows exponentially with q: ~exp(1.06q), growth 2.88× per unit q.

**Key finding:** Walking regime makes χ_F scale as ~N² (first-order) despite gap/correlators showing continuous behavior. Fourth observable with walking-specific anomaly (after entropy, Casimir, correlators).

**POTENTIALLY NOVEL:** First fidelity susceptibility measurement across walking boundary. Discovery of first-order-like χ_F scaling in walking regime. Need more sizes at q=5 to harden.

[Full report: sprints/sprint_102.md]

### Sprint 103 — Harden χ_F Scaling: α(q) Confirmed Novel
**Status:** Complete (3 experiments).

**q=5 GPU extension (103a).** n=6,8,9,10 (4 sizes, GPU for n≥9). α=2.091 (4-point fit, err=0.002). Pairwise: (6,8)→2.088, (8,9)→2.094, (9,10)→2.100 — converging UPWARD. n=10 (dim=9.8M) at 156s on GPU.

**q=6,7 mapping (103b).** q=6 n=6,8: α=2.37. q=7 n=6,7,8: α=2.65 (pairwise 2.63, 2.67). Super-first-order scaling (α>2) for ALL q≥5, increasing with q.

**Full α(q) analysis (103c).** α(q) = 0.315q + 0.469 linear for q≥4 (residuals ±0.05). α=2 crossing at q≈4.9 (walking boundary). χ_F(n=6) ~ exp(1.06q). q=4 α=1.69 (15% below BKT prediction due to log corrections).

**Upgraded to CONFIRMED NOVEL.** Five checks: 4+ sizes at q=5 (0.3% stability), three walking q values, q=2,3 match exact ν to <2%, independent reproduction of q=7 n=6, simple linear functional form.

[Full report: sprints/sprint_103.md]

### Sprint 104 — Energy-Entropy Hierarchy Universality Test (NEGATIVE)
**Status:** Complete (3 experiments).

**J1-J2 chain at three regimes (104a).** Spin-1/2 chain, periodic BC, S_z=0 sector exact diag, N=8-20. Compared c_eff (entropy) vs c_Cas (Casimir) convergence to c=1. XX (Δ=0): tied (1.0×). Heisenberg (Δ=1): entropy wins 21× (c_eff 0.07% off, c_Cas 1.4% off). BKT (J2=0.2412): Casimir wins 14× (c_Cas 0.03% off, c_eff 0.37% off).

**Velocity extraction (104b).** Independent v from S_z=0→S_z=1 gap. XX: v_gap=1.002 (exact 1.0). Heisenberg: v_gap=1.387 (exact π/2=1.571, 12% log correction). BKT: v_gap=1.177 (smoothly converging, minimal log correction). Multi-size Casimir fit confirms: c_Cas(fit) = 0.998-1.005 for all models.

**Cross-model comparison (104c).** Potts max |Δc_eff| = 26% (q=7-8). J1-J2 max |Δc_eff| = 0.6%. Potts effect is 41× LARGER. Heisenberg c_Cas deviation follows 1/ln(N) (fit: 0.283/ln(N) - 0.084).

**Key finding: Energy-entropy hierarchy is NOT universal.** Direction depends on correction type: marginal operator logs → entropy wins (Heisenberg); BKT log³ corrections → Casimir wins; walking spectrum reorganization → Casimir wins by O(1) (Potts only). The O(1) entropy deviation is unique to walking.

[Full report: sprints/sprint_104.md]

### Sprint 105 — χ_F Scaling at J1-J2 BKT: Walking Super-Scaling is Unique
**Status:** Complete (3 experiments).

**Wide χ_F scan (105a).** J1-J2 Heisenberg, S_z=0 periodic BC, N=8-20. No peak near J2_c=0.2412 at any size — χ_F monotonically increasing through BKT region. Peak instead at J2≈0.487 (Majumdar-Ghosh point). N=16 has level-crossing spike.

**BKT vs MG resolution (105b).** BKT region (J2=0.15-0.35): MONOTONIC for all N. MG region (J2=0.40-0.55): peak saturates at N≈16 (χ_F=1.88) then DECREASES. Pairwise α: 4.24→0.28→-0.16. MG is a finite-size level crossing, not divergent.

**Exact-point scaling (105c).** χ_F at J2_c=0.2412: grows as N^0.58 (global), but pairwise α decreases 1.01→0.29 — trending to logarithmic. Three-way comparison:
- BKT: α→0 (invisible, exponential gap closing too slow)
- MG first-order: saturates then decreases (finite discontinuity)
- Potts walking: α=2.09-2.65, increasing with N (genuine super-first-order)

**Walking χ_F super-scaling confirmed as walking-specific.** Combined with Sprint 104 (Casimir-Re(c) walking-specific), both confirmed novel results now properly scoped.

[Full report: sprints/sprint_105.md]

### Sprint 106 — χ_F Spectral Decomposition: Walking Super-Scaling Mechanism
**Status:** Complete (3 experiments).

**Spectral decomposition at g_c (106a).** S_q Potts periodic chain, 20 eigenstates per config. χ_F is 100% dominated by a SINGLE excited state: the (q-1)-fold degenerate S_q multiplet (level q-1). The spectral gap (level 1) has ZERO matrix element with H_field — symmetry-forbidden. For q≥3, one multiplet captures 100%; for q=2, 91-93%.

**Size scaling of components (106b).** Decomposition: α = β_me + 2z_m - 1, where gap_m ~ N^{-z_m} and |me|² ~ N^{β_me}. Extended to n=14 (q=2), n=10 (q=3), n=9 (q=5, GPU), n=7 (q=7, GPU). Decomposition is exact (predicted = measured to all digits). z_m: 0.989 (q=2) → 1.310 (q=7). β_me: 0.066 (q=2) → 1.010 (q=7). Both increase linearly with q.

**Mechanism analysis (106c).** Added q=4 (5 sizes) and q=6 (3 sizes). Linear fits: z_m(q) = 0.065q + 0.843, β_me(q) = 0.182q - 0.201. Reconstructed α(q) = 0.312q + 0.485 matches known 0.315q + 0.469 within 3%.

**Two sources of walking super-scaling:** (1) Multiplet gap closes faster than 1/N (z_m > 1 for q≥3), (2) Field matrix element grows with system size (β_me > 0 for q≥3). For q=2 (real CFT): gap only. For q=7 (broken walking): both contribute (72%/28%).

**POTENTIALLY NOVEL:** First spectral decomposition of χ_F at walking transition. Spectral gap symmetry-forbidden. Exact α = β_me + 2z_m - 1 with linear q-dependence.

[Full report: sprints/sprint_106.md]

### Sprint 107 — Harden χ_F Spectral Decomposition: CONFIRMED NOVEL
**Status:** Complete (4 experiments).

**GPU extension (107a/107a2).** q=5 extended to 5 sizes (n=6-10, GPU for n=10 dim=9.8M, 279s). q=7 extended to 3 sizes (n=6-8, GPU for n=8 dim=5.8M, 185s). All sizes: dominant fraction = 1.000. Updated fits: z_m(q) = 0.065q + 0.845, β_me(q) = 0.188q − 0.238. α = β_me + 2z_m − 1 exact to machine precision.

**Cross-check (107b).** Spectral vs finite-difference χ_F compared at q=2,3,5. Spectral/fd ratio = captured fraction: q=5 ~98% (single multiplet), q=2 ~87-93% (multi-state). Confirms mechanism: walking regime is truly single-multiplet dominated.

**Entanglement connection (107c).** Energy multiplet gap (z_energy ≈ 1.0-1.3) and entanglement gap (z_ent ≈ 0.2) share S_q symmetry origin but scale independently. Δξ/gap_m grows with N. The two (q-1)-fold multiplets are independent physical phenomena.

**Upgraded to CONFIRMED NOVEL.** Five checks: 5+ sizes at q=5 (pairwise α converges upward: 2.076→2.099), cross-validation, falsification survived, exact decomposition formula, independence from entanglement spectrum.

[Full report: sprints/sprint_107.md]

### Sprint 108 — q=4 BKT Crossover: Log Corrections Map Three Regimes
**Status:** Complete (3 experiments).

**q=4 GPU extension (108a).** 7 sizes n=4-10 (GPU for n=9,10). Dominant fraction=1.000 at all sizes (single multiplet). Pairwise α converges downward: 1.825→1.771. Global α=1.788.

**Log correction analysis (108b).** Pairwise exponent drift vs 1/ln(N) for q=3,4,5 (7 sizes each). Walking (q=5): α_log = -0.003/ln(N), R²=0.001 — zero correction. BKT (q=4): α_log = +0.243/ln(N), R²=0.92 — moderate. Continuous (q=3): α_log = +0.460/ln(N), R²=0.98 — strong. Extrapolated α_∞: q=3→1.22, q=4→1.66, q=5→2.08.

**Multiplet structure (108c).** Gap ratio (multiplet/spectral) decreases with q: 6.2 (q=3) → 5.2 (q=4) → 4.6 (q=5). Spectral gap is (q-1)-fold degenerate and symmetry-forbidden. Dominant state is a singlet above the multiplet.

**Key finding:** Linear formula α=0.315q+0.469 valid ONLY for walking regime (q≥5) where log corrections vanish. For q≤4, finite-size α is inflated. Walking regime is a cleaner measurement regime than continuous or BKT. **NOTE:** 1/ln(N) extrapolation for q=2,3 RETRACTED in Sprint 109 — power-law 1/N² is correct.

[Full report: sprints/sprint_108.md]

### Sprint 109 — α(q) Correction Form: Power-Law Recovers Exact ν
**Status:** Complete (3 experiments).

**q=3 GPU extension (109a).** 9 sizes n=4-14 (GPU for n=12,14). Pairwise α converges to 1.416 at (n=12,14) — heading straight to exact 1.4 (ν=5/6). Single multiplet dominance (frac=1.000) confirmed at all sizes.

**q=2 and q=4 extension (109b).** q=2: 11 sizes n=4-18. Pairwise α converges to 1.012 at (n=16,18) — approaching exact 1.0 (ν=1). q=4: 8 sizes n=4-11 (GPU for n=11). Pairwise α flat at 1.771 for last 3 pairs — BKT slow convergence.

**Power-law vs log correction analysis (109c).** Power-law 1/N^ω fits vs 1/ln(N) fits. Power-law overwhelmingly wins for q=2 (AIC: -140 vs -87) and q=3 (AIC: -109 vs -71). Fitted ω≈2 — standard FSS correction, not leading irrelevant operator. Power-law α_∞: q=2→1.001 (exact 1.0, 0.1% error), q=3→1.405 (exact 1.4, 0.4% error). Log α_∞: q=2→0.874 (12.6% error), q=3→1.301 (7.1% error). Neither model works for q=4 BKT.

**Partial retraction of Sprint 108:** 1/ln(N) form was wrong for q=2,3 (continuous transitions have power-law, not log corrections). Extrapolated α_∞(q=3)=1.22 retracted → correct value 1.40. Walking (q≥5) zero-correction finding CONFIRMED.

[Full report: sprints/sprint_109.md]

### Sprints 110-117 -- alpha(q) walking-regime mapping q=5..30 (compressed; see KNOWLEDGE.md + sprints/)
- **110** q=5-9: linear alpha(q) from S103 revised (q=4 was BKT contaminant); walking alpha~0.262q+0.815; single-multiplet universal.
- **111** q=10 chi_F alpha=3.349; power-law alpha(q) slightly preferred; super-scaling persists where walking broken (c_eff/Re(c)=0.60).
- **112** q=12 chi_F alpha=3.631; QUADRATIC alpha(q) preferred, linear RULED OUT (dAIC=12); growth sublinear.
- **113** DMRG chi_F open-vs-periodic BC: open-BC alpha far lower (q=4 1.51, q=5 1.60) and boundary effect GROWS with N; periodic exact diag definitive. POTENTIALLY NOVEL: chi_F BC-dependence enhanced at walking transition.
- **114** q=15 alpha=3.921; logarithmic alpha(q) growth emerging; quadratic peaks unphysically.
- **115** q=20 alpha=4.590; LOGARITHMIC alpha(q) becomes AIC-best; quadratic decisively ruled out; z_m crosses 2.0.
- **116** q=25 alpha=5.170; log+loglog marginally best (dAIC=1.4, not decisive); n=5 dim 9.8M took 1616s = practical GPU limit.
- **117** q=30 alpha(3,4)=5.384; pure log alpha(q)=1.87 ln(q)-0.97 preferred (Occam, LOO ties); q=5-30 mapping complete (diminishing returns).

### Sprint 118 -- q=4 chi_F Extended + Model Identity Audit
**Status:** Complete (1 experiment + audit).

**q=4 chi_F with 8 sizes n=4-11 (118a).** Pairwise alpha converges: 1.825->1.794->1.780->1.774->1.772->1.771->1.771. **alpha(q=4) = 1.771 +/- 0.001** (stable last 3 pairs). Differs from exact q=4 Potts alpha=2.0 by 11.5% — likely logarithmic corrections at the marginal Ashkin-Teller point.

**⚠ MODEL IDENTITY AUDIT:** Code audit confirmed ALL experiments from Sprint 076 onward use the **standard S_q Potts model** (Σ X^k field), NOT the "Potts-clock hybrid" (X+X† field) described in KNOWLEDGE.md. All six claimed novel findings are on the known S_q Potts chain. KNOWLEDGE.md, STATE.md, and sprint report corrected. The novel contributions are the probes (chi_F spectral decomposition, systematic scaling data), not the model itself.

~~Original Sprint 118 interpretation "confirms hybrid != S_q Potts" was WRONG~~ — the code IS S_q Potts.

[Full report: sprints/sprint_118.md]

### Sprint 119 — Hybrid Potts-Clock chi_F Spectral Decomposition
**Status:** Complete (2 experiments).

**Hybrid q=5 chi_F spectral (119a).** 7 sizes n=4-10 (GPU for n≥8). g_c=0.438. Single-multiplet dominance frac=1.000 at ALL sizes — identical to S_q. Spectral gap symmetry-forbidden. Global alpha=1.408, z_m=0.909, beta_me=0.590, nu_eff=0.831. **Prediction confirmed: alpha≈1.41, nu≈0.83.** Pairwise alpha DECREASING (1.56→1.26), opposite to S_q (INCREASING 2.08→2.10).

**Hybrid q=3,7,10 chi_F spectral (119b).** q=3 (sanity: hybrid=S_q): alpha=1.46→1.40, matches exact. q=7 (5 sizes n=4-8): alpha=0.952, z_m=0.770. q=10 (4 sizes n=4-7): alpha=0.552, z_m=0.688. Pairwise alpha STRONGLY decreasing at q≥7.

**Key findings:**
1. Single-multiplet dominance UNIVERSAL (both models, all q)
2. Decomposition alpha = beta_me + 2*z_m - 1 EXACT in both models
3. Hybrid alpha DECREASES with q (1.41→0.95→0.55) while S_q INCREASES (2.09→2.65→3.35)
4. z_m < 1 in hybrid (gap closes slower than 1/N) vs z_m > 1 in S_q (faster)
5. Walking super-scaling (alpha>2) is S_q-specific, NOT universal

**POTENTIALLY NOVEL:** First chi_F spectral decomposition on hybrid Potts-clock model. Universal mechanism with model-specific exponents. z_m crossing 1 as microscopic walking/continuous discriminator.

[Full report: sprints/sprint_119.md]

### Sprint 120 — Hybrid q=4 chi_F: z_m=1 Transition Point
**Status:** Complete (2 experiments).

**Hybrid q=4 g_c scan (120a).** Gap×N crossings at n=6,8,10 (GPU). Coarse scan g∈[0.33,0.43], 30 points. **g_c(hybrid,q=4) = 0.3933 ± 0.0002.** Excellent convergence: (6,8)→0.3934, (8,10)→0.3933.

**Hybrid q=4 chi_F spectral (120b).** 8 sizes n=4-11 (up to dim=4.2M, GPU). Plus q=3 sanity check. Single-multiplet dominance frac=1.000 at ALL sizes. **Global alpha=1.548, z_m=1.004, beta_me=0.541, nu_eff=0.785.** Pairwise alpha DECREASING (1.64→1.49), opposite to S_q q=4 (expected upward toward 2.0).

**Key findings:**
1. **z_m=1.004 at q=4** — exactly marginal. Hybrid z_m crosses 1 between q=3 (1.03) and q=5 (0.91), with q=4 at the boundary
2. **Hybrid alpha peaks at q=4** (1.55), then declines: alpha(q)=[1.40, 1.55, 1.41, 0.95, 0.55] for q=[3,4,5,7,10]. Non-monotonic
3. **Model divergence starts at q=4** — 12% gap (hybrid 1.55 vs S_q 1.77), growing to 64% at q=7
4. Pairwise alpha drift is OPPOSITE between models at q=4: hybrid downward, S_q upward. Different universality classes
5. Literature confirms S_q q=4 has log corrections from marginal operator (Salas-Sokal 1997): alpha→2.0 asymptotically

[Full report: sprints/sprint_120.md]

### Sprint 121 — z_m(q) Continuous Fit & S_q q=4 Extended Sizes
**Status:** Complete (2 experiments).

**z_m(q) fitting (121a).** 5 functional forms (linear, log, 1/√q, rational, power-law) fitted to hybrid z_m data at q=[3,4,5,7,10]. All converge: **q_cross = 3.58 ± 0.04.** Best fit: rational z_m = 1.368/(1+0.102q), R²=0.973. Alpha peak also at q≈3.58 from quadratic-in-ln(q) fit.

**S_q q=4 extended (121b).** 8 sizes n=4-11 (up to dim=4.2M, GPU). Single-multiplet dominance frac=1.000. **Global alpha=1.777±0.003, z_m=1.092±0.001, beta_me=0.604±0.002.** Pairwise alpha converges from above: 1.825→1.771. S_q z_m slowly drifting down: 1.097→1.079.

**Key findings:**
1. **q_cross = 3.58 ± 0.04** — walking→continuous boundary at non-integer q. Hybrid q=4 is barely walking (z_m=1.004), not exactly marginal
2. **S_q q=4: alpha=1.777, z_m=1.092** — firmly walking, consistent with asymptotic alpha=2.0 plus log corrections
3. **Alpha drift comparison:** S_q converges to ~1.77 (stable), hybrid decreasing from 1.64→1.49 (still drifting). 19% divergence at (10,11)
4. S_q z_m drift (1.097→1.079) suggests logarithmic approach to z_m=1 at larger sizes — consistent with BKT marginal operator

[Full report: sprints/sprint_121.md]

### Sprint 122 — Log Correction Fits at q=4 & Literature Context
**Status:** Complete (1 experiment + literature search).

**Log correction fits (122a).** 4 models fitted to S_q and hybrid q=4 chi_F data (n=4-11). Power + 1/N^2 correction wins decisively: S_q alpha=1.757±0.002 (AIC best, dAIC=22 over pure power), hybrid alpha=1.460±0.001. **Log-corrected alpha=2 form is WORST fit** for both models (dAIC=42-70 vs best). Free log fit gives negative p (wrong direction).

**Literature search.** Salas-Sokal (1997) predicts p=3/2 for thermal quantities at q=4 Potts. BUT: no prior measurement of chi_F log corrections exists. Lv et al. (2019) needed L=1024 for classical observables — asymptotic regime is far beyond n=11.

**Key findings:**
1. At n≤11, alpha=2 with log corrections cannot fit the data — dAIC=42 (S_q) and 70 (hybrid) vs best model
2. S_q best alpha=1.757 (with 1/N^2 correction), not approaching 2.0 at accessible sizes
3. Hybrid alpha=1.460 — clearly NOT Ashkin-Teller universality
4. chi_F log correction at q=4 has never been measured — would need DMRG at n=50+ to probe

[Full report: sprints/sprint_122.md]

### Sprint 123 — QPU Hardware Validation: TFIM Critical State
**Status:** Complete (simulation only — QPU credentials empty).

**VQE + adiabatic prep (123b,c).** Both FAILED for critical GS. HEA VQE: 50-56% fidelity. Adiabatic Trotter: <ZZ>=0.33 vs exact 0.65 (total time too short for critical gap).

**Exact state prep (123d).** Qiskit `initialize` decomposes n=4 TFIM GS into **11 CX gates** (depth=32). Signal survival: 88% at 1% CX error, 79% at 2%.

**Noisy phase scan (123e).** 3 coupling values (ordered/critical/paramagnetic): phase transition clearly resolvable with 88% signal. Self-dual symmetry <ZZ>=<X> at h_c is noise-robust criticality signature. QPU submission blocked — ~/.qiskit/qiskit-ibm.json empty.

**Key findings:**
1. `initialize` decomposition far superior to VQE/adiabatic for small n
2. Phase transition resolvable on noisy hardware (88% signal at 1% CX error)
3. 6 QPU-ready circuits saved, need credentials to submit (~30s QPU time)

[Full report: sprints/sprint_123.md]

### Sprint 124 -- DMRG chi_F for S_q q=4: Open-BC Alpha Drift
**Status:** Complete (3 experiments).

**iDMRG overlap chi_F (124a,b).** FAILED. Both random-start and warm-start produce wildly non-monotonic chi_F vs bond dimension. Root cause: S_q symmetry is non-abelian, TeNPy iDMRG converges to different local minima at different chi. iDMRG overlap chi_F is not viable for S_q Potts.

**Finite DMRG extension (124c).** Extended open-BC chi_F to n=20 (from n=12 in Sprint 113b). q=4: 8 sizes, pairwise alpha drifts UPWARD (1.505->1.523). Power+1/N^2: alpha_open=1.524+/-0.002, R^2=0.999999. Log-corrected (alpha=2): p=1.237, R^2=0.99971. q=2 cross-check: alpha drifts DOWN toward exact 1.0 (validates method).

**Key finding:** Open-BC alpha at q=4 is NOT converged -- it drifts upward, consistent with approach to higher asymptotic value (periodic 1.77 or log-corrected 2.0). The q=4 log correction regime requires n>>20.

[Full report: sprints/sprint_124.md]

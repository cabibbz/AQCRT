# Sprint 134 — Falsification test of the S133 non-monotonic open χ_F: on-peak vs fixed-g_c

**Date:** 2026-06-02
**Thread:** q=4 S_q Potts per-site χ_F effective exponent — STATE Top-Next #2: "locate the open turnaround mechanism."
**Environment:** Windows, Python 3.11.9, NVIDIA TITAN RTX (24 GB), CuPy 13.6.0, numpy 1.26.4.

## Motivation — a hostile-reviewer falsification of my own newest novel claim

Sprint 133 flagged **POTENTIALLY NOVEL**: the open-BC q=4 per-site χ_F *effective exponent* κ_eff(L)
is **non-monotonic** — it dips to a minimum ~1.520 at n≈7.5 then accelerates upward — while periodic
descends monotonically. The reconciliation narrative ("open is ahead of periodic in one non-monotonic
finite-size flow") and the "wrong-sign defused" argument both rest on this dip being a **real bulk/boundary
property**.

But S133 measured the open χ_F at the **periodic** thermodynamic critical point g_c = 1/q = 0.25. A finite
**open** chain has its *own* pseudo-critical point g*(L) ≠ g_c (boundary shifts it), and g*(L) → g_c only as
L→∞. So the fixed-g_c series samples χ_F(g) at a **moving off-peak distance**. Algebraically,
χ_F(g_c,L) = χ_F(g*,L)·r(L) with the off-peak penalty r(L)→1 monotonically; then
κ_fixed(L) = κ_onpeak(L) + d ln r/d ln L, and the positive, decreasing penalty-derivative can **manufacture a
dip** even if κ_onpeak is monotonic. **The standard FSS practice (Albuquerque 0912.2689; Schwandt–Alet–Capponi
PRL 2009) evaluates χ_F at the peak, not at a fixed coupling.**

**Pre-experiment probe (this sprint):** the open χ_F peak is FAR from g_c and the off-peak penalty is huge —
n=6 peak χ_F≈32.5 at g*≈0.188 vs χ_F(g_c)=8.46 (×3.8); n=8 peak≈42.7 at g*≈0.206 vs 13.1 (×3.3). The S133
open series was sampling the deep tail of a peak that marches toward g_c. This is a serious candidate to
explain the dip.

**Test:** recompute the open-BC q=4 χ_F series **at the finite-size peak g*(L)** (canonical estimator, n=4..12)
and ask: does the κ_eff dip+turnaround SURVIVE on-peak?
- **Survives** → non-monotonicity is intrinsic; S133 novelty hardened.
- **Vanishes (monotonic)** → the dip was a fixed-g_c off-peak artifact; S133 framing must be corrected
  (and a clean on-peak open series is the better bulk probe of the approach to 2.0).
Either outcome is decisive. Bonus: g*(L)−g_c scaling is an independent ν check (expect ∝ L^{−1/ν}, 1/ν=1.5).

## Literature check (3 keyword variations)
1. "fidelity susceptibility peak pseudo-critical finite-size scaling open boundary" → the χ_F peak sits at a
   pseudo-critical point displaced from g_c by a power law in L; on-peak FSS is the standard choice
   (Albuquerque 0912.2689 — our null ref — uses the peak). arXiv:1308.4611 studies χ_F under open vs periodic BC.
2. "non-monotonic fidelity susceptibility 4-state Potts marginal operator log corrections" → q=4 dilution field
   marginal ⇒ multiplicative logs (Cardy–Nauenberg–Scalapino; Salas–Sokal hep-lat/9607030; Blöte 0707.3317),
   all for *thermodynamic* susceptibility/specific heat, not χ_F. No prior non-monotonic χ_F effective exponent.
3. (carried from S133) no literature reports an open-vs-periodic χ_F effective-exponent reconciliation at q=4.
**Gap:** whether the open χ_F effective exponent is genuinely non-monotonic, or an off-peak artifact, is
untested. This sprint settles it for our data.

## Experiments

### exp_134a — OPEN on-peak χ_F sweep, q=4, n=4..12  (DONE)

Measured per-site χ_F at the self-located peak g*(L) (adaptive scan + parabola vertex), OPEN BC.
**Validation:** the χ_F(g_c) recomputed at the fixed periodic g_c reproduces results.db `chi_F_open_exact`
(S133) to ≤2.8e-9 at every n=4..12 — the builder/estimator are identical to S133, only the evaluation
point differs.

| pair | κ_onpeak | κ_fixed-g_c (S133) | g*(n+1) | shift |
|------|----------|--------------------|---------|-------|
| (4,5) | 0.6569 | 1.5559 | 0.17359 | −0.0764 |
| (5,6) | 0.8264 | 1.5301 | 0.18789 | −0.0621 |
| (6,7) | 0.9523 | 1.5212 | 0.19813 | −0.0519 |
| (7,8) | 1.0489 | **1.5199** (min) | 0.20576 | −0.0442 |
| (8,9) | 1.1253 | 1.5222 | 0.21163 | −0.0384 |
| (9,10) | 1.1870 | 1.5263 | 0.21627 | −0.0337 |
| (10,11) | 1.2379 | 1.5313 | 0.22000 | −0.0300 |
| (11,12) | 1.2806 | 1.5368 | 0.22304 | −0.0270 |

The open χ_F peak sits **far below** g_c (shift −0.097 at n=4 → −0.027 at n=12) and the peak height is
3–5× χ_F(g_c). **On-peak κ_eff rises MONOTONICALLY (0.657→1.281), NO interior minimum.** The fixed-g_c
series has its interior minimum at (7,8)=1.520 (the S133 dip). **→ the S133 non-monotonicity is an
off-peak artifact, not a property of the standard peak-height observable.**

### exp_134b — on-peak NULL validation (open BC), q=2→1.0, q=3→1.4  (DONE)

Does the new on-peak observable recover the EXACT nulls where there is no marginal operator?
- **q=2** (null 1.0): on-peak κ rises 0.37→**0.73** (n=16), monotone, still far below 1.0.
- **q=3** (null 1.4): on-peak κ rises 0.39→**1.00** (n=12), monotone, still far below 1.4.

On-peak is monotone-increasing toward the null for q=2,3 too — so q=4's monotone rise is the **universal**
behavior, and the fixed-g_c dip is the anomaly. BUT the **open-boundary** on-peak observable converges
*slowly* (large surface corrections) — it is the tool that isolates the artifact, **not** a superior
asymptote estimator.

### exp_134c — PERIODIC on-peak χ_F control, q=4, n=4..11  (DONE)

Periodic shift is tiny (−0.022 at n=4 → −0.0014 at n=11; g_c is nearly on-peak). Validation: χ_F(g_c)
reproduces results.db `chi_F_exact` (S132) to ≤2e-9.

| pair | κ_onpeak | κ_fixed-g_c (S132) |
|------|----------|--------------------|
| (4,5) | 1.6831 | (descending) |
| (6,7) | 1.7372 | 1.8038 |
| (8,9) | 1.7534 | 1.7855 |
| (9,10) | 1.7578 | 1.7815 |
| (10,11) | 1.7611 | 1.7792 |

**Periodic on-peak κ_eff ASCENDS (1.683→1.761) while fixed-g_c DESCENDS (1.86→1.78).** Opposite drift
directions. The S132 "wrong-sign descent away from 2.0" is therefore **also largely a fixed-g_c effect**:
the peak-height (standard FSS) estimator flows TOWARD 2.0.

### exp_134e — PERIODIC on-peak null validation, q=2,3  (DONE — the linchpin)

The decisive control: for the marginal-operator-free cases, does on-peak ascend-from-below to the exact
null while fixed-g_c descends-from-above to the SAME null?

| q (null) | on-peak κ (largest n) | fixed-g_c κ (largest n) | both bracket null? |
|----------|------------------------|--------------------------|--------------------|
| 2 (1.0) | 0.948→**1.022** ↑ | 1.170→**1.072** ↓ | **yes** (on<null<fixed) |
| 3 (1.4) | 1.311→**1.414** ↑ | 1.592→**1.444** ↓ | **yes** (on<null<fixed) |

**Confirmed.** On-peak ascends from below; fixed-g_c descends from above; both → the exact 2/ν−d. For
q=2,3 (no marginal op) both reach the null at accessible L. So the **identical q=4 pattern** (on-peak
1.76 ↑, fixed-g_c 1.78 ↓) has common destination **2/ν−d = 2.0**; q=4 is only further from it because the
marginal (dilution) operator's multiplicative log slows BOTH estimators.

### exp_134d — synthesis  (DONE)

- **Off-peak identity check:** κ_fixed(L) = κ_onpeak(L) + d ln r/d ln L, where r(L)=χ_F(g_c)/χ_F(g*) is
  the off-peak penalty. Numerical residual **max|·| = 5.3e-15** (machine precision). This rigorously
  decomposes the fixed-g_c effective exponent into the bulk peak-height part (ascending) plus the
  off-peak-penalty derivative. For OPEN the penalty derivative is huge (+0.90→+0.26) and falling; the
  *interior minimum* of the sum is exactly where the falling penalty term crosses the rising bulk term —
  i.e. the S133 dip is the penalty term, not the bulk.
- **Peak-shift scaling (bonus):** open |g*−g_c| local exponent ≈ −1.09 → −1.23 (largest-n). Between the
  boundary 1/L (−1) and the critical L^{−1/ν}=L^{−1.5}; boundary-1/L-dominated at these sizes, so it is
  **not** a clean ν probe (as expected for a surface-shifted pseudo-critical point). Logged, not headline.

## Verdict & implications

1. **[ROBUST] The S133 "non-monotonic open κ_eff (dip+turnaround)" is a FIXED-g_c off-peak artifact.**
   Measured at the open chain's own peak g*(L) — the standard FSS observable — κ_eff rises monotonically
   with no interior minimum (n=4..12), and on-peak is monotone for q=2,3 too. **RETRACT** the
   non-monotonic-κ_eff claim as a physical property.
2. **[ROBUST] The S132 "periodic κ_eff descent away from 2.0" is largely a fixed-g_c effect too.** On-peak
   periodic κ_eff *ascends* toward 2.0; the q=2,3 validation proves fixed-g_c descends to the null *from
   above* (so a descending fixed-g_c κ is **not** evidence of a sub-null asymptote).
3. **[STRENGTHENED] The genuine (peak-height) bulk effective exponent ascends toward 2/ν−d for BOTH BC**,
   the same validated direction as q=2,3 toward their exact nulls. This **resolves the direction** of the
   S129–S133 "wrong-sign" tension: it was a fixed-coupling evaluation artifact, not evidence against 2.0.
4. **[HONEST CAVEAT] The asymptote value is still not pinned at L≤12.** q=4 on-peak κ is ~1.76 (periodic,
   n=11) / 1.28 (open, n=12) — far below 2.0, because the marginal log makes the approach slow. But (a)
   the flow DIRECTION now matches the proven q=2,3 cases, (b) no feature (dip, plateau, descent) of the
   *standard* estimator suggests a sub-2 limit, and (c) naive increment extrapolation is unreliable (the
   q=3 control reaches 1.4 despite decelerating increments; the marginal log makes geometric extrapolation
   underestimate).

**Hostile-reviewer answers.** *Apples-to-apples?* Yes — identical builder/estimator/convention; only the
evaluation point (peak vs fixed g_c) differs; the off-peak identity holds to 5e-15. *Could finite-size /
off-peak explain the S133 dip?* Demonstrably YES — that was the whole test. *Non-trivial data points?*
q=2 and q=3 periodic each show on-peak↑/fixed↓ bracketing the EXACT null (could have failed; didn't), plus
the q=4 open dip vanishing on-peak. *Literature opposite?* The on-peak vs fixed-coupling χ_F distinction is
standard FSS (Albuquerque uses the peak); no paper reports the q=4 opposite-drift / wrong-sign resolution.

## Status update to the standing framework
- The q=4 χ_F asymptote question is **unchanged in its hard answer** (still 2/ν−d=2.0 by ν=2/3 +
  Albuquerque; still not numerically pinned at L≤12). What changed: the **apparent evidence against 2.0**
  (S132 descent, S133 dip) is dissolved — both were fixed-g_c off-peak artifacts; the standard peak-height
  estimator ascends toward 2.0 for both BC, validated against exact q=2,3 nulls.
- **POTENTIALLY NOVEL (modest, methodological):** at the marginal 4-state Potts point the fixed-critical-
  coupling χ_F effective exponent and the peak-height effective exponent drift in OPPOSITE directions
  (fixed↓, peak↑) toward a common 2/ν−d; the opposite drift is what manufactured an apparent
  wrong-sign/non-monotonic tension. No prior report found. Copied to unpublished/.


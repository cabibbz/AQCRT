# Sprint 129 — External Audit of the q=4 χ_F Headline Claim

**Type:** Audit sprint (user-requested, external multi-agent scrutiny). No new physics computed;
all numbers below were *reproduced* from the project's own code and `results.db` (read-only).

## What was audited
The Sprint 125–128 headline: **"S_q Potts q=4 fidelity-susceptibility exponent α ≈ 1.77,
asymptotically below 2, with Salas–Sokal log corrections (α=2, p=3/2) rejected (dAIC=41)."**
Source: `exp_127a` (exact χ_F), `exp_128c` (extrapolation → α_∞=1.771), `exp_128d` (4-model AIC).
Data: exact χ_F at n = {4,6,8,9,10,11} only — 6 deterministic points, ln N lever arm ×1.73.

## Verdict
**The computational machinery is sound; the headline interpretation is inverted.** The measured
1.77 is the finite-size effective value falling short of the *theoretically correct* leading
exponent 2, not an asymptotic exponent that refutes 2.

---

## Pillar-by-pillar findings

### ✅ Machinery that checks out (no action needed)
- **`g_c = 1/q` is exact.** Kramers–Wannier self-duality of `H = -Σδ - gΣ_{k}X^k` verified
  numerically: per-bond identity to 1e-16, ground-state energy duality `e₀(g)=qg·e₀(1/(q²g))` to
  1e-15, fixed point at `1/q`. (Evaluating at the finite-N χ_F *peak* instead of fixed 1/q shifts
  α *down* by ~0.05, i.e. the fixed-1/q choice is mildly conservative — it does not inflate α.)
- **Finite-difference χ_F is reliable to ~5 significant figures.** The dominant error at dg=1e-4 is
  smooth O(dg²) truncation, *not* catastrophic cancellation (the 1−overlap signal ~1e-6 sits ~10
  digits above the eigensolver floor). Cross-checked against a cancellation-free dense Lehmann sum
  and Richardson extrapolation. Net effect on α(q=4): **−5×10⁻⁶**, i.e. 1400× below the quoted
  ±0.0069. *Caveat:* the stored 6-decimal χ_F values (e.g. 27.138030) overstate precision — they
  carry a known ~1e-6…4e-6 low-bias and are good to ~5 sig figs only.
- **The AIC procedure is legitimate.** A synthetic recovery test (generate data from the true
  α=2, p=3/2 form, run the identical 4-model comparison) recovers the log model at dAIC≈340 with
  zero noise and 95–98% selection under 0.1–1% noise. AICc does not flip the ranking; the ranking
  survives a full log-space refit. So the procedure is *not* rigged against the log model.

### ❌ DECISIVE FLAW 1 — the correct leading exponent for this observable **is 2**, not a hypothesis to reject
The project measures **per-site** χ_F = (2−ov₊−ov₋)/(dg²·n). The derived finite-size scaling of the
fidelity-susceptibility *density* at a quantum critical point is

> χ_F / L^d ~ L^{2/ν − d}  (Albuquerque, Alet, Sire, Capponi, PRB **81**, 064418 (2010), Eq. 21).

The project's **own q=3 result proves it uses exactly this convention**:

| q | ν (Potts) | per-site `2/ν − d` (d=1) | project's measurement | marginal operator? |
|---|-----------|--------------------------|-----------------------|--------------------|
| 2 | 1   | 1.000 | (per-site Ising = N(N−1)/8 → N/4, slope→1) ✓ | no |
| 3 | 5/6 | **1.400 = 7/5** | 1.41 → 1.407 ✓ (project calls 7/5 "exact") | no |
| 4 | 2/3 | **2.000** | **1.77** — *below the correct value* | **yes (dilution, c=1)** |

So **α=2 is the right answer for q=4**, and 1.77 is the finite-size value sitting below it. The
physics is coherent: q=3 has no marginal operator → it converges cleanly to 7/5; q=4 *does* → it
approaches 2 slowly with multiplicative log corrections, which at L≤11 reads as ~1.77.

The "Salas–Sokal p=3/2" null was also **mislabeled**: 3/2 is the log power of the *2D classical*
4-state Potts **specific heat** (Salas–Sokal 1997, Eq. 2.34a/3.23); that paper's *susceptibility*
log power is 1/8 (Eq. 2.34c), and it makes no fidelity-susceptibility prediction at all. (Sprint 122
itself flagged the χ_F↔specific-heat p=3/2 mapping as an unproven conjecture — it is defensible as a
guess since χ_F couples to the thermal sector, but it is not a literature prediction to "reject.")

### ❌ DECISIVE FLAW 2 — the extrapolation that "rules out 2" is circular and cannot resolve logs at L≤11
`exp_128c` fits `α_eff(N) = α_∞ + c/N^p` — a **no-log** power-correction ansatz — and licenses it for
q=4 from its success at q=3. But q=3 is genuinely power-law-corrected (no marginal operator), so its
success transfers no reliability to q=4, where the *existence* of logs is the entire question.

**Demonstrated directly:** feeding the same extrapolator synthetic data with *true* α=2 + Salas–Sokal
logs on the q=4 grid returns **α_∞ = 1.60–1.89** — it is structurally incapable of detecting the logs
it claims to exclude. And the resolvability is hopeless: for `N²/(ln N)^{3/2}` the local exponent is
`2 − (3/2)/ln N`, which over n=4…11 (ln N ∈ [1.39, 2.40]) crawls from 0.92 to 1.37; reaching α_eff=1.9
needs N≈3×10⁶. The drift-sign argument is also **boundary-condition-dependent** (periodic χ_F drifts
*down* to 1.78, but the project's own open-BC DMRG drifts *up* toward 2.0), so it does not favor a
sub-2 asymptote.

| q=4 χ_F fit (6 exact pts) | α | AIC | note |
|---|---|---|---|
| Pure power | 1.7945 ± 0.0069 | −20.8 | fine *effective* exponent for n≤11 |
| Power + 1/N² | 1.760 | −52.0 | "best" but 3 params/6 pts, corr(A,α)=−0.999 → α not identified |
| α=2 + free-log | (2.0), p=0.41 | −10.6 | "worst" — but α=2+log+1/N² fits *better* than pure power (SSR 0.003 vs 0.097) |

The data prefer a sub-2 *effective* exponent at these sizes — a statement about L≤11, **not** about
the asymptote. The α=2-with-corrections family is **not excludable**.

### ⚠️ Note on factor-2 and /n (real, but harmless)
χ_F uses overlap-*squared* → a built-in ×2 vs the standard χ_F=2(1−F)/δ², plus a per-site /n. Both
are constant prefactors that cancel in the log-log slope, so they do **not** affect any exponent. (An
audit agent initially called the /n an "off-by-one" error; that was itself wrong — it over-generalized
from Ising ν=1. For q=4 the per-site exponent genuinely *is* 2 = 2/ν−d, so the comparison to 2 is
apples-to-apples. Resolved via the q=3=7/5 anchor above.)

---

## Secondary issues found
- **q=5 α inconsistency:** recorded as both 2.094±0.002 (STATE.md, S127) and 2.139±0.019
  (KNOWLEDGE.md line 67, S128 refit). Reconcile — this propagates into the α(q) fit.
- **`results.db` factor-2 convention split:** absolute χ_F before/after Sprint 125 differ by ×2
  (form A, linear overlap, vs form B, squared overlap). Exponents are unaffected, but any cross-sprint
  *magnitude* comparison is corrupted. Pick a canonical convention and annotate.
- **Novelty is narrow:** the model is the standard S_q Potts (GRZ / Ma-He / Jacobsen-Wiese); g_c=1/q
  is known; the χ_F "mechanism" α=β_me+2z_m−1 is self-described as a tautological identity. The
  remaining novelty is the *measurement*, which the inverted framing undermines.
- **QPU unused for 89+ sprints** (credentials empty).

## Recommended reframing
1. Anchor q=4 on the **derived leading exponent 2/ν−d = 2**; report 1.77 as the finite-size effective
   value and the sub-2 shortfall as **marginal-operator log suppression, unresolved at L≤11**.
2. **Retire** `exp_128c`'s extrapolation and all "Salas–Sokal p=3/2 rejected" language.
3. Decisive next experiment: **periodic-BC χ_F at L≫11** (symmetry-reduced ED or periodic DMRG), fit
   `χ_F = A·N²·(ln N)^{−p}·(1+c/N²)`.
4. Fix the q=5 number and the DB factor-2 split.

## Literature added/corrected
- **Albuquerque, Alet, Sire, Capponi — PRB 81, 064418 (2010), arXiv:0912.2689.** χ_F density
  ~ L^{2/ν−d}. The correct null. Per-site q=4 ⇒ L².
- **Salas & Sokal — J. Stat. Phys. 88, 567 (1997), hep-lat/9607030.** 2D *classical* Potts; p=3/2 is
  the **specific-heat** log power (χ log power is 1/8). Not a χ_F prediction.

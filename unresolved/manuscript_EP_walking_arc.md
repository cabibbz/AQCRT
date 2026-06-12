# The walking crossover of the transverse-field Potts chain, measured through a thermal-gap exceptional point — and a q-independent decay constant locked to the exact classical interface tension

*Draft manuscript (v1, 2026-06-12), consolidating Sprints 136–141 of an autonomous research
program. Repository: github.com/cabibbz/AQCRT — every number below maps to a script and a
results.db row (reproducibility table in the Appendix). Figures: unresolved/figures/.*

## Abstract

The q-state Potts chain in a transverse field has a first-order quantum transition for q>4
that is *weakly* first order near q=4: the renormalization-group flow passes close to a pair
of complex fixed points ("walking"), producing approximately conformal behavior up to an
exponentially large correlation length ξ(q). We introduce and validate an exceptional-point
(EP) estimator of the thermal scaling: the two lowest Z_q-charge-0 levels form an avoided
crossing whose nearest complex-coupling coalescence sits at Im(g_EP) = Δ_min/c₁, measurable
from real-coupling data alone. Using charge-conserving DMRG on open chains up to n=48 sites
we observe, for the first time in this observable family, the full walking crossover: both
Δ_min(L)·L and Im(g_EP)(L) leave their conformal-shadow power laws *exponentially* once L
exceeds the exact classical correlation length ξ_d(q) of Buffenoir–Wallon — with a null
result at q=6 (ξ=159) ruling out method artifacts, and a registered, parameter-free
prediction at q=7 (Λ_Im = 79±5 from the q=8,10 coefficients; measured 79±25) confirming
Λ ∝ ξ_d blind. In the asymptotic regime (L/ξ up to 3.4) the decay rate saturates at a
dimensionless constant σ̃·ξ_d = 0.24±0.03, *identical at q=8 and q=10* (plateau means 0.256
vs 0.259) — numerically half the exact classical order–disorder interface tension relation
2σ_od·ξ_d = 1 of Borgs–Janke. Two natural explanations are experimentally eliminated: the
classical duality does not transfer naively (σ̃ξ_d = 1/2 excluded at 10σ), and an
amplitude-level transfer fails because the quantum chain's *own* correlation length is
microscopic (ξ_x ≈ 2–4 sites at q=10, decoupled from ξ_d). The result is a sharp open
puzzle: a quantum tunneling rate locked, across q, to a length scale of the isotropic
classical model that the quantum chain's local correlations do not know about.

## 1. Introduction

For Q>4 the two-dimensional Potts model has a first-order transition whose correlation
length ξ(Q) ~ exp(π²/√(Q−4)) grows enormous as Q→4⁺. Gorbenko, Rychkov and Zan [GRZ]
explained this "walking" behavior through a pair of complex conformal field theories at
complex coupling; lattice realizations and analytic continuations of the critical exponents
followed [Ma–He; Jacobsen–Wiese]. On the quantum side, Campostrini, Nespolo, Pelissetto and
Vicari [CNPV] established the finite-size scaling laws at first-order *quantum* transitions,
including the exponential gap closing and its boundary-condition dependence, for the
transverse-field Potts chain

    H = − Σᵢ δ(sᵢ, sᵢ₊₁) − g Σᵢ Σ_{k=1}^{q−1} Xᵢᵏ ,    g_c = 1/q (self-dual).

What has been missing is a *finite-size instrument* that watches a single observable walk:
look conformal below ξ, and visibly leave that regime at L ~ ξ, with the scale set by the
exact classical ξ_d(q) [Buffenoir–Wallon]. This draft reports such an instrument and what it
found, including one result we did not anticipate and currently cannot explain (§3.4–3.5).

## 2. The estimator and methods

**EP estimator (S136).** The thermal (energy-channel) gap Δ_ε(g) between the two lowest
Z_q-charge-0 states has a minimum at a pseudo-critical g*(L). Near g*, the two levels form a
two-level avoided crossing; on open chains its wings are asymmetric and the form

    Δ(g) = sqrt(Δ_min² + (c₁ δ + c₂ δ²)²),   δ = g − g*

describes the data to relative residuals 10⁻⁶–10⁻¹⁵ where the dip is well sampled. The
nearest complex-g coalescence (exceptional point, the quantum analogue of a Fisher zero) is
Im(g_EP) = Δ_min/c₁ to leading order. The estimator was validated against a true
complex-symmetric diagonalization at q=2 (~2%) and recovers the exact thermal exponents
1/ν = 1 (q=2) and 6/5 (q=3) from the scaling Im(g_EP) ~ L^(−1/ν).

**Charge-conserving DMRG (S137).** In the Fourier (charge) basis the field term is diagonal
and the Potts coupling becomes (1/q)[1 + Σ_k Zk_i Zk†_j] with real permutation operators;
total charge is conserved explicitly. Ground and first-excited charge-0 states (the latter
via orthogonalization) reproduce open-boundary exact diagonalization to relative 10⁻⁶ (q=6),
8×10⁻⁵ (q=8) and 3×10⁻⁴ (q=10) at χ=64; production used χ up to 128, n up to 48.

**Fitting discipline.** A four-parameter crossing fit through ~5 points is exact-identified
and hides 5–18% parameter noise behind machine-precision residuals; we therefore require ≥7
points within 3× the minimum gap and refine until the relative residual is below 5×10⁻³ or
its small-n model-error floor (~10⁻²). All finite-size-scaling fits are weighted by these
per-size residuals. Pre-registered predictions and falsifiers were written into the
repository before the corresponding data existed (S138, S139, S140, S141), and an
independent 48-agent code/data audit preceded the arc.

## 3. Results

### 3.1 The crossover, with a null control (S137; Fig. 1)

Plotted against L/ξ_d(q), the gap amplitudes Δ_min·L of q=7, 8, 10 fall on a common
declining trajectory while the q=6 control (ξ_d = 158.9; L/ξ ≤ 0.15) stays flat at its
CFT-like constant (Fig. 1a). Fits of A·L^(−p)·e^(−L/Λ) against pure power laws give
ΔAIC = +17 (q=8) and +37 (q=10) in favor of the exponential term — and ΔAIC ≈ 0 for the
q=6 control, excluding truncation or estimator artifacts (identical χ ladder and code path).
The fitted crossover lengths track the exact classical correlation length:
Λ_Im/ξ_d = 1.59 (q=8) and 1.71 (q=10) while ξ_d itself changes by 2.26×.

### 3.2 A registered, parameter-free prediction at q=7 (S138; Fig. 2)

If Λ ∝ ξ_d is physics, q=7 (ξ_d = 48.1) must show decay onset with
Λ_Im = (1.65±0.09)·ξ_d = 79±5 — written down, with three falsifiers, before any q=7 data.
The measurement (n = 8…40) returned Λ_Im = 79±25, with the decay term independently demanded
(ΔAIC +13 on Δ_min) at the strength implied by the matched-L/ξ q=8 calibration, and the
fixed-Λ=79 fit beating the pure power law with zero adjustable decay parameters.

### 3.3 The asymptotic decay constant (S139; Fig. 3)

Beyond the onset, the local decay rate σ_loc = −d ln(Δ_min L)/dL at q=10 flattens for
L/ξ ≳ 2 at σ_loc·ξ_d ≈ 0.23–0.27 (nine windows, up to L/ξ = 3.4). The exact classical
anchor is the Borgs–Janke order–disorder interface tension, 2σ_od ξ_d = 1: a naive transfer
predicts σ̃·ξ_d = 1/2, which the data exclude (ΔAIC +17 tail-only, +135 in the four-q joint
fit; the local rate sits at half the required level). Fixing σ̃·ξ_d ≡ 1/4 fits the tail as
well as the free fit (s_free = 0.213±0.035).

### 3.4 The velocity test: both explanations die (S140; Fig. 4a)

Two readings could rationalize 1/4: an amplitude-level duality (gap = matrix element,
weight ∝ amplitude², requiring the quantum chain's own correlation length ξ_x ≈ ξ_d), or a
naive duality in proper quantum units (requiring ξ_x ≈ 2ξ_d). Direct measurement of the
disordered-branch correlator at the transition (DMRG, Ornstein–Zernike fits, size-converged
n=48→64) gives ξ_x ≲ 4.3 sites at q=10 — neither. The dispersion cross-check (exact
charge-block diagonalization; near coexistence naive eigenvector filtering fails because the
Lanczos vectors mix the degenerate ordered tower) finds a nearly flat magnon band,
consistent with a microscopic ξ_x. The quantum first-order point thus carries **two
decoupled lengths**: ξ_x ≈ 2–4 sites, and a tunneling scale ≈ 17 sites that tracks the
*classical* ξ_d. Classically these are locked by duality + complete wetting; in the quantum
chain they are demonstrably not.

### 3.5 Universality of the constant (S141; Fig. 3)

The decisive registered test: extend q=8 into its own asymptotic window (n up to 48,
L/ξ = 2.0). The q=8 tail windows flatten at mean σ_loc·ξ_d = 0.256, against the q=10
plateau 0.259 — the same constant to 1% across a 2.26× change of ξ_d. A joint shared-s fit
over both tails gives s = 0.213 ± 0.029: consistent with 1/4 (1.3σ), excluding 0.40 (the
onset value frozen; 6.4σ) and 0.50 (classical duality; 9.9σ). The q=8-only parametric fit is
underpowered (four sizes) — the fit-free plateau and the joint fit carry the verdict.

### 3.6 Where the "conformal shadow" reading is licensed (S136–137; Fig. 4b)

The Coulomb-gas (den Nijs) continuation, exact at Q≤4, gives Re(1/ν_complex) = 1.534, 1.563,
1.588 at q=5, 6, 7. The measured effective exponents (periodic exact diagonalization, L<ξ)
match only at q=5 (1.505); at q=6, 7 they already rise past the complex-CFT value toward the
first-order scale — at L/ξ as small as 0.05–0.15, the crossover contaminates the effective
exponent. Shadow language, used quantitatively, belongs to q=5 alone in this family.

## 4. Discussion: the open puzzle

The arc establishes, with registered tests at each step:

1. Λ_Im = (1.65±0.09)·ξ_d(q) — the crossover onset (q = 7, 8, 10; one point earned blind);
2. σ̃·ξ_d(q) = 0.24±0.03 — the asymptotic decay constant, q-independent (q = 8, 10);
3. ξ_x(quantum) ≈ 2–4 sites at q=10 — decoupled from both.

Result 2 is numerically σ_od·ξ_d/2 with σ_od the *exact* classical tension — yet neither the
naive nor the amplitude-level duality transfer survives experiment, and the quantum chain's
own correlations cannot supply the length. Why does a quantum tunneling rate, in quantum
lattice units, lock across q onto half the exact classical product? Possibilities we cannot
yet distinguish: (i) the extreme-anisotropy (τ-continuum) limit preserves interface free
energies per *classical* unit in a way it does not preserve correlation lengths — calculable
in principle from the integrable structure of the self-dual chain; (ii) the constant is not
exactly 1/4 (our joint value 0.213±0.029 sits 1.3σ low) and matches some other invariant of
the anisotropic limit; (iii) an unrecognized exact relation for the quantum chain's
order–disorder kink free energy. A direct measurement of the quantum interface free energy
(fixed-boundary DMRG energy excess: disordered wall vs ordered wall) is the obvious next
experiment and would localize where the classical normalization enters.

**Relation to prior work.** The exponential gap closing at first-order quantum transitions
and its BC dependence are CNPV's; the exact ξ_d and σ_od are Buffenoir–Wallon's and
Borgs–Janke's; walking and complex CFTs are GRZ's. New here, to our knowledge: the EP
observable and its validation as a 1/ν estimator on the quantum chain; the q-resolved
observation of the walking crossover with a null control and a blind-confirmed Λ ∝ ξ_d law;
the two-length decoupling; and the q-independent σ̃·ξ_d ≈ 1/4 constant against the exact
classical anchor.

**Limitations.** Open boundary conditions throughout the production arc (the crossover is
bulk physics, but BC-dependent prefactors are not resolved); q=8 reaches only L/ξ = 2.0; the
exact value of the constant (1/4 vs 0.21–0.25) is not pinned; all error bars on Λ and s are
fit-derived with per-size residual weights, not bootstrap.

## Appendix: reproducibility map

| Claim | Script(s) | Data |
|---|---|---|
| EP estimator + q=2,3 validation | exp_136a/b, ep_utils | sprint_136*.json; DB im_gEP |
| DMRG vs ED validation (q=6,7,8,10) | exp_137a (SPRINT_NO env) | sprint_137a/138a_validate_q*.json |
| Crossover + null control | exp_137b/c | sprint_137b_crossover_q{6,8,10}.json, sprint_137_analysis.json |
| Blind q=7 prediction | sprint_138.md (registration), exp_138a | sprint_138b_crossover_q7.json, sprint_138_analysis.json |
| Asymptotic constant (q=10) | exp_139a | sprint_139b_crossover_q10.json, sprint_139_analysis.json |
| Velocity test / two lengths | exp_140a/b | sprint_140a_xi_q10.json, sprint_140b_dispersion_q10.json |
| q=8 universality | exp_141a | sprint_141b_crossover_q8.json, sprint_141_analysis.json |
| Figures | exp_142a_figures.py | unresolved/figures/fig1–4 |

Numerical-hygiene rules adopted during the arc (each learned the hard way, see CHANGELOG):
≥7-point crossing fits; per-size residual weighting with floors for exact-identified legacy
fits; exact charge blocks near coexistence; correlator (not v/Δ) for ξ in flat-band regimes;
BC-qualified database quantity names; merge-on-save for accumulating result files.

## References

- V. Gorbenko, S. Rychkov, B. Zan, SciPost Phys. 5, 050 (2018) [GRZ].
- E. Buffenoir, S. Wallon, J. Phys. A 26, 3045 (1993) — exact ξ_d(q) at the transition.
- C. Borgs, W. Janke, J. Phys. I France 2, 2011 (1992) — exact σ_od; 2σ_od ξ_d = 1.
- M. Campostrini, J. Nespolo, A. Pelissetto, E. Vicari, arXiv:1410.8662 [CNPV].
- S.-K. Ma, Y.-C. He ("Shadow of complex fixed point"), arXiv:1811.11189.
- J. L. Jacobsen, K. J. Wiese, PRL 133, 077101 (2024).
- A. F. Albuquerque, F. Alet, C. Sire, S. Capponi, PRB 81, 064418 (2010).

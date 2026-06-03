# Sprint 132 — Restore GPU compute, push q=4 per-site χ_F to the n=12 frontier

**Date:** 2026-06-02
**Thread:** q=4 S_q Potts per-site χ_F effective exponent. STATE Top-Next #1: "(GPU) periodic-BC χ_F
q=4 n=12–14 — watch amplitude exp 1.8→2.0. Core blocker; CPU can't reach (q=4 n=12 = 16.7M).
BLOCKED until CuPy/CUDA restored."
**Environment:** Windows, Python 3.11.9, NVIDIA TITAN RTX (24 GB), driver 591.74 / CUDA 13.1, nvcc 12.6.

## Motivation
The core physics blocker for ~3 sprints has been "CuPy/CUDA unavailable" — every recent sprint fell
back to CPU and could not reach the q=4 n≥12 sizes needed to watch the per-site χ_F amplitude exponent
climb from its finite-size value (~1.79–1.81 at n≤11) toward the predicted asymptote 2/ν−d = 2.0
(ν=2/3, Albuquerque density law). This sprint **restores GPU compute** and uses it to add the first
new data point past the CPU wall.

## Root cause of the GPU outage
`import cupy` failed with `numpy.core.multiarray failed to import` — a hard ABI mismatch:
the installed **cupy-cuda12x 14.0.1 requires numpy≥2.0,<2.6**, but the validated CPU research stack
runs **numpy 1.26.4** (scipy 1.15.3, qiskit 2.3.1, tenpy 1.1.0). The hardware/driver/toolkit were all
fine (nvidia-smi, nvcc 12.6 present). **Surgical fix:** downgrade only the GPU package to
**cupy-cuda12x 13.6.0** (supports numpy 1.22–2.x), pinning numpy==1.26.4 so the entire validated CPU
stack is untouched. No numpy 2.x upgrade → zero risk to the existing 130-sprint CPU codebase/results.

## Plan
1. **exp_132a** — validate the restored GPU pipeline: recompute `chi_F_exact` (canonical finite-diff
   estimator, dg=1e-4, g_c=1/q) at q=4 n=9,10,11 via `gpu_utils.eigsh` (all route to GPU, dim>50k) and
   compare to stored DB values; add a fresh CPU-vs-GPU cross-check at n=9. Must match to ~1e-6.
2. **exp_132b** — the frontier point: q=4 n=12 (dim 16.7M) per-site χ_F on GPU; refit the effective
   exponent on n=4..12 and report the pairwise (n,n+2) slope at the top of the series — does it climb?

## Results
(in progress)

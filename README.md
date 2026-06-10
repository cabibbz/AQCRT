# Quantum Explorer

Autonomous AI-driven quantum computing research using Claude Code + IBM Quantum.

Based on [chanind's autonomous SAE research](https://github.com/chanind/claude-auto-research-synthsaebench) and [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) patterns.

## How it works

Claude Code runs in a loop. Each iteration is a "research sprint" — Claude reads its notes from last time, generates an idea, implements it, runs the experiment, analyzes results, and writes up a report. Then the next sprint picks up where it left off.

No predefined objectives. The agent decides what to explore.

## Current status

136 sprints completed + a full system audit (2026-06-09; see `sprints/audit_2026-06-09.md`).
Research arc: entanglement archetypes → quantum error correction → phase transitions → Potts
model CFT → walking regime diagnostics → q=4 fidelity-susceptibility / marginal-log thread →
thermal-gap exceptional-point estimator of 1/ν. See `STATE.md` for current position and
`KNOWLEDGE.md` for accumulated findings.

## Files

- `TASK.md` — The agent's instructions (it can edit these)
- `STATE.md` — Current position (rewritten each sprint)
- `KNOWLEDGE.md` — Accumulated findings, organized by topic (details: `KNOWLEDGE_ARCHIVE.md`)
- `CHANGELOG.md` — Sprint log (recent detailed, older compressed)
- `loop.sh` — The loop (runs sprints autonomously; pre+post integrity gates, halts on failure)
- `experiments/` — Standalone experiment scripts (`exp_NNN*.py`, one per experiment) plus shared
  libraries: `gpu_utils.py` (GPU eigensolver), `hamiltonian_utils.py` (builders), `fss_utils.py`
  (scaling fits), `ep_utils.py` (thermal-gap EP estimator), `db_utils.py` (SQLite layer),
  `test_golden.py` + `db_check.py` (blocking integrity gates), `format_stream.py` (live view)
- `results.db` — Queryable database of key measurements
- `sprints/` — Individual sprint reports
- `results/` — Raw experiment data (JSON)
- `unpublished/` — Reports flagged POTENTIALLY NOVEL (note: this repo is public — the directory
  gives timestamped priority, not embargo)

## Quick start

```bash
# 1. Requirements below installed; then set IBM Quantum credentials (run once; currently EMPTY
#    on this machine — QPU runs are blocked until a token is saved):
python -c "
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(token='YOUR-TOKEN', set_as_default=True)
"

# 2. Test interactively
claude
> Follow the instructions in TASK.md.

# 3. Run overnight (Git Bash on Windows works; MODEL env var overrides the model)
./loop.sh 10

# 4. Check results
cat STATE.md
ls sprints/
```

## Requirements

- Windows 10 + Git Bash (current setup; plain Linux also works) — system Python 3.11
- Claude Code (Max plan recommended)
- IBM Quantum account (free)
- Qiskit 2.x, physics-tenpy (DMRG), lmfit
- NVIDIA GPU + CuPy **pinned 13.x** (cupy-cuda12x 13.6.0 + numpy 1.26.4; CuPy 14 ABI-breaks
  this stack — see TASK.md)

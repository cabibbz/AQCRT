#!/bin/bash
# Ralph Wiggum Loop — Autonomous Quantum Research
# Based on chanind's SAE research setup
#
# Usage: ./loop.sh [number_of_sprints]
# Default: 10 sprints.  MODEL env var overrides the model (default claude-opus-4-8).
#
# Each sprint: Claude reads TASK.md, does a research sprint,
# logs results, and exits. Next iteration picks up from the notes.

SPRINTS=${1:-10}
MODEL="${MODEL:-claude-opus-4-8}"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

cd "$PROJECT_DIR"
mkdir -p logs

echo "============================================"
echo "  Quantum Explorer — Ralph Wiggum Loop"
echo "  Starting $SPRINTS sprints at $(date)"
echo "  Project: $PROJECT_DIR   Model: $MODEL"
echo "============================================"

# --- integrity gates (BLOCKING: a broken chi_F pipeline or doc<->db drift halts the loop).
# Run BEFORE each sprint (don't compound a broken state) and AFTER each sprint (don't
# let a sprint that broke the math/bookkeeping go undetected until the NEXT run —
# audit 2026-06-09: previously post-sprint corruption was caught one sprint late,
# after it had already been committed and pushed).
run_gates() {
    local label="$1" logfile="$2" fail=0
    echo "[$label] golden-values + db-drift checks -> $logfile"
    if python experiments/test_golden.py > "$logfile" 2>&1; then
        echo "[$label] golden: PASS"
    else
        echo "[$label] golden: *** FAIL ***"; fail=1
    fi
    if python experiments/db_check.py >> "$logfile" 2>&1; then
        echo "[$label] db-check: consistent"
    else
        echo "[$label] db-check: *** DRIFT ***"; fail=1
    fi
    return $fail
}

CLAUDE_FAILS=0

for i in $(seq 1 $SPRINTS); do
    echo ""
    echo ">>> Sprint $i/$SPRINTS — $(date) <<<"
    echo ""

    # --- unpushed-work check (audit 2026-06-09: sprint-136 commits silently sat unpushed;
    # the repo is the scientific record, local disk must not be its only copy) ---
    if git rev-parse --verify -q origin/main >/dev/null; then
        AHEAD=$(git rev-list --count origin/main..main 2>/dev/null || echo 0)
        if [ "${AHEAD:-0}" -gt 0 ]; then
            echo "[preflight] WARNING: $AHEAD local commit(s) not on origin/main — pushing now"
            git push origin main || echo "[preflight] *** push FAILED — fix connectivity/auth; continuing, but the local disk is the only copy ***"
        fi
    fi

    # --- pre-sprint gates ---
    if ! run_gates "preflight" "logs/preflight-$i-$TIMESTAMP.log"; then
        echo ""
        echo "!!! PRE-SPRINT GATE FAILED at sprint $i -- HALTING LOOP."
        echo "    A golden-values regression (broken chi_F math) or a doc<->results.db drift was found."
        echo "    Running further sprints would compound the error. Fix it (see logs/preflight-$i-$TIMESTAMP.log), then restart loop.sh."
        exit 1
    fi

    # --- the sprint ---
    # raw NDJSON -> per-sprint .jsonl (forensic, machine-parseable);  stderr -> .err;
    # stdout -> live, readable VERBOSE view via format_stream.py (thinking, every tool call +
    # inputs, tool results, per-turn tokens). Set STREAM_FULL=1 for untruncated thinking/results.
    SPRINT_LOG="logs/sprint-$i-$TIMESTAMP.jsonl"
    SPRINT_ERR="logs/sprint-$i-$TIMESTAMP.err"
    claude -p "ultrathink. Follow the instructions in TASK.md." \
        --model "$MODEL" \
        --dangerously-skip-permissions \
        --output-format stream-json \
        --verbose \
        --max-turns 3000 \
        2> "$SPRINT_ERR" \
        | tee "$SPRINT_LOG" \
        | python -u experiments/format_stream.py

    # PIPESTATUS[0] = claude's exit (NOT tee's / formatter's), so retry logic sees real failures
    EXIT_CODE=${PIPESTATUS[0]}
    echo "[sprint $i] exit=$EXIT_CODE at $(date) -> $SPRINT_LOG" | tee -a "logs/loop-$TIMESTAMP.log"

    if [ $EXIT_CODE -ne 0 ]; then
        CLAUDE_FAILS=$((CLAUDE_FAILS + 1))
        echo "!!! Sprint $i exited with code $EXIT_CODE — last stderr (full: $SPRINT_ERR):"
        tail -n 20 "$SPRINT_ERR"
        if [ $CLAUDE_FAILS -ge 2 ]; then
            echo "!!! 2 consecutive claude failures — HALTING (outage or systematic problem; blind retries churn partial state)."
            exit 1
        fi
        echo "pausing 60s before next"
        sleep 60
    else
        CLAUDE_FAILS=0
    fi

    # --- post-sprint gates: catch a sprint that broke math/bookkeeping IMMEDIATELY ---
    if ! run_gates "postflight" "logs/postflight-$i-$TIMESTAMP.log"; then
        echo ""
        echo "!!! POST-SPRINT GATE FAILED after sprint $i -- HALTING LOOP."
        echo "    Sprint $i broke a golden anchor or drifted results.db<->docs. Its commits may"
        echo "    already be pushed — fix forward (see logs/postflight-$i-$TIMESTAMP.log), then restart loop.sh."
        exit 1
    fi

    # Brief pause between sprints to avoid rate limits
    echo "--- Cooling down before next sprint ---"
    sleep 10
done

echo ""
echo "============================================"
echo "  Loop complete: $SPRINTS sprints finished"
echo "  $(date)"
echo "  Check CHANGELOG.md for results"
echo "============================================"

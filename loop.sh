#!/bin/bash
# Ralph Wiggum Loop — Autonomous Quantum Research
# Based on chanind's SAE research setup
#
# Usage: ./loop.sh [number_of_sprints]
# Default: 10 sprints
#
# Each sprint: Claude reads TASK.md, does a research sprint,
# logs results, and exits. Next iteration picks up from the notes.

SPRINTS=${1:-10}
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

cd "$PROJECT_DIR"
mkdir -p logs

echo "============================================"
echo "  Quantum Explorer — Ralph Wiggum Loop"
echo "  Starting $SPRINTS sprints at $(date)"
echo "  Project: $PROJECT_DIR"
echo "============================================"

for i in $(seq 1 $SPRINTS); do
    echo ""
    echo ">>> Sprint $i/$SPRINTS — $(date) <<<"
    echo ""

    # --- pre-sprint integrity gates (non-blocking: warn, don't halt research) ---
    PRE="logs/preflight-$i-$TIMESTAMP.log"
    echo "[preflight] golden-values + db-drift checks -> $PRE"
    if python experiments/test_golden.py > "$PRE" 2>&1; then echo "[preflight] golden: PASS"; else echo "[preflight] golden: *** FAIL *** (see $PRE)"; fi
    if python experiments/db_check.py >> "$PRE" 2>&1; then echo "[preflight] db-check: consistent"; else echo "[preflight] db-check: *** DRIFT *** (see $PRE)"; fi

    # --- the sprint (forensic per-sprint NDJSON; stream-json so headless output IS captured) ---
    SPRINT_LOG="logs/sprint-$i-$TIMESTAMP.jsonl"
    claude -p "ultrathink. Follow the instructions in TASK.md." \
        --model claude-opus-4-8 \
        --dangerously-skip-permissions \
        --output-format stream-json \
        --verbose \
        --max-turns 3000 \
        2>&1 | tee "$SPRINT_LOG"

    # PIPESTATUS[0] = claude's exit (NOT tee's), so retry logic actually sees real failures
    EXIT_CODE=${PIPESTATUS[0]}
    echo "[sprint $i] exit=$EXIT_CODE at $(date) -> $SPRINT_LOG" | tee -a "logs/loop-$TIMESTAMP.log"

    if [ $EXIT_CODE -ne 0 ]; then
        echo "!!! Sprint $i exited with code $EXIT_CODE — pausing 60s before next"
        sleep 60
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

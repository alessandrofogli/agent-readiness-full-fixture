#!/usr/bin/env bash
# Capture a flame graph of the running API process (see docs/profiling.md).
set -euo pipefail

PID="${1:-$(pgrep -f 'uvicorn api.main:app' | head -1 || true)}"
OUT="${2:-profile.svg}"

if [ -z "${PID}" ]; then
  echo "No running API process found. Start it with: make up && uv run uvicorn api.main:app"
  exit 1
fi

echo "Sampling PID ${PID} for 30s -> ${OUT}"
uv run py-spy record --pid "${PID}" --output "${OUT}" --duration 30
echo "Flame graph written to ${OUT}"

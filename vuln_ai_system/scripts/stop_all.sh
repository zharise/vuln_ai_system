#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for name in api vllm; do
  pid_file="data/runs/services/${name}.pid"
  if [ -f "$pid_file" ]; then
    kill "$(cat "$pid_file")" 2>/dev/null || true
    rm -f "$pid_file"
  fi
done


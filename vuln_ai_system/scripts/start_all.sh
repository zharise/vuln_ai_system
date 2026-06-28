#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/runs/services

if [ "${START_VLLM:-1}" = "1" ]; then
  nohup ./scripts/start_vllm.sh > data/runs/services/vllm.log 2>&1 &
  echo $! > data/runs/services/vllm.pid
fi

nohup ./scripts/start_api.sh > data/runs/services/api.log 2>&1 &
echo $! > data/runs/services/api.pid

echo "api: http://127.0.0.1:18080"
echo "vllm: http://127.0.0.1:8000/v1"


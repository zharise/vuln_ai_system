#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${MODEL_PATH:-/opt/aivuln/models/Qwen2.5-Coder-7B-Instruct}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

export VLLM_USE_MODELSCOPE="${VLLM_USE_MODELSCOPE:-False}"
export ASCEND_RT_VISIBLE_DEVICES="${ASCEND_RT_VISIBLE_DEVICES:-0,1,2,3}"
export PYTORCH_NPU_ALLOC_CONF="${PYTORCH_NPU_ALLOC_CONF:-expandable_segments:True}"

exec python3 -m vllm.entrypoints.openai.api_server \
  --host "$HOST" \
  --port "$PORT" \
  --model "$MODEL_PATH" \
  --served-model-name Qwen2.5-Coder-7B-Instruct \
  --trust-remote-code \
  --tensor-parallel-size "${TENSOR_PARALLEL_SIZE:-4}" \
  --max-model-len "${MAX_MODEL_LEN:-32768}" \
  --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION:-0.85}"

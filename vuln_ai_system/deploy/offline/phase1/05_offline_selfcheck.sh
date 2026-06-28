#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/aivuln}"
source "$APP_DIR/.venv/bin/activate"

python - <<'PY'
mods = [
    "numpy", "pandas", "openpyxl", "yaml", "requests",
    "fastapi", "uvicorn", "pydantic", "transformers",
]
for m in mods:
    __import__(m)
print("base imports ok")
PY

python - <<'PY'
try:
    import vllm
    print("vllm import ok", vllm.__version__)
except Exception as e:
    print("vllm import failed:", repr(e))
PY

command -v npu-smi >/dev/null 2>&1 && npu-smi info || echo "npu-smi not found"

echo "phase1 offline selfcheck done"


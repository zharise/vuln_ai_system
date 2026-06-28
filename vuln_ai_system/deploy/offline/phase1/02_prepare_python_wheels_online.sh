#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/opt/aivuln_offline}"
WHEEL_DIR="$ROOT_DIR/wheelhouse-base"
mkdir -p "$WHEEL_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3.10}"
command -v "$PYTHON_BIN"

cat > "$ROOT_DIR/requirements-base.txt" <<'REQ'
numpy==1.26.4
pandas==2.2.3
openpyxl==3.1.5
PyYAML==6.0.2
requests==2.32.3
fastapi==0.115.6
uvicorn==0.34.0
pydantic==2.10.4
transformers==4.48.3
accelerate==1.3.0
sentencepiece==0.2.0
safetensors==0.5.2
tiktoken==0.8.0
einops==0.8.0
psutil==6.1.1
REQ

"$PYTHON_BIN" -m pip download -r "$ROOT_DIR/requirements-base.txt" -d "$WHEEL_DIR"

cat > "$ROOT_DIR/install_python_env_offline.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${APP_DIR:-/opt/aivuln}"
PYTHON_BIN="${PYTHON_BIN:-python3.10}"
cd "$(dirname "$0")"
mkdir -p "$APP_DIR"
"$PYTHON_BIN" -m venv "$APP_DIR/.venv"
source "$APP_DIR/.venv/bin/activate"
python -m pip install --no-index --find-links wheelhouse-base -r requirements-base.txt
python - <<'PY'
import numpy, pandas, openpyxl, yaml, requests, fastapi, pydantic, transformers
print("base python deps ok")
PY
SH
chmod +x "$ROOT_DIR/install_python_env_offline.sh"

echo "Base wheelhouse ready: $WHEEL_DIR"


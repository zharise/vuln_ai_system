#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/opt/aivuln_offline}"
WHEEL_DIR="$ROOT_DIR/wheelhouse-vllm-ascend"
mkdir -p "$WHEEL_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3.10}"
command -v "$PYTHON_BIN"

cat > "$ROOT_DIR/requirements-vllm-ascend.txt" <<'REQ'
vllm-ascend==0.18.0
modelscope==1.26.0
REQ

"$PYTHON_BIN" -m pip download \
  --extra-index-url https://mirrors.huaweicloud.com/ascend/repos/pypi/variant \
  --extra-index-url https://mirrors.huaweicloud.com/ascend/repos/pypi \
  -r "$ROOT_DIR/requirements-vllm-ascend.txt" \
  -d "$WHEEL_DIR"

cat > "$ROOT_DIR/install_vllm_ascend_offline.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${APP_DIR:-/opt/aivuln}"
cd "$(dirname "$0")"
source "$APP_DIR/.venv/bin/activate"
python -m pip install --no-index --find-links wheelhouse-vllm-ascend -r requirements-vllm-ascend.txt
python - <<'PY'
import vllm
print("vllm import ok", vllm.__version__)
PY
SH
chmod +x "$ROOT_DIR/install_vllm_ascend_offline.sh"

echo "vLLM Ascend wheelhouse ready: $WHEEL_DIR"


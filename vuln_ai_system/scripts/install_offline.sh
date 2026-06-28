#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
source .venv/bin/activate
pip install --no-index --find-links wheelhouse -r requirements.txt
if [ -d wheelhouse-vllm-ascend ]; then
  pip install --no-index --find-links wheelhouse-vllm-ascend -r requirements-vllm-ascend.txt
fi
chmod +x scripts/*.sh
echo "installed"

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p wheelhouse-vllm-ascend
python3 -m pip download \
  --extra-index-url https://mirrors.huaweicloud.com/ascend/repos/pypi/variant \
  --extra-index-url https://mirrors.huaweicloud.com/ascend/repos/pypi \
  -r requirements-vllm-ascend.txt \
  -d wheelhouse-vllm-ascend
echo "wheelhouse-vllm-ascend ready"

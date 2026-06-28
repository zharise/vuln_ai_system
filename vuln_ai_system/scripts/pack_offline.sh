#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p wheelhouse offline_bundle
python3 -m pip download -r requirements.txt -d wheelhouse
tar czf offline_bundle/aivuln_offline_bundle.tar.gz \
  config src scripts deploy docs requirements.txt requirements-vllm-ascend.txt pyproject.toml \
  wheelhouse models data/source data/targets
echo "offline_bundle/aivuln_offline_bundle.tar.gz"

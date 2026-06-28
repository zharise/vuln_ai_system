#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
mkdir -p data/source data/targets data/runs
touch data/targets/targets.txt
python3 -m aivuln.cli --config config/system.yaml "$@"

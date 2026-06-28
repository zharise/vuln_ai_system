#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
exec uvicorn aivuln.api:app --host 0.0.0.0 --port 18080


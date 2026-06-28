#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/opt/aivuln_offline}"
OUT="${OUT:-/opt/aivuln_phase1_offline_bundle.tar.gz}"

tar czf "$OUT" -C "$(dirname "$ROOT_DIR")" "$(basename "$ROOT_DIR")"
sha256sum "$OUT" > "$OUT.sha256"

echo "$OUT"
echo "$OUT.sha256"


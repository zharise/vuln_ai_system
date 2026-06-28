#!/usr/bin/env bash
set -euo pipefail

ASCEND_PKG_DIR="${ASCEND_PKG_DIR:-/opt/aivuln_offline/ascend_pkgs}"

if [ ! -d "$ASCEND_PKG_DIR" ]; then
  echo "missing $ASCEND_PKG_DIR"
  exit 2
fi

chmod +x "$ASCEND_PKG_DIR"/*.run

for pkg in "$ASCEND_PKG_DIR"/Ascend-hdk-*.run "$ASCEND_PKG_DIR"/Ascend-cann-toolkit_*.run "$ASCEND_PKG_DIR"/Ascend-cann-nnal_*.run "$ASCEND_PKG_DIR"/Ascend-cann-kernels-*.run; do
  [ -f "$pkg" ] || continue
  echo "install $pkg"
  "$pkg" --quiet --install
done

if [ -f /usr/local/Ascend/ascend-toolkit/set_env.sh ]; then
  grep -q "ascend-toolkit/set_env.sh" /etc/profile || echo "source /usr/local/Ascend/ascend-toolkit/set_env.sh" >> /etc/profile
  source /usr/local/Ascend/ascend-toolkit/set_env.sh
fi

command -v npu-smi >/dev/null 2>&1 && npu-smi info || true
echo "Ascend runtime install step done"


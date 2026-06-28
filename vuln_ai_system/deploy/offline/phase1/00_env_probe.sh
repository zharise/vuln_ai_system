#!/usr/bin/env bash
set -euo pipefail

echo "[OS]"
cat /etc/os-release || true
uname -a

echo "[CPU/MEM/DISK]"
lscpu | egrep 'CPU\\(s\\)|Model name|Socket|Core|Thread' || true
free -h
df -h

echo "[ASCEND]"
command -v npu-smi >/dev/null 2>&1 && npu-smi info || echo "npu-smi not found"
ls -ld /usr/local/Ascend 2>/dev/null || true

echo "[PYTHON]"
command -v python3 && python3 --version || true
command -v python3.10 && python3.10 --version || true

echo "[NETWORK]"
ip addr | head -80 || true


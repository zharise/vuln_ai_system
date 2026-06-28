#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
install -d /opt/aivuln
cp -a . /opt/aivuln
chmod +x /opt/aivuln/scripts/*.sh
cp deploy/systemd/aivuln-api.service /etc/systemd/system/
cp deploy/systemd/aivuln-vllm.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable aivuln-api aivuln-vllm
echo "systemd installed"


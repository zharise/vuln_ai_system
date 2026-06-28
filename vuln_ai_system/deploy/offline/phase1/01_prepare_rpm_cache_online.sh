#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/opt/aivuln_offline}"
RPM_DIR="$ROOT_DIR/rpms"
mkdir -p "$RPM_DIR"

dnf makecache
dnf install -y dnf-plugins-core || true

PKGS=(
  gcc gcc-c++ make cmake ninja-build
  git git-lfs tar gzip bzip2 xz unzip zip
  openssl openssl-devel libffi-devel zlib-devel bzip2-devel xz-devel sqlite-devel readline-devel
  python3 python3-devel python3-pip python3-virtualenv
  python3.10 python3.10-devel python3.10-pip
  numactl numactl-devel hwloc
  pciutils lsof net-tools iproute iputils bind-utils
  rsync vim tmux htop
)

dnf download --resolve --alldeps --destdir "$RPM_DIR" "${PKGS[@]}"

cat > "$ROOT_DIR/install_rpms_offline.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dnf install -y --disablerepo='*' rpms/*.rpm
SH
chmod +x "$ROOT_DIR/install_rpms_offline.sh"

echo "RPM cache ready: $RPM_DIR"


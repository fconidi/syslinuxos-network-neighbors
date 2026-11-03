#!/bin/bash
set -euo pipefail
umask 022

HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:?usage: build-deb.sh OUTPUT_DIRECTORY}"
mkdir -p "$OUT"
OUT="$(realpath "$OUT")"
STAGE="$(mktemp -d "$OUT/package.XXXXXX")"
chmod 755 "$STAGE"
trap 'rm -rf -- "$STAGE"' EXIT

install -Dm644 "$HERE/packaging/control" "$STAGE/DEBIAN/control"
install -Dm755 "$HERE/source/launcher" "$STAGE/usr/bin/syslinuxos-network-neighbors"
for source in backend.py i18n.py app.py; do
    install -Dm644 "$HERE/source/$source" "$STAGE/usr/lib/syslinuxos-network-neighbors/$source"
done
install -Dm755 "$HERE/source/read-helper" "$STAGE/usr/lib/syslinuxos-network-neighbors/read-helper"
install -Dm644 "$HERE/packaging/com.syslinuxos.network-neighbors.read.policy" \
    "$STAGE/usr/share/polkit-1/actions/com.syslinuxos.network-neighbors.read.policy"
install -Dm644 "$HERE/packaging/syslinuxos-network-neighbors.desktop" \
    "$STAGE/usr/share/applications/syslinuxos-network-neighbors.desktop"
install -Dm644 "$HERE/packaging/syslinuxos-network-neighbors.menu" \
    "$STAGE/etc/xdg/menus/applications-merged/syslinuxos-network-neighbors.menu"
printf '%s\n' '/etc/xdg/menus/applications-merged/syslinuxos-network-neighbors.menu' \
    > "$STAGE/DEBIAN/conffiles"
install -Dm644 "$HERE/README.md" "$STAGE/usr/share/doc/syslinuxos-network-neighbors/README.md"
install -Dm644 "$HERE/LICENSE" "$STAGE/usr/share/doc/syslinuxos-network-neighbors/copyright"

desktop-file-validate "$STAGE/usr/share/applications/syslinuxos-network-neighbors.desktop"
python3 - "$STAGE/usr/share/polkit-1/actions/com.syslinuxos.network-neighbors.read.policy" <<'PY'
import sys
import xml.etree.ElementTree as ET
ET.parse(sys.argv[1])
PY
python3 - "$STAGE/etc/xdg/menus/applications-merged/syslinuxos-network-neighbors.menu" <<'PY'
import sys
import xml.etree.ElementTree as ET
ET.parse(sys.argv[1])
PY
dpkg-deb --root-owner-group --build "$STAGE" "$OUT/syslinuxos-network-neighbors_0.1.0_all.deb"

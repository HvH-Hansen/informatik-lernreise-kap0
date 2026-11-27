#!/usr/bin/env bash
# Installer für Linux (ext4 / Btrfs / XFS / ZFS)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/index.html" ]; then
  SRC_DIR="$SCRIPT_DIR"
else
  SRC_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

SYSTEM_MODE=0
if [ "${1:-}" = "--system" ] || [ "$(id -u)" -eq 0 ]; then
  SYSTEM_MODE=1
fi

if [ "$SYSTEM_MODE" -eq 1 ]; then
  INSTALL_DIR="/opt/informatik-lernreise-kap0"
  BIN_DIR="/usr/local/bin"
  APP_DIR="/usr/share/applications"
  ICON_DIR="/usr/share/icons/hicolor/scalable/apps"
else
  INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/informatik-lernreise-kap0"
  BIN_DIR="$HOME/.local/bin"
  APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
  ICON_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor/scalable/apps"
fi

echo "=== Informatik Lernreise Kapitel 0 Installer (Linux) ==="
echo "Zielverzeichnis: $INSTALL_DIR"

mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$APP_DIR" "$ICON_DIR"

if [ "$SRC_DIR" != "$INSTALL_DIR" ]; then
  for item in VERSION LICENSE NOTICE README.md CHANGELOG.md ANLEITUNG_Kollegium_Einrichtung.md ANLEITUNG_Google_Sheets_Anbindung.md index.html config.example.js Start_Lernreise.command google_apps_script scripts assets; do
    if [ -e "$SRC_DIR/$item" ]; then
      rm -rf "$INSTALL_DIR/$item"
      cp -a "$SRC_DIR/$item" "$INSTALL_DIR/$item"
    fi
  done
  if [ ! -f "$INSTALL_DIR/config.js" ] && [ -f "$INSTALL_DIR/config.example.js" ]; then
    cp "$INSTALL_DIR/config.example.js" "$INSTALL_DIR/config.js"
  fi
fi

cat > "$BIN_DIR/informatik-lernreise-kap0" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$INSTALL_DIR"
for cand in python3 python; do
  if command -v "\$cand" >/dev/null 2>&1; then
    if "\$cand" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then
      exec "\$cand" "$INSTALL_DIR/scripts/serve_local.py" --open-browser "\$@"
    fi
  fi
done
exec xdg-open "$INSTALL_DIR/index.html"
EOF
chmod +x "$BIN_DIR/informatik-lernreise-kap0"

if [ -f "$INSTALL_DIR/assets/icon.svg" ]; then
  cp "$INSTALL_DIR/assets/icon.svg" "$ICON_DIR/informatik-lernreise-kap0.svg"
fi

cat > "$APP_DIR/informatik-lernreise-kap0.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Informatik Lernreise Kapitel 0
GenericName=Interaktive Informatik-Lernreise (Klasse 5/6)
Comment=Mediatown – 6 Lernstationen mit Google-Sheets-Auswertung & Offline-Modus
Exec=$BIN_DIR/informatik-lernreise-kap0
Icon=informatik-lernreise-kap0
Terminal=false
Categories=Education;
Keywords=Schule;Informatik;Lernreise;Mediatown;
StartupNotify=true
EOF

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APP_DIR" >/dev/null 2>&1 || true
fi

echo "[OK] Installation abgeschlossen. Startbefehl: informatik-lernreise-kap0"

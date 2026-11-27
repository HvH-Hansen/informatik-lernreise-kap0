#!/usr/bin/env bash
# Installer für macOS (APFS / HFS+)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_BUNDLE_NAME="Informatik Lernreise Kap0.app"

if [ -d "$SCRIPT_DIR/$APP_BUNDLE_NAME" ]; then
  SRC_APP="$SCRIPT_DIR/$APP_BUNDLE_NAME"
elif [ -d "$SCRIPT_DIR/../$APP_BUNDLE_NAME" ]; then
  SRC_APP="$SCRIPT_DIR/../$APP_BUNDLE_NAME"
else
  echo "[FEHLER] App-Bundle '$APP_BUNDLE_NAME' nicht gefunden." >&2
  exit 1
fi

TARGET_DIR="${1:-/Applications}"
if [ ! -w "$TARGET_DIR" ]; then
  TARGET_DIR="$HOME/Applications"
  mkdir -p "$TARGET_DIR"
fi

DEST_APP="$TARGET_DIR/$APP_BUNDLE_NAME"
echo "=== Informatik Lernreise Kapitel 0 Installer (macOS) ==="
echo "Installiere App-Bundle nach: $DEST_APP"

BACKUP_CFG=""
EXISTING_CFG="$DEST_APP/Contents/Resources/app/config.js"
if [ -f "$EXISTING_CFG" ]; then
  BACKUP_CFG="$(mktemp)"
  cp "$EXISTING_CFG" "$BACKUP_CFG"
fi

rm -rf "$DEST_APP"
cp -R "$SRC_APP" "$DEST_APP"
chmod +x "$DEST_APP/Contents/MacOS/Informatik-Lernreise-Kap0" || true

if [ -n "$BACKUP_CFG" ] && [ -f "$BACKUP_CFG" ]; then
  cp "$BACKUP_CFG" "$DEST_APP/Contents/Resources/app/config.js"
  rm -f "$BACKUP_CFG"
  echo "Bestehende config.js wurde beibehalten."
fi

if command -v xattr >/dev/null 2>&1; then
  xattr -dr com.apple.quarantine "$DEST_APP" >/dev/null 2>&1 || true
fi

echo "[OK] Installation abgeschlossen: $DEST_APP"

#!/usr/bin/env bash
# Deinstaller für Linux (belässt Nutzer-config.js, falls im Systemmodus nicht gelöscht werden soll)
set -euo pipefail

if [ "${1:-}" = "--system" ] || [ "$(id -u)" -eq 0 ]; then
  rm -rf /opt/informatik-lernreise-kap0
  rm -f /usr/local/bin/informatik-lernreise-kap0
  rm -f /usr/share/applications/informatik-lernreise-kap0.desktop
  rm -f /usr/share/icons/hicolor/scalable/apps/informatik-lernreise-kap0.svg
else
  rm -rf "${XDG_DATA_HOME:-$HOME/.local/share}/informatik-lernreise-kap0"
  rm -f "$HOME/.local/bin/informatik-lernreise-kap0"
  rm -f "${XDG_DATA_HOME:-$HOME/.local/share}/applications/informatik-lernreise-kap0.desktop"
  rm -f "${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor/scalable/apps/informatik-lernreise-kap0.svg"
fi

echo "[OK] Informatik Lernreise Kapitel 0 wurde entfernt."

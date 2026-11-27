#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

PY_BIN=""
for cand in python3 /opt/homebrew/bin/python3 /usr/local/bin/python3 python; do
  if command -v "$cand" >/dev/null 2>&1; then
    if "$cand" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then
      PY_BIN="$cand"
      break
    fi
  fi
done

if [ -n "$PY_BIN" ]; then
  exec "$PY_BIN" scripts/serve_local.py --open-browser "$@"
fi

echo "[HINWEIS] Python 3 nicht gefunden – öffne index.html direkt im Browser."
if command -v open >/dev/null 2>&1; then
  exec open "index.html"
elif command -v xdg-open >/dev/null 2>&1; then
  exec xdg-open "index.html"
fi
echo "Bitte index.html manuell im Browser öffnen." >&2
exit 1

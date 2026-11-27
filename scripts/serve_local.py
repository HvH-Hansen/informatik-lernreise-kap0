#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/serve_local.py
======================
Lokaler HTTP-Starter (127.0.0.1) für die Informatik Lernreise Kapitel 0.
Nutzt ausschließlich die Python-Standardbibliothek (keine externen Pakete nötig).
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import socketserver
import sys
import threading
import urllib.request
import webbrowser
from pathlib import Path

APP_VERSION = "0.4.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class QuietNoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """Serviert statische Dateien und verhindert Caching von config.js."""

    def end_headers(self) -> None:
        if self.path.split("?", 1)[0].endswith("/config.js") or self.path.split("?", 1)[0] == "/config.js":
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.send_header("Pragma", "no-cache")
        super().end_headers()

    def log_message(self, fmt: str, *args: object) -> None:
        return


class ReusableThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def read_endpoint_status() -> str:
    cfg = PROJECT_ROOT / "config.js"
    if not cfg.is_file():
        return "Offline-/Lokalmodus (keine config.js)"
    text = cfg.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"endpointUrl\s*:\s*['\"]([^'\"]*)['\"]", text)
    url = m.group(1).strip() if m else ""
    if re.match(r"^https?://", url, re.I):
        return "Google Sheets aktiv (Cloud-Sync)"
    return "Offline-/Lokalmodus (endpointUrl leer)"


def bind_local_server(preferred_port: int) -> ReusableThreadingHTTPServer:
    handler = functools.partial(QuietNoCacheHandler, directory=str(PROJECT_ROOT))
    ports = [preferred_port] if preferred_port == 0 else [*range(preferred_port, preferred_port + 20), 0]
    last_err: OSError | None = None
    for port in ports:
        try:
            return ReusableThreadingHTTPServer(("127.0.0.1", port), handler)
        except OSError as exc:
            last_err = exc
    raise RuntimeError(f"Lokaler Server konnte nicht gestartet werden: {last_err}")


def run_selftest() -> int:
    required = [
        PROJECT_ROOT / "index.html",
        PROJECT_ROOT / "config.js",
        PROJECT_ROOT / "google_apps_script" / "Code.gs",
        PROJECT_ROOT / "VERSION",
    ]
    missing = [p.relative_to(PROJECT_ROOT).as_posix() for p in required if not p.is_file()]
    if missing:
        print(f"[FAIL] Fehlende Pflichtdateien: {', '.join(missing)}", file=sys.stderr)
        return 1

    srv = bind_local_server(0)
    port = srv.server_address[1]
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    try:
        for route in ("/index.html", "/config.js"):
            url = f"http://127.0.0.1:{port}{route}"
            with urllib.request.urlopen(url, timeout=5) as resp:
                if resp.status != 200:
                    print(f"[FAIL] Unerwarteter Status {resp.status} für {route}", file=sys.stderr)
                    return 1
                body = resp.read()
                if not body:
                    print(f"[FAIL] Leere Antwort für {route}", file=sys.stderr)
                    return 1
                if route == "/config.js":
                    cc = resp.headers.get("Cache-Control", "")
                    if "no-store" not in cc:
                        print(f"[FAIL] Cache-Control no-store fehlt für /config.js ({cc!r})", file=sys.stderr)
                        return 1
    finally:
        srv.shutdown()
        srv.server_close()

    print(f"[PASS] Informatik Lernreise v{APP_VERSION} Selftest erfolgreich ({read_endpoint_status()}).")
    return 0


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Lokaler Starter für Informatik Lernreise Kapitel 0")
    parser.add_argument("--port", type=int, default=8780, help="Bevorzugter lokaler Port (Standard: 8780)")
    parser.add_argument("--open-browser", action="store_true", help="Lernreise direkt im Standardbrowser öffnen")
    parser.add_argument("--selftest", action="store_true", help="Selbsttest ausführen und beenden")
    args = parser.parse_args()

    if args.selftest:
        sys.exit(run_selftest())

    srv = bind_local_server(args.port)
    port = srv.server_address[1]
    url = f"http://127.0.0.1:{port}/index.html"
    print(f"=== Informatik Lernreise Kapitel 0 (v{APP_VERSION}) ===")
    print(f"Lokale Adresse : {url}")
    print(f"Sync-Status    : {read_endpoint_status()}")
    print("Beenden mit Strg+C (dieses Fenster offen lassen, solange gelernt wird).")

    if args.open_browser:
        threading.Timer(0.25, lambda: webbrowser.open(url)).start()

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nLokaler Server beendet.")
    finally:
        srv.shutdown()
        srv.server_close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_packages.py
=========================
Deterministischer Cross-OS Paket- & Archiv-Builder für die Informatik Lernreise Kapitel 0.
Nutzt ausschließlich die Python-Standardbibliothek (0 externe Build-Abhängigkeiten).

Wichtige DSGVO-Regel:
In ALLEN ausgelieferten Paketen/Archiven wird `config.js` aus `config.example.js`
erzeugt (leere `endpointUrl`), niemals mit der persönlichen Apps-Script-URL aus dem Repo.

Copyright (c) 2025-2026 HvH-Hansen (MIT License)
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import stat
import sys
import tarfile
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = PROJECT_ROOT / "VERSION"
DIST_ROOT = PROJECT_ROOT / "dist"

CORE_FILES = [
    "VERSION",
    "LICENSE",
    "NOTICE",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "ANLEITUNG_Kollegium_Einrichtung.md",
    "ANLEITUNG_Google_Sheets_Anbindung.md",
    "index.html",
    "config.example.js",
    "config.js",
    "Start_Lernreise.bat",
    "Start_Lernreise.command",
]

RUNTIME_FILES = [
    "VERSION",
    "LICENSE",
    "NOTICE",
    "README.md",
    "CHANGELOG.md",
    "ANLEITUNG_Kollegium_Einrichtung.md",
    "ANLEITUNG_Google_Sheets_Anbindung.md",
    "index.html",
    "config.example.js",
    "config.js",
    "Start_Lernreise.bat",
    "Start_Lernreise.command",
]

CORE_DIRS = [
    "google_apps_script",
    "scripts",
    "assets",
    "tests",
    "packaging",
    ".github",
    ".githooks",
]

RUNTIME_DIRS = [
    "google_apps_script",
    "scripts",
    "assets",
]

EXCLUDED_DIR_NAMES = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "dist",
    "build",
    "scratch",
    "Schuelerdaten",
    ".pytest_cache",
}

EXECUTABLE_SUFFIXES = {".sh", ".command"}
LF_SUFFIXES = {".sh", ".command", ".py", ".js", ".css", ".html", ".json", ".md", ".yml", ".yaml", ".spec", ".desktop", ".svg"}
CRLF_SUFFIXES = {".bat", ".ps1", ".iss"}


def read_version() -> str:
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    return "0.4.0"


def should_include_path(rel_path: Path) -> bool:
    for part in rel_path.parts:
        if part in EXCLUDED_DIR_NAMES:
            return False
    name = rel_path.name
    if name in {".DS_Store", "Thumbs.db", "desktop.ini"} or name.endswith((".pyc", ".pyo", ".log", ".tmp", ".bak", ".csv", ".xlsx")):
        return False
    if name == ".env" or name.startswith(".env."):
        return False
    return True


def collect_project_files(include_dev_meta: bool = True) -> list[tuple[Path, Path]]:
    """Liefert (quellpfad, relativer_pfad) deterministisch sortiert. `config.js` nutzt immer `config.example.js`."""
    entries: list[tuple[Path, Path]] = []
    example_cfg = PROJECT_ROOT / "config.example.js"

    files_list = CORE_FILES if include_dev_meta else RUNTIME_FILES
    for fname in files_list:
        src = example_cfg if (fname == "config.js" and example_cfg.is_file()) else (PROJECT_ROOT / fname)
        if src.is_file():
            entries.append((src, Path(fname)))

    dirs = CORE_DIRS if include_dev_meta else RUNTIME_DIRS
    for dname in dirs:
        dpath = PROJECT_ROOT / dname
        if not dpath.is_dir():
            continue
        for root, dirnames, filenames in os.walk(dpath):
            dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIR_NAMES)
            for fn in sorted(filenames):
                abs_p = Path(root) / fn
                rel_p = abs_p.relative_to(PROJECT_ROOT)
                if not include_dev_meta and rel_p.parts[:2] == ("scripts", "release_manager.py"):
                    continue
                if not include_dev_meta and rel_p.parts[:2] == ("scripts", "build_packages.py"):
                    continue
                if should_include_path(rel_p):
                    entries.append((abs_p, rel_p))

    entries.sort(key=lambda pair: pair[1].as_posix())
    return entries


def normalize_payload(abs_path: Path, rel_path: Path, target_os: str) -> bytes:
    data = abs_path.read_bytes()
    suffix = rel_path.suffix.lower()
    is_hook = rel_path.parent.as_posix() == ".githooks"

    if target_os == "windows" and suffix in CRLF_SUFFIXES:
        text = data.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\n", "\r\n")
        return text.encode("utf-8")

    if target_os in ("posix", "linux", "macos") and (suffix in LF_SUFFIXES or is_hook):
        try:
            text = data.decode("utf-8")
            return text.replace("\r\n", "\n").encode("utf-8")
        except UnicodeDecodeError:
            return data

    return data


def posix_mode(rel_path: Path) -> int:
    suffix = rel_path.suffix.lower()
    if suffix in EXECUTABLE_SUFFIXES or rel_path.parent.as_posix() == ".githooks":
        return 0o755
    return 0o644


def add_tar_bytes(tf: tarfile.TarFile, arcname: str, data: bytes, mode: int = 0o644, mtime: int = 1764240000) -> None:
    ti = tarfile.TarInfo(name=arcname)
    ti.size = len(data)
    ti.mode = mode
    ti.mtime = mtime
    ti.uid = 0
    ti.gid = 0
    ti.uname = "root"
    ti.gname = "root"
    ti.type = tarfile.REGTYPE
    tf.addfile(ti, io.BytesIO(data))


def add_tar_dir(tf: tarfile.TarFile, arcname: str, mode: int = 0o755, mtime: int = 1764240000) -> None:
    ti = tarfile.TarInfo(name=arcname.rstrip("/"))
    ti.type = tarfile.DIRTYPE
    ti.mode = mode
    ti.mtime = mtime
    ti.uid = 0
    ti.gid = 0
    ti.uname = "root"
    ti.gname = "root"
    tf.addfile(ti)


def add_zip_bytes(zf: zipfile.ZipFile, arcname: str, data: bytes, mode: int = 0o644) -> None:
    zi = zipfile.ZipInfo(arcname, date_time=(2026, 11, 27, 12, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.create_system = 3
    zi.external_attr = (stat.S_IFREG | mode) << 16
    zf.writestr(zi, data)


def build_source_archives(out_dir: Path, version: str, files: list[tuple[Path, Path]]) -> list[Path]:
    prefix = f"informatik-lernreise-kap0-v{version}"
    tgz_path = out_dir / f"{prefix}-source.tar.gz"
    zip_path = out_dir / f"{prefix}-source.zip"

    with tarfile.open(tgz_path, "w:gz", format=tarfile.PAX_FORMAT) as tf:
        for abs_p, rel_p in files:
            payload = normalize_payload(abs_p, rel_p, "posix")
            add_tar_bytes(tf, f"{prefix}/{rel_p.as_posix()}", payload, mode=posix_mode(rel_p))

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for abs_p, rel_p in files:
            payload = normalize_payload(abs_p, rel_p, "posix")
            add_zip_bytes(zf, f"{prefix}/{rel_p.as_posix()}", payload, mode=posix_mode(rel_p))

    return [tgz_path, zip_path]


def build_windows_package(out_dir: Path, version: str, files: list[tuple[Path, Path]]) -> Path:
    prefix = f"informatik-lernreise-kap0-v{version}-windows"
    zip_path = out_dir / f"informatik-lernreise-kap0-v{version}-windows-x64.zip"

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for abs_p, rel_p in files:
            payload = normalize_payload(abs_p, rel_p, "windows")
            add_zip_bytes(zf, f"{prefix}/{rel_p.as_posix()}", payload, mode=posix_mode(rel_p))

        for fname in ("install_windows.ps1", "uninstall_windows.ps1"):
            src = PROJECT_ROOT / "packaging" / "windows" / fname
            if src.is_file():
                payload = normalize_payload(src, Path(fname), "windows")
                add_zip_bytes(zf, f"{prefix}/{fname}", payload, mode=0o644)

    return zip_path


def build_linux_archives(out_dir: Path, version: str, files: list[tuple[Path, Path]]) -> list[Path]:
    prefix = f"informatik-lernreise-kap0-v{version}-linux"
    tgz_path = out_dir / f"informatik-lernreise-kap0-v{version}-linux-x86_64.tar.gz"
    txz_path = out_dir / f"informatik-lernreise-kap0-v{version}-linux-x86_64.tar.xz"

    def write_tar(tf: tarfile.TarFile) -> None:
        for abs_p, rel_p in files:
            payload = normalize_payload(abs_p, rel_p, "linux")
            add_tar_bytes(tf, f"{prefix}/{rel_p.as_posix()}", payload, mode=posix_mode(rel_p))
        for fname, mode in (
            ("install_linux.sh", 0o755),
            ("uninstall_linux.sh", 0o755),
            ("informatik-lernreise-kap0.desktop", 0o644),
        ):
            src = PROJECT_ROOT / "packaging" / "linux" / fname
            if src.is_file():
                payload = normalize_payload(src, Path(fname), "linux")
                add_tar_bytes(tf, f"{prefix}/{fname}", payload, mode=mode)

    with tarfile.open(tgz_path, "w:gz", format=tarfile.PAX_FORMAT) as tf:
        write_tar(tf)

    with tarfile.open(txz_path, "w:xz", format=tarfile.PAX_FORMAT) as tf:
        write_tar(tf)

    return [tgz_path, txz_path]


def _ar_entry(name: str, data: bytes, mtime: int = 1764240000, mode: int = 0o100644) -> bytes:
    header = (
        f"{name:<16}"
        f"{mtime:<12}"
        f"{0:<6}"
        f"{0:<6}"
        f"{oct(mode)[2:]:<8}"
        f"{len(data):<10}"
        "`\n"
    ).encode("ascii")
    if len(header) != 60:
        raise ValueError(f"Ungültige ar-Header-Länge ({len(header)}) für {name}")
    pad = b"\n" if len(data) % 2 == 1 else b""
    return header + data + pad


def build_deb_package(out_dir: Path, version: str, runtime_files: list[tuple[Path, Path]]) -> Path:
    """Erzeugt ein valides Debian/Ubuntu .deb-Paket (ar + control.tar.gz + data.tar.gz)."""
    deb_path = out_dir / f"informatik-lernreise-kap0_{version}_all.deb"

    data_buf = io.BytesIO()
    total_kb = 0
    with gzip.GzipFile(fileobj=data_buf, mode="wb", mtime=1764240000) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tf:
            for d in (
                "./opt",
                "./opt/informatik-lernreise-kap0",
                "./usr",
                "./usr/bin",
                "./usr/share",
                "./usr/share/applications",
                "./usr/share/icons",
                "./usr/share/icons/hicolor",
                "./usr/share/icons/hicolor/scalable",
                "./usr/share/icons/hicolor/scalable/apps",
                "./usr/share/doc",
                "./usr/share/doc/informatik-lernreise-kap0",
            ):
                add_tar_dir(tf, d)

            for abs_p, rel_p in runtime_files:
                payload = normalize_payload(abs_p, rel_p, "linux")
                total_kb += max(1, (len(payload) + 1023) // 1024)
                add_tar_bytes(tf, f"./opt/informatik-lernreise-kap0/{rel_p.as_posix()}", payload, mode=posix_mode(rel_p))

            cli_wrapper = (
                "#!/usr/bin/env bash\n"
                "set -euo pipefail\n"
                'APP_DIR="/opt/informatik-lernreise-kap0"\n'
                'cd "$APP_DIR"\n'
                "for cand in python3 python; do\n"
                '  if command -v "$cand" >/dev/null 2>&1; then\n'
                '    if "$cand" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then\n'
                '      exec "$cand" "$APP_DIR/scripts/serve_local.py" --open-browser "$@"\n'
                "    fi\n"
                "  fi\n"
                "done\n"
                'exec xdg-open "$APP_DIR/index.html"\n'
            ).encode("utf-8")
            add_tar_bytes(tf, "./usr/bin/informatik-lernreise-kap0", cli_wrapper, mode=0o755)

            desktop_p = PROJECT_ROOT / "packaging" / "linux" / "informatik-lernreise-kap0.desktop"
            if desktop_p.is_file():
                add_tar_bytes(
                    tf,
                    "./usr/share/applications/informatik-lernreise-kap0.desktop",
                    normalize_payload(desktop_p, desktop_p, "linux"),
                    mode=0o644,
                )

            icon_p = PROJECT_ROOT / "assets" / "icon.svg"
            if icon_p.is_file():
                add_tar_bytes(
                    tf,
                    "./usr/share/icons/hicolor/scalable/apps/informatik-lernreise-kap0.svg",
                    icon_p.read_bytes(),
                    mode=0o644,
                )

            lic_p = PROJECT_ROOT / "LICENSE"
            if lic_p.is_file():
                add_tar_bytes(
                    tf,
                    "./usr/share/doc/informatik-lernreise-kap0/copyright",
                    lic_p.read_bytes(),
                    mode=0o644,
                )

    data_tar_gz = data_buf.getvalue()

    control_txt = (
        f"Package: informatik-lernreise-kap0\n"
        f"Version: {version}\n"
        f"Section: education\n"
        f"Priority: optional\n"
        f"Architecture: all\n"
        f"Installed-Size: {total_kb}\n"
        f"Recommends: python3 (>= 3.8)\n"
        f"Maintainer: HvH-Hansen <https://github.com/HvH-Hansen/informatik-lernreise-kap0>\n"
        f"Homepage: https://github.com/HvH-Hansen/informatik-lernreise-kap0\n"
        f"Description: Informatik Lernreise Kapitel 0 (Klasse 5/6)\n"
        f" Interaktive Lernreise mit 6 Stationen, A2/B1-Scaffolding,\n"
        f" Offline-Modus und optionaler Google-Sheets-Auswertung.\n"
    ).encode("utf-8")

    conffiles_txt = b"/opt/informatik-lernreise-kap0/config.js\n"

    postinst_sh = (
        "#!/bin/sh\n"
        "set -e\n"
        "if command -v update-desktop-database >/dev/null 2>&1; then\n"
        "  update-desktop-database /usr/share/applications >/dev/null 2>&1 || true\n"
        "fi\n"
        "echo 'Informatik Lernreise Kapitel 0 installiert. Starten mit: informatik-lernreise-kap0'\n"
    ).encode("utf-8")

    prerm_sh = (
        "#!/bin/sh\n"
        "set -e\n"
        "exit 0\n"
    ).encode("utf-8")

    ctrl_buf = io.BytesIO()
    with gzip.GzipFile(fileobj=ctrl_buf, mode="wb", mtime=1764240000) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tf:
            add_tar_bytes(tf, "./control", control_txt, mode=0o644)
            add_tar_bytes(tf, "./conffiles", conffiles_txt, mode=0o644)
            add_tar_bytes(tf, "./postinst", postinst_sh, mode=0o755)
            add_tar_bytes(tf, "./prerm", prerm_sh, mode=0o755)
    control_tar_gz = ctrl_buf.getvalue()

    ar_bytes = (
        b"!<arch>\n"
        + _ar_entry("debian-binary", b"2.0\n")
        + _ar_entry("control.tar.gz", control_tar_gz)
        + _ar_entry("data.tar.gz", data_tar_gz)
    )
    deb_path.write_bytes(ar_bytes)
    return deb_path


def _macos_info_plist(version: str) -> bytes:
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleDevelopmentRegion</key>
  <string>de</string>
  <key>CFBundleDisplayName</key>
  <string>Informatik Lernreise Kap0</string>
  <key>CFBundleExecutable</key>
  <string>Informatik-Lernreise-Kap0</string>
  <key>CFBundleIdentifier</key>
  <string>de.hvh-wuppertal.informatik-lernreise-kap0</string>
  <key>CFBundleInfoDictionaryVersion</key>
  <string>6.0</string>
  <key>CFBundleName</key>
  <string>Informatik Lernreise Kap0</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
  <key>CFBundleShortVersionString</key>
  <string>{version}</string>
  <key>CFBundleVersion</key>
  <string>{version}</string>
  <key>LSMinimumSystemVersion</key>
  <string>12.0</string>
  <key>NSHumanReadableCopyright</key>
  <string>Copyright (c) 2025-2026 HvH-Hansen (MIT License)</string>
  <key>NSHighResolutionCapable</key>
  <true/>
</dict>
</plist>
"""
    return xml.encode("utf-8")


def _macos_launcher_script() -> bytes:
    script = """#!/usr/bin/env bash
set -euo pipefail

CONTENTS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="$CONTENTS_DIR/Resources/app"

cd "$APP_DIR"
for cand in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3 python3 python; do
  if command -v "$cand" >/dev/null 2>&1; then
    if "$cand" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then
      exec "$cand" "$APP_DIR/scripts/serve_local.py" --open-browser "$@"
    fi
  fi
done

exec open "$APP_DIR/index.html"
"""
    return script.encode("utf-8")


def build_macos_packages(
    out_dir: Path,
    version: str,
    runtime_files: list[tuple[Path, Path]],
    stage_app_dir: Path | None = None,
) -> list[Path]:
    """Erstellt macOS .app-Bundle Archive (.tar.gz & .zip) und optional einen entpackten Stage-Ordner."""
    prefix = f"informatik-lernreise-kap0-v{version}-macos"
    app_name = "Informatik Lernreise Kap0.app"
    tgz_path = out_dir / f"informatik-lernreise-kap0-v{version}-macos-universal.tar.gz"
    zip_path = out_dir / f"informatik-lernreise-kap0-v{version}-macos-universal.zip"

    bundle_entries: list[tuple[str, bytes, int]] = [
        (f"{app_name}/Contents/Info.plist", _macos_info_plist(version), 0o644),
        (f"{app_name}/Contents/MacOS/Informatik-Lernreise-Kap0", _macos_launcher_script(), 0o755),
    ]
    icon_p = PROJECT_ROOT / "assets" / "icon.svg"
    if icon_p.is_file():
        bundle_entries.append((f"{app_name}/Contents/Resources/icon.svg", icon_p.read_bytes(), 0o644))

    for abs_p, rel_p in runtime_files:
        payload = normalize_payload(abs_p, rel_p, "macos")
        bundle_entries.append((f"{app_name}/Contents/Resources/app/{rel_p.as_posix()}", payload, posix_mode(rel_p)))

    install_mac_p = PROJECT_ROOT / "packaging" / "macos" / "install_macos.sh"
    install_mac_bytes = normalize_payload(install_mac_p, install_mac_p, "macos") if install_mac_p.is_file() else b""

    with tarfile.open(tgz_path, "w:gz", format=tarfile.PAX_FORMAT) as tf:
        for arc_rel, data, mode in bundle_entries:
            add_tar_bytes(tf, f"{prefix}/{arc_rel}", data, mode=mode)
        if install_mac_bytes:
            add_tar_bytes(tf, f"{prefix}/install_macos.sh", install_mac_bytes, mode=0o755)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for arc_rel, data, mode in bundle_entries:
            add_zip_bytes(zf, f"{prefix}/{arc_rel}", data, mode=mode)
        if install_mac_bytes:
            add_zip_bytes(zf, f"{prefix}/install_macos.sh", install_mac_bytes, mode=0o755)

    if stage_app_dir is not None:
        if stage_app_dir.exists():
            shutil.rmtree(stage_app_dir)
        stage_app_dir.mkdir(parents=True, exist_ok=True)
        for arc_rel, data, mode in bundle_entries:
            dest = stage_app_dir / arc_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            if mode == 0o755 and sys.platform != "win32":
                dest.chmod(0o755)

    return [tgz_path, zip_path]


def write_sha256sums(out_dir: Path, artifacts: list[Path]) -> Path:
    sums_path = out_dir / "SHA256SUMS.txt"
    lines: list[str] = []
    for p in sorted(artifacts, key=lambda x: x.name):
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{digest}  {p.name}")
    sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return sums_path


def _check_config_neutral(name: str, data: bytes, errors: list[str], pkg_name: str) -> None:
    if name.endswith("/config.js") or name == "config.js":
        txt = data.decode("utf-8", errors="replace")
        if "script.google.com/macros/s/" in txt or "AKfycb" in txt:
            errors.append(f"DSGVO-Verstoß in {pkg_name}: {name} enthält eine persönliche Google-Apps-Script-URL!")


def verify_artifacts(out_dir: Path, artifacts: list[Path], sums_path: Path) -> list[str]:
    errors: list[str] = []
    expected_hashes: dict[str, str] = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, fname = line.split("  ", 1)
        expected_hashes[fname.strip()] = digest.strip()

    for p in artifacts:
        if not p.is_file() or p.stat().st_size == 0:
            errors.append(f"Datei fehlt oder leer: {p.name}")
            continue
        actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
        if expected_hashes.get(p.name) != actual_hash:
            errors.append(f"SHA256 stimmt nicht für {p.name}")

        if p.name.endswith(".zip"):
            try:
                with zipfile.ZipFile(p, "r") as zf:
                    bad = zf.testzip()
                    if bad is not None:
                        errors.append(f"Defekter ZIP-Eintrag {bad} in {p.name}")
                    for n in zf.namelist():
                        if any(x in n for x in ("Schuelerdaten/", ".env")) or n.endswith((".csv", ".xlsx")):
                            errors.append(f"DSGVO-Verstoß in {p.name}: unzulässige Datei {n}")
                        if n.endswith("/config.js") or n == "config.js":
                            _check_config_neutral(n, zf.read(n), errors, p.name)
            except Exception as exc:
                errors.append(f"ZIP ungültig ({p.name}): {exc}")

        elif p.name.endswith((".tar.gz", ".tar.xz")):
            try:
                mode = "r:gz" if p.name.endswith(".tar.gz") else "r:xz"
                with tarfile.open(p, mode) as tf:
                    members = tf.getmembers()
                    if not members:
                        errors.append(f"Leeres Tar-Archiv: {p.name}")
                    for m in members:
                        if any(x in m.name for x in ("Schuelerdaten/", ".env")) or m.name.endswith((".csv", ".xlsx")):
                            errors.append(f"DSGVO-Verstoß in {p.name}: unzulässige Datei {m.name}")
                        if m.isfile() and (m.name.endswith("/config.js") or m.name == "config.js"):
                            f = tf.extractfile(m)
                            if f is not None:
                                _check_config_neutral(m.name, f.read(), errors, p.name)
            except Exception as exc:
                errors.append(f"Tar-Archiv ungültig ({p.name}): {exc}")

        elif p.name.endswith(".deb"):
            raw = p.read_bytes()
            if not raw.startswith(b"!<arch>\ndebian-binary"):
                errors.append(f"Ungültiger ar-Header in {p.name}")
            elif b"control.tar.gz" not in raw or b"data.tar.gz" not in raw:
                errors.append(f"Fehlende control/data.tar.gz in {p.name}")
            elif b"AKfycb" in raw or b"script.google.com/macros/s/" in raw:
                errors.append(f"DSGVO-Verstoß in {p.name}: persönliche Apps-Script-URL enthalten!")

    return errors


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Informatik Lernreise Cross-OS Paket- & Archiv-Builder")
    parser.add_argument("--output-dir", default="", help="Ausgabeordner (Standard: dist/v<VERSION>)")
    parser.add_argument("--clean", action="store_true", help="Zielordner vor dem Bau leeren")
    parser.add_argument("--verify", action="store_true", help="Alle gebauten Archive & Pakete sofort validieren")
    parser.add_argument("--macos-stage-dir", default="", help="Optionaler Entpack-Pfad für .app-Bundle (macOS CI)")
    parser.add_argument("--json", action="store_true", help="Maschinenlesbare JSON-Ausgabe")
    args = parser.parse_args()

    version = read_version()
    out_dir = Path(args.output_dir) if args.output_dir else (DIST_ROOT / f"v{version}")
    if args.clean and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_files = collect_project_files(include_dev_meta=True)
    runtime_files = collect_project_files(include_dev_meta=False)

    built: list[Path] = []
    built.extend(build_source_archives(out_dir, version, all_files))
    built.append(build_windows_package(out_dir, version, all_files))
    built.extend(build_linux_archives(out_dir, version, all_files))
    built.append(build_deb_package(out_dir, version, runtime_files))
    stage_dir = Path(args.macos_stage_dir) if args.macos_stage_dir else None
    built.extend(build_macos_packages(out_dir, version, runtime_files, stage_app_dir=stage_dir))

    sums_path = write_sha256sums(out_dir, built)

    errors: list[str] = []
    if args.verify:
        errors = verify_artifacts(out_dir, built, sums_path)

    if args.json:
        print(
            json.dumps(
                {
                    "version": version,
                    "output_dir": str(out_dir),
                    "artifacts": [{"name": p.name, "bytes": p.stat().st_size} for p in [*built, sums_path]],
                    "verified": args.verify,
                    "errors": errors,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"=== Informatik Lernreise Paket-Builder v{version} ===")
        print(f"Zielordner: {out_dir}")
        for p in [*built, sums_path]:
            size_kb = p.stat().st_size / 1024.0
            print(f"  [OK] {p.name:<56s} ({size_kb:8.1f} KB)")
        if args.verify:
            if errors:
                for err in errors:
                    print(f"  [FAIL] {err}", file=sys.stderr)
            else:
                print(f"[PASS] Alle {len(built)} Pakete/Archive erfolgreich verifiziert (DSGVO-frei & neutral konfiguriert).")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()

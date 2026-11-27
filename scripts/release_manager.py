#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/release_manager.py
==========================
Automatische SemVer-Versionsverwaltung (0.y.z), Changelog-Fortschreibung
(`CHANGELOG.md`) und Git-Hook-Integration für die Informatik Lernreise Kapitel 0.

Copyright (c) 2025-2026 HvH-Hansen (MIT License)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = PROJECT_ROOT / "VERSION"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"
HOOKS_DIR = PROJECT_ROOT / ".githooks"

AUTO_START_MARKER = "<!-- AUTO-CHANGELOG:START -->"
AUTO_END_MARKER = "<!-- AUTO-CHANGELOG:END -->"

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
CONVENTIONAL_RE = re.compile(r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s*(?P<desc>.+)$")

CATEGORY_MAP: dict[str, str] = {
    "feat": "Hinzugefügt",
    "feature": "Hinzugefügt",
    "add": "Hinzugefügt",
    "fix": "Behoben",
    "bugfix": "Behoben",
    "security": "Sicherheit",
    "sec": "Sicherheit",
    "perf": "Geändert",
    "refactor": "Geändert",
    "style": "Geändert",
    "ui": "Geändert",
    "docs": "Dokumentation",
    "doc": "Dokumentation",
    "build": "Wartung & Pakete",
    "ci": "Wartung & Pakete",
    "chore": "Wartung & Pakete",
    "test": "Wartung & Pakete",
}


def read_version() -> str:
    if not VERSION_FILE.exists():
        return "0.3.0"
    raw = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not SEMVER_RE.match(raw):
        raise ValueError(f"Ungültige SemVer-Version in VERSION: {raw!r}")
    return raw


def parse_semver(version: str) -> tuple[int, int, int]:
    m = SEMVER_RE.match(version.strip())
    if not m:
        raise ValueError(f"Ungültige Version: {version!r}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def bump_semver(current: str, level: str) -> str:
    major, minor, patch = parse_semver(current)
    if level == "major":
        if major == 0:
            return f"0.{minor + 1}.0"
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"Unbekanntes Bump-Level: {level}")


def classify_commit(subject: str, body: str = "") -> tuple[str, str, str]:
    """Bestimmt (bump_level, changelog_section, formatted_bullet) aus einer Commit-Message."""
    subj = subject.strip()
    full = f"{subj}\n{body}".strip()
    is_breaking = "BREAKING CHANGE" in full or bool(re.search(r"^[a-zA-Z]+(\([^)]+\))?!:", subj))

    m = CONVENTIONAL_RE.match(subj)
    if m:
        ctype = m.group("type").lower()
        scope = m.group("scope")
        desc = m.group("desc").strip()
        section = CATEGORY_MAP.get(ctype, "Geändert")
        prefix = f"**{ctype}({scope}):**" if scope else f"**{ctype}:**"
        bullet = f"{prefix} {desc}"
        if is_breaking:
            return "major", section, f"**BREAKING** {bullet}"
        if ctype in ("feat", "feature", "add"):
            return "minor", section, bullet
        return "patch", section, bullet

    lower = subj.lower()
    if is_breaking:
        return "major", "Geändert", f"**BREAKING:** {subj}"
    if lower.startswith(("add ", "hinzufügen", "neue ", "neues ", "neuer ")):
        return "minor", "Hinzugefügt", subj
    if lower.startswith(("fix ", "beheb", "korrigier")):
        return "patch", "Behoben", subj
    return "patch", "Geändert", subj


def should_skip_bump(subject: str, body: str = "") -> bool:
    combined = f"{subject}\n{body}"
    if re.match(r"^chore\(release\):", subject.strip(), re.I):
        return True
    if "[skip bump]" in combined.lower() or "[no bump]" in combined.lower():
        return True
    if subject.strip().startswith("Merge "):
        return True
    return False


def _replace_pattern(path: Path, pattern: str, replacement: str) -> bool:
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, original, count=1, flags=re.MULTILINE)
    if count > 0 and updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def _minor_series(version: str) -> str:
    major, minor, _ = parse_semver(version)
    return f"{major}.{minor}.x"


def sync_version_files(version: str) -> list[str]:
    """Synchronisiert die Versionsnummer in allen Projekt-, Starter- und Packaging-Dateien."""
    touched: list[str] = []

    current_vf = VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else ""
    if current_vf != version:
        VERSION_FILE.write_text(f"{version}\n", encoding="utf-8")
        touched.append("VERSION")

    series = _minor_series(version)
    replacements: list[tuple[Path, str, str]] = [
        (
            PROJECT_ROOT / "README.md",
            r"(badge/Version-v)[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9_]+)",
            rf"\g<1>{version}\g<2>",
        ),
        (
            PROJECT_ROOT / "SECURITY.md",
            r"^(\|\s*`)[0-9]+\.[0-9]+\.x(`\s*\(aktuell\)\s*\|)",
            rf"\g<1>{series}\g<2>",
        ),
        (
            PROJECT_ROOT / "scripts" / "serve_local.py",
            r'^(APP_VERSION\s*=\s*)"[^"]+"',
            rf'\g<1>"{version}"',
        ),
        (
            PROJECT_ROOT / "packaging" / "linux" / "informatik-lernreise-kap0.spec",
            r"^(Version:\s+)\S+",
            rf"\g<1>{version}",
        ),
        (
            PROJECT_ROOT / "packaging" / "linux" / "PKGBUILD",
            r"^(pkgver=)\S+",
            rf"\g<1>{version}",
        ),
        (
            PROJECT_ROOT / "packaging" / "windows" / "installer.iss",
            r'^(#define MyAppVersion\s+)"[^"]+"',
            rf'\g<1>"{version}"',
        ),
    ]

    for target, pat, repl in replacements:
        if _replace_pattern(target, pat, repl):
            touched.append(target.relative_to(PROJECT_ROOT).as_posix())

    return touched


def check_version_sync(version: str) -> dict[str, Any]:
    """Prüft ohne Schreibzugriff, ob alle Version-Träger synchron sind."""
    series = _minor_series(version)
    checks: list[tuple[Path, str, str]] = [
        (PROJECT_ROOT / "README.md", r"badge/Version-v([0-9]+\.[0-9]+\.[0-9]+)-[a-zA-Z0-9_]+", version),
        (PROJECT_ROOT / "SECURITY.md", r"^\|\s*`([0-9]+\.[0-9]+\.x)`\s*\(aktuell\)\s*\|", series),
        (PROJECT_ROOT / "scripts" / "serve_local.py", r'^APP_VERSION\s*=\s*"([^"]+)"', version),
        (PROJECT_ROOT / "packaging" / "linux" / "informatik-lernreise-kap0.spec", r"^Version:\s+(\S+)", version),
        (PROJECT_ROOT / "packaging" / "linux" / "PKGBUILD", r"^pkgver=(\S+)", version),
        (PROJECT_ROOT / "packaging" / "windows" / "installer.iss", r'^#define MyAppVersion\s+"([^"]+)"', version),
    ]
    out_of_sync: list[dict[str, str]] = []
    synced: list[str] = []
    for path, pat, expected in checks:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        m = re.search(pat, text, flags=re.MULTILINE)
        found = m.group(1) if m else "FEHLT"
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        if found != expected:
            out_of_sync.append({"file": rel, "found": found, "expected": expected})
        else:
            synced.append(rel)
    return {"version": version, "synced": synced, "out_of_sync": out_of_sync}


def build_changelog_entry(
    version: str,
    date_str: str,
    section: str,
    bullet: str,
    commit_hash: str | None = None,
) -> str:
    hash_suffix = f" (`{commit_hash[:7]}`)" if commit_hash else ""
    lines = [
        f"## [{version}] - {date_str}{hash_suffix}",
        "",
        f"### {section}",
        f"- {bullet}",
    ]
    return "\n".join(lines)


def prepend_changelog_entries(entries: list[str]) -> None:
    if not entries:
        return
    if not CHANGELOG_FILE.exists():
        content = (
            "# Changelog\n\n"
            f"{AUTO_START_MARKER}\n"
            f"{AUTO_END_MARKER}\n"
        )
    else:
        content = CHANGELOG_FILE.read_text(encoding="utf-8")

    block = "\n\n".join(entries)
    if AUTO_START_MARKER in content:
        before, after = content.split(AUTO_START_MARKER, 1)
        after_stripped = after.lstrip("\r\n")
        new_content = f"{before}{AUTO_START_MARKER}\n{block}\n\n{after_stripped}"
    else:
        new_content = f"{content.rstrip()}\n\n{block}\n"

    CHANGELOG_FILE.write_text(new_content, encoding="utf-8")


def extract_release_notes(version: str) -> str:
    if not CHANGELOG_FILE.exists():
        return f"Release v{version}"
    content = CHANGELOG_FILE.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|{re.escape(AUTO_END_MARKER)}|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(content)
    if not m:
        return f"Release v{version}"
    notes = m.group(1).strip()
    return notes or f"Release v{version}"


def _run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(PROJECT_ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=check,
    )


def get_unreleased_commits() -> list[dict[str, str]]:
    """Findet Commits auf HEAD seit dem jüngsten Release-Anker (Tag `v*`, `VERSION`-Commit oder Changelog-Hash)."""
    if not (PROJECT_ROOT / ".git").exists():
        return []

    candidates: list[str] = []

    tag_res = _run_git(["describe", "--tags", "--match", "v*", "--abbrev=0"], check=False)
    if tag_res.returncode == 0 and tag_res.stdout.strip():
        candidates.append(tag_res.stdout.strip())

    ver_res = _run_git(["log", "-n", "1", "--format=%H", "--", "VERSION"], check=False)
    if ver_res.returncode == 0 and ver_res.stdout.strip():
        candidates.append(ver_res.stdout.strip())

    if CHANGELOG_FILE.exists():
        ch_text = CHANGELOG_FILE.read_text(encoding="utf-8")
        m = re.search(r"^## \[[^\]]+\] - \d{4}-\d{2}-\d{2} \(`([0-9a-f]{7,40})`\)", ch_text, re.MULTILINE)
        if m:
            candidate = m.group(1)
            verify = _run_git(["cat-file", "-e", f"{candidate}^{{commit}}"], check=False)
            if verify.returncode == 0:
                candidates.append(candidate)

    since_ref: str | None = None
    best_dist: int | None = None
    for ref in candidates:
        cnt_res = _run_git(["rev-list", "--count", f"{ref}..HEAD"], check=False)
        if cnt_res.returncode == 0:
            try:
                dist = int(cnt_res.stdout.strip())
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    since_ref = ref
            except ValueError:
                pass

    rev_range = f"{since_ref}..HEAD" if since_ref else "HEAD"
    fmt = "%H%x1f%ad%x1f%s%x1f%b%x1e"
    log_res = _run_git(["log", "--reverse", "--date=short", f"--pretty=format:{fmt}", rev_range], check=False)
    if log_res.returncode != 0 or not log_res.stdout.strip():
        return []

    commits: list[dict[str, str]] = []
    for raw_rec in log_res.stdout.split("\x1e"):
        rec = raw_rec.strip()
        if not rec:
            continue
        parts = rec.split("\x1f")
        if len(parts) < 3:
            continue
        sha, date_str, subject = parts[0].strip(), parts[1].strip(), parts[2].strip()
        body = parts[3].strip() if len(parts) > 3 else ""
        if should_skip_bump(subject, body):
            continue
        files_res = _run_git(["diff-tree", "--no-commit-id", "--name-only", "-r", sha], check=False)
        changed_files = set(files_res.stdout.splitlines()) if files_res.returncode == 0 else set()
        if "VERSION" in changed_files:
            continue
        commits.append({"sha": sha, "date": date_str, "subject": subject, "body": body})
    return commits


def is_version_staged() -> bool:
    if not (PROJECT_ROOT / ".git").exists():
        return False
    res = _run_git(["diff", "--cached", "--name-only"], check=False)
    if res.returncode != 0:
        return False
    return "VERSION" in set(res.stdout.splitlines())


def install_hooks() -> dict[str, Any]:
    if not HOOKS_DIR.exists():
        raise FileNotFoundError(f"Hook-Verzeichnis fehlt: {HOOKS_DIR}")
    _run_git(["config", "core.hooksPath", ".githooks"])
    if sys.platform != "win32":
        for hook_file in HOOKS_DIR.iterdir():
            if hook_file.is_file():
                hook_file.chmod(hook_file.stat().st_mode | 0o111)
    res = _run_git(["config", "--get", "core.hooksPath"], check=False)
    return {"hooks_path": res.stdout.strip(), "installed": res.stdout.strip() == ".githooks"}


def action_status() -> dict[str, Any]:
    ver = read_version()
    sync_info = check_version_sync(ver)
    hooks_cfg = ""
    if (PROJECT_ROOT / ".git").exists():
        r = _run_git(["config", "--get", "core.hooksPath"], check=False)
        hooks_cfg = r.stdout.strip()
    pending = get_unreleased_commits()
    return {
        "version": ver,
        "sync": sync_info,
        "hooks_path": hooks_cfg or "(Standard .git/hooks)",
        "hooks_active": hooks_cfg == ".githooks",
        "unbumped_commits": [{"sha": c["sha"][:7], "subject": c["subject"]} for c in pending],
    }


def _pending_marker_path() -> Path | None:
    if not (PROJECT_ROOT / ".git").exists():
        return None
    res = _run_git(["rev-parse", "--git-path", "HVH_BUMP_PENDING"], check=False)
    if res.returncode == 0 and res.stdout.strip():
        p = Path(res.stdout.strip())
        return p if p.is_absolute() else (PROJECT_ROOT / p)
    return PROJECT_ROOT / ".git" / "HVH_BUMP_PENDING"


def action_bump_message(subject: str, body: str = "", level_override: str = "auto", stage: bool = False) -> dict[str, Any]:
    if should_skip_bump(subject, body):
        return {"skipped": True, "reason": "Release-/Merge-Commit oder [skip bump]", "version": read_version()}
    if stage and is_version_staged():
        ver = read_version()
        touched = sync_version_files(ver)
        if touched and (PROJECT_ROOT / ".git").exists():
            _run_git(["add", *touched], check=False)
            marker = _pending_marker_path()
            if marker is not None:
                marker.write_text(ver, encoding="utf-8")
        return {"skipped": True, "reason": "VERSION bereits im Commit gestaged", "version": ver, "synced": touched}

    old_ver = read_version()
    cur_ver = old_ver
    entries_newest_first: list[str] = []

    if (PROJECT_ROOT / ".git").exists():
        for c in get_unreleased_commits():
            c_lvl, c_sec, c_bul = classify_commit(c["subject"], c["body"])
            cur_ver = bump_semver(cur_ver, c_lvl)
            c_entry = build_changelog_entry(
                cur_ver,
                c["date"] or dt.date.today().isoformat(),
                c_sec,
                c_bul,
                commit_hash=c["sha"],
            )
            entries_newest_first.insert(0, c_entry)

    auto_level, section, bullet = classify_commit(subject, body)
    level = auto_level if level_override == "auto" else level_override
    new_ver = bump_semver(cur_ver, level)
    today = dt.date.today().isoformat()
    entry = build_changelog_entry(new_ver, today, section, bullet)
    entries_newest_first.insert(0, entry)

    prepend_changelog_entries(entries_newest_first)
    touched = sync_version_files(new_ver)
    files_to_stage = list(dict.fromkeys(["VERSION", "CHANGELOG.md", *touched]))

    if stage and (PROJECT_ROOT / ".git").exists():
        existing = [f for f in files_to_stage if (PROJECT_ROOT / f).exists()]
        if existing:
            _run_git(["add", *existing], check=True)
            marker = _pending_marker_path()
            if marker is not None:
                marker.write_text(new_ver, encoding="utf-8")

    return {
        "skipped": False,
        "old_version": old_ver,
        "version": new_ver,
        "level": level,
        "section": section,
        "staged": stage,
        "files_updated": files_to_stage,
    }


def action_bump_from_git() -> dict[str, Any]:
    commits = get_unreleased_commits()
    old_ver = read_version()
    if not commits:
        touched = sync_version_files(old_ver)
        return {
            "bumped": False,
            "old_version": old_ver,
            "version": old_ver,
            "commits_processed": 0,
            "files_updated": touched,
        }

    cur_ver = old_ver
    entries_newest_first: list[str] = []
    processed: list[dict[str, str]] = []
    for c in commits:
        level, section, bullet = classify_commit(c["subject"], c["body"])
        cur_ver = bump_semver(cur_ver, level)
        entry = build_changelog_entry(cur_ver, c["date"] or dt.date.today().isoformat(), section, bullet, commit_hash=c["sha"])
        entries_newest_first.insert(0, entry)
        processed.append({"sha": c["sha"][:7], "version": cur_ver, "subject": c["subject"]})

    prepend_changelog_entries(entries_newest_first)
    touched = sync_version_files(cur_ver)
    return {
        "bumped": True,
        "old_version": old_ver,
        "version": cur_ver,
        "commits_processed": len(processed),
        "commits": processed,
        "files_updated": list(dict.fromkeys(["VERSION", "CHANGELOG.md", *touched])),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Informatik Lernreise Release-, Versions- & Changelog-Manager")
    parser.add_argument(
        "--action",
        choices=["status", "sync", "bump", "release-notes", "install-hooks"],
        default="status",
        help="Auszuführende Aktion",
    )
    parser.add_argument("--message", default="", help="Commit-Nachricht für manuellen Bump")
    parser.add_argument("--message-file", default="", help="Pfad zur Commit-Msg-Datei (für .githooks/commit-msg)")
    parser.add_argument("--from-git", action="store_true", help="Alle noch nicht vermerkten Git-Commits einzeln hochzählen")
    parser.add_argument("--level", choices=["auto", "patch", "minor", "major"], default="auto", help="Bump-Stufe")
    parser.add_argument("--stage", action="store_true", help="Aktualisierte Dateien per `git add` vormerken")
    parser.add_argument("--version", default="", help="Zielversion für --action release-notes")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    args = parser.parse_args()

    if args.action == "status":
        res = action_status()
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"Aktuelle Version: v{res['version']}")
            print(f"Git-Hooks (.githooks): {'AKTIV' if res['hooks_active'] else 'NICHT AKTIV'} ({res['hooks_path']})")
            print(f"Synchronisierte Dateien ({len(res['sync']['synced'])}): {', '.join(res['sync']['synced'])}")
            if res["sync"]["out_of_sync"]:
                print(f"[WARN] Nicht synchron: {res['sync']['out_of_sync']}")
            if res["unbumped_commits"]:
                print(f"Offene Commits ohne Versions-Bump ({len(res['unbumped_commits'])}):")
                for c in res["unbumped_commits"]:
                    print(f"  - {c['sha']}: {c['subject']}")
            else:
                print("Alle Commits sind in VERSION / CHANGELOG.md berücksichtigt.")
        return

    if args.action == "sync":
        ver = read_version()
        touched = sync_version_files(ver)
        res = {"version": ver, "updated": touched}
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else f"[OK] Version v{ver} synchronisiert ({len(touched)} Datei(en) aktualisiert).")
        return

    if args.action == "install-hooks":
        res = install_hooks()
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else f"[OK] Git-Hooks aktiviert: core.hooksPath={res['hooks_path']}")
        return

    if args.action == "release-notes":
        ver = args.version.strip() or read_version()
        print(extract_release_notes(ver))
        return

    if args.action == "bump":
        if args.from_git:
            res = action_bump_from_git()
        elif args.message_file:
            raw_msg = Path(args.message_file).read_text(encoding="utf-8", errors="replace")
            clean_lines = [ln for ln in raw_msg.splitlines() if not ln.startswith("#")]
            subject = clean_lines[0].strip() if clean_lines else ""
            body = "\n".join(clean_lines[1:]).strip()
            if not subject:
                res = {"skipped": True, "reason": "Leere Commit-Nachricht", "version": read_version()}
            else:
                res = action_bump_message(subject, body, level_override=args.level, stage=args.stage)
        elif args.message:
            lines = args.message.splitlines()
            res = action_bump_message(lines[0], "\n".join(lines[1:]), level_override=args.level, stage=args.stage)
        else:
            parser.error("--action bump benötigt --message, --message-file oder --from-git.")
            return

        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif res.get("skipped"):
            print(f"[SKIP] {res.get('reason')} (v{res.get('version')})")
        elif "commits_processed" in res:
            if res["bumped"]:
                print(f"[OK] {res['commits_processed']} Commit(s) verbucht: v{res['old_version']} -> v{res['version']}")
            else:
                print(f"[OK] Keine offenen Commits (aktuell v{res['version']}).")
        else:
            print(f"[OK] Version erhöht: v{res['old_version']} -> v{res['version']} ({res['section']})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Automatisierte Tests für Versionierung, lokalen Starter und DSGVO-neutrale Pakete."""

from __future__ import annotations

import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import build_packages  # noqa: E402
import release_manager  # noqa: E402


class TestReleaseAndPackages(unittest.TestCase):
    def test_semver_bump_and_commit_classification(self) -> None:
        self.assertEqual(release_manager.bump_semver("0.3.0", "patch"), "0.3.1")
        self.assertEqual(release_manager.bump_semver("0.3.9", "minor"), "0.4.0")
        self.assertEqual(release_manager.bump_semver("0.4.0", "major"), "0.5.0")

        lvl, sec, _ = release_manager.classify_commit("feat(station-04): Neue Aufgabe")
        self.assertEqual((lvl, sec), ("minor", "Hinzugefügt"))

        lvl_fix, sec_fix, _ = release_manager.classify_commit("fix(cloud): Merge korrigiert")
        self.assertEqual((lvl_fix, sec_fix), ("patch", "Behoben"))

    def test_version_sync_across_repo(self) -> None:
        ver = release_manager.read_version()
        sync_res = release_manager.check_version_sync(ver)
        self.assertEqual(sync_res["out_of_sync"], [], f"Version nicht synchron: {sync_res['out_of_sync']}")
        self.assertGreaterEqual(len(sync_res["synced"]), 6)

    def test_serve_local_selftest(self) -> None:
        res = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "serve_local.py"), "--selftest"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(res.returncode, 0, msg=res.stdout + res.stderr)
        self.assertIn("[PASS]", res.stdout)

    def test_build_packages_neutral_config_and_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "out"
            res = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT_ROOT / "scripts" / "build_packages.py"),
                    "--output-dir",
                    str(out_dir),
                    "--verify",
                ],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(res.returncode, 0, msg=res.stdout + res.stderr)

            ver = build_packages.read_version()
            win_zip = out_dir / f"informatik-lernreise-kap0-v{ver}-windows-x64.zip"
            lin_tgz = out_dir / f"informatik-lernreise-kap0-v{ver}-linux-x86_64.tar.gz"
            deb_pkg = out_dir / f"informatik-lernreise-kap0_{ver}_all.deb"

            self.assertTrue(win_zip.is_file())
            self.assertTrue(lin_tgz.is_file())
            self.assertTrue(deb_pkg.is_file())

            with zipfile.ZipFile(win_zip, "r") as zf:
                cfg_entries = [n for n in zf.namelist() if n.endswith("/config.js")]
                self.assertEqual(len(cfg_entries), 1)
                cfg_txt = zf.read(cfg_entries[0]).decode("utf-8")
                self.assertIn("endpointUrl: ''", cfg_txt)
                self.assertNotIn("script.google.com/macros/s/", cfg_txt)

            with tarfile.open(lin_tgz, "r:gz") as tf:
                cfg_members = [m for m in tf.getmembers() if m.name.endswith("/config.js")]
                self.assertEqual(len(cfg_members), 1)
                cfg_txt = tf.extractfile(cfg_members[0]).read().decode("utf-8")  # type: ignore[union-attr]
                self.assertIn("endpointUrl: ''", cfg_txt)
                self.assertNotIn("script.google.com/macros/s/", cfg_txt)


if __name__ == "__main__":
    unittest.main()

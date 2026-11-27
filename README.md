# Mediatown – Informatik Lernreise Kapitel 0 (Klasse 5/6)

[![Version](https://img.shields.io/badge/Version-v0.4.0-3730a3)](CHANGELOG.md)
[![Lizenz](https://img.shields.io/badge/Lizenz-MIT-16a34a)](LICENSE)
[![Plattformen](https://img.shields.io/badge/Plattformen-Web%20%7C%20Windows%20%7C%20Linux%20%7C%20macOS-0284c7)](https://github.com/HvH-Hansen/informatik-lernreise-kap0/releases)
[![GitHub Pages](https://img.shields.io/badge/Live-GitHub%20Pages-0284c7)](https://hvh-hansen.github.io/informatik-lernreise-kap0/)
[![Google Sheets](https://img.shields.io/badge/Auswertung-Google%20Sheets-0f9d58)](ANLEITUNG_Kollegium_Einrichtung.md)

Interaktive, browserbasierte Lernreise für den Informatik-Unterricht in **Klasse 5/6** an der Hermann-von-Helmholtz-Realschule Wuppertal (HvH). Sie kombiniert **6 eigenständige Lernstationen** mit sprachsensiblem **A2/B1-Scaffolding**, wertschätzendem **3-Teile-Feedback**, Stempel- und Sternesystem sowie **Cloud-Spielstand & zentraler Auswertung** über Google Sheets (optional auch offline/lokal per Installationspaket).

---

## Zentrale Links

| Ressource | Zweck | Link |
|---|---|---|
| **Live-Lernreise (SuS)** | Direkter Start der HvH-Instanz auf GitHub Pages | [hvh-hansen.github.io/informatik-lernreise-kap0](https://hvh-hansen.github.io/informatik-lernreise-kap0/) |
| **Kollegiums-Anleitung** | Eigene GitHub Pages + Google Sheets (ohne JSON) + lokale Installation | [ANLEITUNG_Kollegium_Einrichtung.md](ANLEITUNG_Kollegium_Einrichtung.md) |
| **Apps-Script-Kurzreferenz** | Technische Einrichtung & Update von `Code.gs` | [ANLEITUNG_Google_Sheets_Anbindung.md](ANLEITUNG_Google_Sheets_Anbindung.md) |
| **Installationspakete** | Fertige Pakete für Windows, macOS, Linux & Quellarchive | [GitHub Releases](https://github.com/HvH-Hansen/informatik-lernreise-kap0/releases) |

> [!IMPORTANT]
> **Datenschutz (DSGVO / § 48 SchulG NRW):** Dieses Repository enthält ausschließlich den Quellcode und die statischen Lerninhalte. Die Anmeldung in der Lernreise erfolgt datensparsam über `Klasse | Vorname | Initial` (1. Buchstabe des Nachnamens). Es dürfen **keine** Klassenlisten, CSV-/Excel-Exporte oder `.env`-Dateien in das Repository eingecheckt werden. Alle Installationspakete werden mit einer **neutralen `config.js`** (aus [`config.example.js`](config.example.js), `endpointUrl: ''`) ausgeliefert. Bitte achte als Lehrkraft darauf, dass deine verknüpfte Google-Sheets-Tabelle ausschließlich für berechtigte Lehrkräfte freigegeben ist (kein öffentlicher Lesezugriff).

---

## Für Kolleginnen & Kollegen: Eigene Instanz & Installation

### Option A: Eigene GitHub Pages + Google Sheets (empfohlen für eigene Klassen)
Jede Lehrkraft kann das Repository kostenlos forken, über **GitHub Pages** unter eigener Schul-/Klassen-URL bereitstellen und eine eigene **Google-Tabelle** verknüpfen – alle Spielstände und Auswertungen erscheinen direkt in `Übersicht` und `Spielstaende`, **ohne JSON-Dateien auszuwerten**.  
👉 Vollständige Schritt-für-Schritt-Anleitung: [**ANLEITUNG_Kollegium_Einrichtung.md**](ANLEITUNG_Kollegium_Einrichtung.md)

### Option B: Fertige Release-Pakete für den eigenen Rechner (Windows, Linux, macOS)
Unter [**GitHub Releases**](https://github.com/HvH-Hansen/informatik-lernreise-kap0/releases) stehen für jeden Release fertige Installationspakete inkl. `SHA256SUMS.txt` bereit:

| Plattform / Dateisystem | Paketformate | Installation & Start |
|---|---|---|
| **Windows** (NTFS / exFAT) | `*-windows-setup.exe`, `*-windows-x64.zip` | `.exe`-Installer starten oder `.zip` entpacken & `Start_Lernreise.bat` / `install_windows.ps1` ausführen |
| **Linux (Debian / Ubuntu)** | `*_all.deb` | `sudo apt install ./informatik-lernreise-kap0_<version>_all.deb` (Start mit `informatik-lernreise-kap0`) |
| **Linux (Universal / Fedora / Arch)** | `*-linux-x86_64.tar.gz`, `*-linux-x86_64.tar.xz`, `.spec`, `PKGBUILD` | Archiv entpacken & `./install_linux.sh` ausführen |
| **macOS** (APFS / HFS+) | `*-macos-apfs.dmg`, `*-macos.pkg`, `*-macos-universal.tar.gz` / `.zip` | `.dmg`/`.pkg` öffnen bzw. `Informatik Lernreise Kap0.app` nach `/Applications` kopieren |
| **Reine Quellarchive** | `*-source.tar.gz`, `*-source.zip` | Entpacken & `Start_Lernreise.bat` / `Start_Lernreise.command` bzw. `index.html` öffnen |

### Option C: Direkt aus dem Git-Repository (für gemeinsame Weiterentwicklung)
1. Repository klonen:
   ```bash
   git clone https://github.com/HvH-Hansen/informatik-lernreise-kap0.git
   cd informatik-lernreise-kap0
   ```
2. Lokale Git-Hooks (DSGVO-Schutz & automatische Versionierung) aktivieren:
   ```powershell
   # Windows
   py -3 scripts/release_manager.py --action install-hooks
   # macOS / Linux
   python3 scripts/release_manager.py --action install-hooks
   ```
3. Lokal starten oder prüfen (nur Python-Standardbibliothek nötig):
   ```powershell
   py -3 scripts/serve_local.py --open-browser
   py -3 scripts/serve_local.py --selftest
   ```

---

## Aufbau der Lernreise (6 Stationen)

| Station | Thema |
|---|---|
| **0.1** | Fachbegriffe |
| **0.2** | Maus & Tastatur |
| **0.3** | Arbeiten am PC |
| **0.4** | Textverarbeitung |
| **0.5** | Infos im Internet |
| **0.6** | Präsentation |

- **Motivation & Differenzierung:** Pro Station gibt es Pflichtaufgaben, Zusatzaufgaben, Stempel, bis zu 3 Sterne, Sammel-Abzeichen sowie ein sprachsensibles A2/B1-Scaffolding mit 3-Teile-Feedback.
- **Cloud-Spielstand & Gerätewechsel:** Zwischenstände werden über `Klasse|Vorname|Initial` im Tabellenblatt **`Spielstaende`** gesichert und beim erneuten Anmelden an einem anderen Schul-PC automatisch zusammengeführt und wiederhergestellt (`google_apps_script/Code.gs`).
- **Zentrale Übersicht:** Alle erledigten Stationen, Stempel, Sterne und Abzeichen laufen gebündelt im Tabellenblatt **`Übersicht`** zusammen.

---

## Repository-Struktur

| Datei / Ordner | Funktion |
|---|---|
| [`index.html`](index.html) | Vollständige Lernreise (Hub + eingebettete Lernpfade `0.1–0.6`, GSAP/Lottie-UI) |
| [`config.js`](config.js) | Endpunkt-Konfiguration (`window.PC00_CONFIG`) für die GitHub-Pages-Instanz |
| [`config.example.js`](config.example.js) | Neutrale Vorlage für Forks und alle Installationspakete (`endpointUrl: ''`) |
| [`google_apps_script/Code.gs`](google_apps_script/Code.gs) | Google-Apps-Script-Backend (`doGet` / `doPost`) für `Übersicht` & `Spielstaende` |
| [`Start_Lernreise.bat`](Start_Lernreise.bat) / [`Start_Lernreise.command`](Start_Lernreise.command) | 1-Klick-Starter für Windows, macOS & Linux |
| [`scripts/serve_local.py`](scripts/serve_local.py) | Lokaler HTTP-Starter (`127.0.0.1`) mit `no-store`-Header für `config.js` & `--selftest` |
| [`scripts/release_manager.py`](scripts/release_manager.py) | Automatische SemVer-Versionierung, `CHANGELOG.md`-Pflege & Hook-Installer |
| [`scripts/build_packages.py`](scripts/build_packages.py) | Deterministischer Cross-OS-Paket-Builder (Windows, Linux `.deb`/Tar, macOS `.app`, Source, `SHA256SUMS.txt`) |
| [`packaging/`](packaging/) | OS-spezifische Installer (`install_windows.ps1`, `installer.iss`, `install_linux.sh`, `.spec`, `PKGBUILD`, `install_macos.sh`) |
| [`tests/`](tests/) | Automatisierte Tests für Versionierung, Starter und DSGVO-neutrale Pakete |
| [`ANLEITUNG_Kollegium_Einrichtung.md`](ANLEITUNG_Kollegium_Einrichtung.md) | Ausführliche Anleitung für Kolleginnen & Kollegen (GitHub Pages, Google Sheets, Pakete, Mitarbeit) |
| [`ANLEITUNG_Google_Sheets_Anbindung.md`](ANLEITUNG_Google_Sheets_Anbindung.md) | Kurzreferenz zur Apps-Script-Brücke |
| [`VERSION`](VERSION) / [`CHANGELOG.md`](CHANGELOG.md) | Zentrale SemVer-Versionsnummer & chronologisches Änderungsprotokoll |
| [`LICENSE`](LICENSE) / [`NOTICE`](NOTICE) / [`SECURITY.md`](SECURITY.md) / [`CONTRIBUTING.md`](CONTRIBUTING.md) | Lizenz, Drittanbieter-Hinweise, DSGVO-/Sicherheitsrichtlinie & Mitmach-Leitfaden |

---

## Versionierung, Auto-Changelog & Paketbau

Das Projekt folgt **Semantic Versioning (`0.y.z`)** im Vorab-Stadium ([`VERSION`](VERSION)) und pflegt [`CHANGELOG.md`](CHANGELOG.md) automatisch nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/):

- **Lokale Git-Hooks aktivieren (DSGVO-Schutz + Auto-Versioning pro Commit):**
  ```powershell
  py -3 scripts/release_manager.py --action install-hooks
  ```
  - `feat(bereich): ...` → Minor-Version erhöhen (`0.(y+1).0`)
  - `fix(bereich): ...` / `docs:` / `refactor:` / `chore:` → Patch-Version erhöhen (`0.y.(z+1)`)
- **Automatische GitHub Releases (`.github/workflows/release.yml`):** Bei einem Push auf `main` prüft der Workflow `VERSION` und `CHANGELOG.md`, führt Tests und `--selftest` aus, baut Pakete für **Linux (`.deb`, `.tar.gz`, `.tar.xz`), macOS (`.dmg`, `.pkg`, `.app`-Archive) und Windows (`.exe`, `.zip`)** und veröffentlicht automatisch ein GitHub Release.
- **Alle Pakete lokal selbst bauen & prüfen:**
  ```powershell
  py -3 scripts/build_packages.py --clean --verify
  ```

---

## Lizenz & Copyright

Copyright © 2025–2026 **HvH-Hansen** (Hermann-von-Helmholtz-Realschule Wuppertal).  
Veröffentlicht unter der **MIT-Lizenz** – Details siehe [`LICENSE`](LICENSE), Drittanbieter-Hinweise in [`NOTICE`](NOTICE) und Datenschutz-/Sicherheitsrichtlinien in [`SECURITY.md`](SECURITY.md).

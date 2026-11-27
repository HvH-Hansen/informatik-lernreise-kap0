# Changelog

Alle nennenswerten Änderungen an der **Informatik Lernreise Kapitel 0** werden in dieser Datei dokumentiert.

Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), und dieses Projekt folgt [Semantic Versioning 2.0.0](https://semver.org/lang/de/) im Vorab-Stadium (`0.y.z`: neue Funktionsblöcke erhöhen `minor`, Fehlerbehebungen und Dokumentations-Updates erhöhen `patch`).

<!-- AUTO-CHANGELOG:START -->
## [0.4.0] - 2026-11-27

### Hinzugefügt
- **Öffnung für Kollegium & eigene Instanzen (`ANLEITUNG_Kollegium_Einrichtung.md`, `config.example.js`, `README.md`, `CONTRIBUTING.md`):**
  - Schritt-für-Schritt-Anleitung für Kolleginnen und Kollegen: eigenen GitHub-Fork anlegen, GitHub Pages aktivieren, Google Sheets (`Übersicht` & `Spielstaende`) ohne JSON-Auswertung einrichten und sicher betreiben.
  - Neutrale Vorlage `config.example.js` als Basis für eigene Instanzen und alle Installationspakete.
- **Lokale Nutzung & Cross-OS-Installationspakete (`Start_Lernreise.bat`, `Start_Lernreise.command`, `scripts/serve_local.py`, `scripts/build_packages.py`, `packaging/`):**
  - Lokaler Webserver `scripts/serve_local.py` (`127.0.0.1`, `Cache-Control: no-store` für `config.js`, `--selftest`) sowie 1-Klick-Starter für Windows, macOS und Linux inkl. Browser-Direktstart-Fallback ohne Python.
  - Deterministischer Cross-OS-Paket-Builder für Windows (`.zip`, Inno-Setup `.iss`), Linux (`.deb`, `.tar.gz`, `.tar.xz`, `.spec`, `PKGBUILD`, `.desktop`), macOS (`.app`-Bundle in `.tar.gz`/`.zip`, `.dmg`/`.pkg` via CI), Quellarchive und `SHA256SUMS.txt` – jeweils mit neutraler `config.js` (`endpointUrl: ''`) ohne persönliche URLs.
- **Automatisierte Versionierung, Git-Hooks & Release-Pipeline (`scripts/release_manager.py`, `.githooks/`, `.github/workflows/release.yml`, `tests/test_release_and_packages.py`):**
  - Automatische SemVer-/Changelog-Fortschreibung über `commit-msg`/`post-commit`-Hooks und Multi-OS-GitHub-Actions-Release-Workflow.

## [0.3.0] - 2026-11-22

### Hinzugefügt
- **HvH-Repository-Standards & Dokumentation:**
  - Zentrale [`README.md`](README.md) mit direktem Link zur Live-Lernreise und zur zentralen Google-Sheets-Auswertung, Architekturüberblick und Badges.
  - Rechtliche & organisatorische Standards analog zur `HvH_Korrektur_Engine`: `LICENSE` (MIT + DSGVO-Hinweis), `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`.
  - Versionierung & Automatisierung: `VERSION` (`0.3.0`), `CHANGELOG.md`, `.github/workflows/release.yml` (automatische Tag- & GitHub-Release-Erstellung), Issue-/PR-Vorlagen (`.github/`) sowie lokaler DSGVO-Schutz-Hook (`.githooks/pre-commit`) und erweiterte `.gitignore`.
- **Pädagogisches & visuelles Feintuning (`index.html`):**
  - Sprachsensibles HvH-Scaffolding auf Niveau **A2/B1** und einheitliches **3-Teile-Feedback**.
  - GSAP- und Lottie-Animationen ohne Audio-Ausgabe für den Einsatz im Klassenraum sowie Synchronisation aus `build_komplett_html.ps1`.

## [0.2.0] - 2026-11-22

### Hinzugefügt
- **Cloud-Spielstand & Wiederherstellung über Schul-PCs hinweg (`google_apps_script/Code.gs`, `index.html`, `ANLEITUNG_Google_Sheets_Anbindung.md`):**
  - Speicherung vollständiger Spielstände im zweiten Tabellenblatt **`Spielstaende`** über den datensparsamen Schlüssel `Klasse|Vorname|Initial`.
  - Intelligente Merge-Logik (`mergeSnapshots`) in `Code.gs`, damit bereits erledigte Aufgaben beim Gerätewechsel nicht überschrieben werden.
  - Direkte Übermittlung aus den eingebetteten Lernpfaden inkl. Cache-Busting für `config.js`.

## [0.1.0] - 2026-11-22

### Hinzugefügt
- **Erstveröffentlichung auf GitHub Pages (`index.html`, `config.js`, `google_apps_script/Code.gs`):**
  - Interaktiver Lernreise-Hub für Informatik Klasse 5/6 mit den 6 Stationen `0.1 Fachbegriffe`, `0.2 Maus & Tastatur`, `0.3 Arbeiten am PC`, `0.4 Textverarbeitung`, `0.5 Infos im Internet` und `0.6 Präsentation`.
  - Stempel-, Sterne- und Abzeichensystem sowie automatische Übertragung an das Google-Sheets-Tabellenblatt **`Übersicht`**.
<!-- AUTO-CHANGELOG:END -->

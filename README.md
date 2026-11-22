# Mediatown – Informatik Lernreise Kapitel 0 (Klasse 5/6)

[![Version](https://img.shields.io/badge/Version-v0.3.0-3730a3)](CHANGELOG.md)
[![Lizenz](https://img.shields.io/badge/Lizenz-MIT-16a34a)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Live-GitHub%20Pages-0284c7)](https://hvh-hansen.github.io/informatik-lernreise-kap0/)
[![Google Sheets](https://img.shields.io/badge/Auswertung-Google%20Sheets-0f9d58)](https://docs.google.com/spreadsheets/d/18H3WCdJIQg55TMqKm7guNF4yzV-OcdabSQxjU2GKxc8/edit?usp=sharing)

Interaktive, browserbasierte Lernreise für den Informatik-Unterricht in **Klasse 5/6** an der Hermann-von-Helmholtz-Realschule Wuppertal (HvH). Sie kombiniert **6 eigenständige Lernstationen** mit sprachsensiblem **A2/B1-Scaffolding**, wertschätzendem **3-Teile-Feedback**, Stempel- und Sternesystem sowie **Cloud-Spielstand & zentraler Auswertung** über Google Sheets (optional auch offline/statisch im Browser).

---

## Zentrale Links

| Ressource | Zweck | Link |
|---|---|---|
| **Live-Lernreise (SuS)** | Direkter Start der Lernreise auf GitHub Pages | [hvh-hansen.github.io/informatik-lernreise-kap0](https://hvh-hansen.github.io/informatik-lernreise-kap0/) |
| **Zentrale Auswertungs-Tabelle** | Klassenübersicht (`Übersicht`) & Cloud-Spielstände (`Spielstaende`) in Google Sheets | [Google Sheets öffnen](https://docs.google.com/spreadsheets/d/18H3WCdJIQg55TMqKm7guNF4yzV-OcdabSQxjU2GKxc8/edit?usp=sharing) |
| **Apps-Script-Einrichtung** | Schritt-für-Schritt-Anleitung für eigene Instanzen / Lehrkräfte | [ANLEITUNG_Google_Sheets_Anbindung.md](ANLEITUNG_Google_Sheets_Anbindung.md) |

> [!IMPORTANT]
> **Datenschutz (DSGVO / § 48 SchulG NRW):** Dieses Repository enthält ausschließlich den Quellcode und die statischen Lerninhalte. Die Anmeldung in der Lernreise erfolgt datensparsam über `Klasse | Vorname | Initial` (1. Buchstabe des Nachnamens). Es dürfen **keine** Klassenlisten, CSV-/Excel-Exporte oder `.env`-Dateien in das Repository eingecheckt werden. Bitte achten Sie als Lehrkraft darauf, dass die verlinkte Google-Sheets-Auswertung ausschließlich für berechtigte Lehrkräfte freigegeben ist (kein öffentlicher Lesezugriff).

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
| [`index.html`](index.html) | Vollständige GitHub-Pages-Lernreise (Hub + eingebettete Lernpfade `0.1–0.6`, GSAP/Lottie-UI) |
| [`config.js`](config.js) | Endpunkt-Konfiguration (`window.PC00_CONFIG`) für die Google-Apps-Script-Web-App |
| [`google_apps_script/Code.gs`](google_apps_script/Code.gs) | Google-Apps-Script-Backend (`doGet` / `doPost`) für `Übersicht` & `Spielstaende` |
| [`ANLEITUNG_Google_Sheets_Anbindung.md`](ANLEITUNG_Google_Sheets_Anbindung.md) | Einrichtung & Update der Google-Sheets-Brücke |
| [`VERSION`](VERSION) | Zentrale Versionsnummer nach Semantic Versioning (`0.3.0`) |
| [`CHANGELOG.md`](CHANGELOG.md) | Chronologisches Änderungsprotokoll (Keep a Changelog) |
| [`LICENSE`](LICENSE) | MIT-Lizenz inkl. DSGVO- & Schul-Nutzungshinweis |
| [`NOTICE`](NOTICE) | Hinweise zu verwendeten Drittanbieter-Bibliotheken & Schriftarten |
| [`SECURITY.md`](SECURITY.md) | Datenschutz- & Sicherheitsrichtlinie |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Leitfaden für Beiträge, Forks, Conventional Commits & Prüfungen |

---

## Versionierung & Releases

Das Projekt folgt **Semantic Versioning (`0.y.z`)** im Vorab-Stadium ([`VERSION`](VERSION)) und pflegt [`CHANGELOG.md`](CHANGELOG.md) nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/):

- **Conventional Commits:**
  - `feat(bereich): ...` → Minor-Version erhöhen (`0.(y+1).0`)
  - `fix(bereich): ...` / `docs:` / `refactor:` / `chore:` → Patch-Version erhöhen (`0.y.(z+1)`)
- **Automatische GitHub Releases (`.github/workflows/release.yml`):** Bei einem Push auf `main` prüft der Workflow `VERSION` und `CHANGELOG.md`, legt – falls noch nicht vorhanden – den Tag `v<VERSION>` an und erstellt automatisch ein GitHub Release samt Release Notes.
- **Lokalen DSGVO-Schutz aktivieren:**
  ```powershell
  git config core.hooksPath .githooks
  ```
  Der `pre-commit`-Hook in [`.githooks/pre-commit`](.githooks/pre-commit) verhindert versehentliche Commits von `.env*`, `Schuelerdaten/`, `*.csv` oder `*.xlsx`.

---

## Mitwirken

Hinweise zu Forks, eigenen Google-Sheets-Instanzen, Branches, Commit-Konventionen und Tests vor Pull Requests stehen in [`CONTRIBUTING.md`](CONTRIBUTING.md). Vorlagen für Issues und Pull Requests liegen in [`.github/`](.github/).

---

## Lizenz & Copyright

Copyright © 2025–2026 **HvH-Hansen** (Hermann-von-Helmholtz-Realschule Wuppertal).  
Veröffentlicht unter der **MIT-Lizenz** – Details siehe [`LICENSE`](LICENSE), Drittanbieter-Hinweise in [`NOTICE`](NOTICE) und Datenschutz-/Sicherheitsrichtlinien in [`SECURITY.md`](SECURITY.md).

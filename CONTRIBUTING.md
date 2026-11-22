# Mitwirken an der Informatik Lernreise Kapitel 0

Vielen Dank für dein Interesse, die Lernreise weiterzuentwickeln, Stationen zu verbessern oder für eigene Lerngruppen anzupassen!

## 1. Datenschutz-Grundregel (DSGVO)
- **Niemals** echte Schülerlisten, CSV-/Excel-Exporte, ausgefüllte Rückmeldebögen oder `.env`-Dateien committen.
- Prüfe vor jedem Commit mit `git status`, dass keine personenbezogenen Daten oder vertraulichen Zugangsdaten im Staging-Bereich liegen.
- Aktiviere einmalig den lokalen `pre-commit`-Hook, der sensible Dateien (`Schuelerdaten/`, `*.csv`, `*.xlsx`, `.env*`) automatisch blockiert:
  ```powershell
  git config core.hooksPath .githooks
  ```

## 2. Eigene Instanz / eigene Lerngruppe (Forks)
Wenn du die Lernreise mit einer eigenen Google-Sheets-Auswertung betreiben oder inhaltlich erweitern möchtest:
1. Erstelle auf GitHub einen **Fork** des Repositories.
2. Richte dein eigenes Tabellenblatt nach [`ANLEITUNG_Google_Sheets_Anbindung.md`](ANLEITUNG_Google_Sheets_Anbindung.md) ein und trage deine eigene Web-App-URL in `config.js` ein.
3. Aktiviere GitHub Pages für deinen Fork. Bewähren sich didaktische oder technische Verbesserungen, reiche sie gern per **Pull Request** ein (ohne deine private `config.js`-URL, falls sie nur für deine Klasse gilt).

## 3. Branches, Conventional Commits & Versionierung
1. Erstelle einen Branch vom aktuellen `main` (z. B. `feat/station-04-tipps` oder `fix/cloud-save-merge`).
2. Nutze **Conventional Commits**:
   - `feat(bereich): ...` → Minor-Bump in `VERSION` (`0.(y+1).0`)
   - `fix(bereich): ...` / `docs:` / `refactor:` / `chore:` → Patch-Bump in `VERSION` (`0.y.(z+1)`)
3. Aktualisiere bei funktionalen oder release-relevanten Änderungen gemeinsam:
   - [`VERSION`](VERSION) (einzelne Versionsnummer ohne Präfix `v`, z. B. `0.3.1`)
   - [`README.md`](README.md) (Versions-Badge oben anpassen, falls `VERSION` geändert wurde)
   - [`CHANGELOG.md`](CHANGELOG.md) (Abschnitt `## [<VERSION>] - JJJJ-MM-TT` ergänzen)
   Sobald auf `main` gepusht wird und für `VERSION` noch kein Tag existiert, erstellt `.github/workflows/release.yml` automatisch den Git-Tag und das GitHub Release.

## 4. Lokale Prüfung vor einem Pull Request
1. Öffne `index.html` lokal im Browser (z. B. über einen lokalen Static-Server oder direkt im Browser) und prüfe die geänderten Stationen sowie die Browser-Konsole auf Fehler.
2. Verwende in allen deutschsprachigen Oberflächen- und Feedbacktexten echte Umlaute (`ä, ö, ü, ß`) und achte auf verständliche A2/B1-Formulierungen sowie Tastaturbedienbarkeit.
3. Falls sich das JSON-Datenformat ändert, prüfe die Kompatibilität mit `google_apps_script/Code.gs` (`doGet`, `doPost`, `mergeSnapshots`).
4. Beschreibe im Pull Request kurz, welche Station oder Komponente angepasst wurde und wie getestet wurde.

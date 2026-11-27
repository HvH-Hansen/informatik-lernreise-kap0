# Mitwirken an der Informatik Lernreise Kapitel 0

Vielen Dank für dein Interesse, die Lernreise weiterzuentwickeln, Stationen zu verbessern oder für eigene Lerngruppen anzupassen!  
Eine vollständige Schritt-für-Schritt-Einrichtung (inkl. GitHub Pages & Google Sheets ohne JSON) findest du in [`ANLEITUNG_Kollegium_Einrichtung.md`](ANLEITUNG_Kollegium_Einrichtung.md).

## 1. Datenschutz-Grundregel (DSGVO)
- **Niemals** echte Schülerlisten, CSV-/Excel-Exporte, ausgefüllte Rückmeldebögen oder `.env`-Dateien committen.
- **Niemals** deine persönliche Google-Apps-Script-URL in einen Pull Request gegen das Haupt-Repository aufnehmen (behalte `config.js` im PR unberührt oder nutze für eigene Instanzen nur deinen Fork).
- Prüfe vor jedem Commit mit `git status`, dass keine personenbezogenen Daten oder `dist/`-Artefakte im Staging-Bereich liegen.
- Aktiviere einmalig die lokalen Git-Hooks (DSGVO-Schutz + automatische Versionierung):
  ```powershell
  # Windows
  py -3 scripts/release_manager.py --action install-hooks
  # macOS / Linux
  python3 scripts/release_manager.py --action install-hooks
  ```

## 2. Eigene Instanz / eigene Lerngruppe (Forks)
Wenn du die Lernreise mit einer eigenen Google-Sheets-Auswertung betreiben oder inhaltlich erweitern möchtest:
1. Erstelle auf GitHub einen **Fork** des Repositories.
2. Richte dein eigenes Tabellenblatt nach [`ANLEITUNG_Kollegium_Einrichtung.md`](ANLEITUNG_Kollegium_Einrichtung.md) ein und trage deine eigene Web-App-URL in `config.js` ein.
3. Aktiviere GitHub Pages für deinen Fork (`Settings → Pages → main / (root)`). Bewähren sich didaktische oder technische Verbesserungen, reiche sie gern per **Pull Request** auf einem Feature-Branch ein (**ohne** deine private `config.js`-URL).

## 3. Branches, Conventional Commits & Versionierung
1. Erstelle einen Branch vom aktuellen `main` (z. B. `feat/station-04-tipps` oder `fix/cloud-save-merge`).
2. Nutze **Conventional Commits**, da der Release-Manager daraus automatisch Versionssprung und Changelog-Eintrag erzeugt:
   - `feat(bereich): ...` → Minor-Bump (`0.(y+1).0`, Kategorie *Hinzugefügt*)
   - `fix(bereich): ...` / `docs:` / `refactor:` / `chore:` → Patch-Bump (`0.y.(z+1)`)
3. Aktualisieren die Hooks lokal nicht automatisch (z. B. ohne Python), übernimmt `.github/workflows/release.yml` beim Push auf `main` das Hochziehen von `VERSION`, `CHANGELOG.md`, `README.md`, `SECURITY.md` und den Packaging-Manifesten sowie den Cross-OS-Paketbau automatisch.

## 4. Lokale Prüfung vor einem Pull Request
1. Starte die Lernreise lokal und prüfe die geänderten Stationen sowie die Browser-Konsole auf Fehler:
   ```powershell
   # Windows
   py -3 scripts/serve_local.py --open-browser
   py -3 scripts/serve_local.py --selftest
   py -3 -m unittest discover -s tests -v
   py -3 scripts/build_packages.py --clean --verify
   # macOS / Linux
   python3 scripts/serve_local.py --open-browser
   python3 scripts/serve_local.py --selftest
   python3 -m unittest discover -s tests -v
   python3 scripts/build_packages.py --clean --verify
   ```
2. Verwende in allen deutschsprachigen Oberflächen- und Feedbacktexten echte Umlaute (`ä, ö, ü, ß`) und achte auf verständliche A2/B1-Formulierungen sowie Tastaturbedienbarkeit.
3. Falls sich das JSON-Datenformat ändert, prüfe die Kompatibilität mit `google_apps_script/Code.gs` (`doGet`, `doPost`, `mergeSnapshots`).
4. Beschreibe im Pull Request kurz, welche Station oder Komponente angepasst wurde und wie getestet wurde.

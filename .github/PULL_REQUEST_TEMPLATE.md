## Zusammenfassung der Änderungen
Kurze Beschreibung (am besten im Conventional-Commits-Format, z. B. `feat(station-03): ...` oder `fix(cloud-save): ...`).

## Checkliste vor dem Merge
- [ ] Keine Schülerdaten (Klassenlisten, CSV-/Excel-Exporte, `.env`-Dateien) im Diff enthalten (`git status` geprüft).
- [ ] Echte deutsche Umlaute (`ä, ö, ü, ß`) sowie verständliche A2/B1-Formulierungen in allen Texten verwendet.
- [ ] `index.html` lokal im Browser getestet (inkl. Konsole ohne Fehler und Tastaturnavigation).
- [ ] Falls sich Datenstruktur oder Cloud-Save geändert haben: Kompatibilität mit `google_apps_script/Code.gs` und `config.js` geprüft.
- [ ] Bei neuen Releases: `VERSION`, Versions-Badge in `README.md` und `CHANGELOG.md` gemeinsam aktualisiert.

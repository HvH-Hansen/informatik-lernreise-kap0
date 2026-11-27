## Zusammenfassung der Änderungen
Kurze Beschreibung (am besten im Conventional-Commits-Format, z. B. `feat(station-03): ...` oder `fix(cloud-save): ...`).

## Checkliste vor dem Merge
- [ ] Keine Schülerdaten (Klassenlisten, CSV-/Excel-Exporte, `.env`-Dateien) und keine `dist/`-Artefakte im Diff enthalten (`git status` geprüft).
- [ ] Keine private Google-Apps-Script-URL versehentlich in `config.js` oder `config.example.js` eingecheckt.
- [ ] Echte deutsche Umlaute (`ä, ö, ü, ß`) sowie verständliche A2/B1-Formulierungen in allen Texten verwendet.
- [ ] Lokal geprüft: `serve_local.py --selftest`, `unittest discover -s tests -v`, `build_packages.py --clean --verify` sowie `index.html` im Browser ohne Konsolenfehler.
- [ ] Falls sich Datenstruktur oder Cloud-Save geändert haben: Kompatibilität mit `google_apps_script/Code.gs` und `config.js` geprüft.

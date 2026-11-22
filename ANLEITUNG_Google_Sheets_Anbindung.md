# Google Sheets Anbindung einrichten (einmalig ca. 2 Minuten)

Damit alle Auswertungen der Kinder automatisch zentral in einer Google-Tabelle landen (ohne JSON-Upload), richte einmalig die kostenlose Apps-Script-Brücke ein:

1. **Google-Tabelle anlegen**
   - Öffne [Google Sheets](https://sheets.google.com) und erstelle eine neue leere Tabelle (z. B. `Informatik 5-6 – Lernreise Kapitel 0`).

2. **Apps Script einfügen**
   - Klicke in der Tabelle oben im Menü auf **Erweiterungen → Apps Script**.
   - Lösche den vorhandenen Platzhalter-Code (`function myFunction() {}`).
   - Kopiere den gesamten Inhalt der Datei `google_apps_script/Code.gs` hinein und speichere (Disketten-Symbol oder `Strg + S`).

3. **Als Web-App bereitstellen**
   - Klicke oben rechts auf **Bereitstellen → Neue Bereitstellung**.
   - Klicke links auf das Zahnrad neben *Typ auswählen* und wähle **Web-App**.
   - Stelle ein:
     - **Ausführen als:** `Ich` (dein Google-Konto)
     - **Zugriff haben:** `Jeder` *(wichtig, damit die Browser der Schülerinnen und Schüler ohne Google-Login abgeben dürfen)*
   - Klicke auf **Bereitstellen**, bestätige einmalig den Zugriff auf dein Tabellenblatt und kopiere die angezeigte **Web-App-URL** (beginnt mit `https://script.google.com/macros/s/.../exec`).

4. **URL in `config.js` eintragen**
   - Öffne auf GitHub (oder lokal unter `github-pages/config.js`) die Datei `config.js`.
   - Trage die kopierte URL bei `endpointUrl` ein:
     ```js
     window.PC00_CONFIG = {
       endpointUrl: 'https://script.google.com/macros/s/DEINE_ID/exec',
       autoSync: true,
       teacherLabel: 'Lehrkraft'
     };
     ```
   - Wenn du die Datei lokal geändert hast, führe `deploy_to_github.ps1` aus (oder speichere den Commit direkt im GitHub-Browser).

5. **Fertig!**
   - Sobald ein Kind eine Station schließt (automatischer Zwischenstand) oder im Tab **Abgeben** auf **„☁️ Ergebnisse an Lehrkraft senden“** klickt, erscheint bzw. aktualisiert sich die Zeile dieses Kindes automatisch im Tabellenblatt **Übersicht** – ohne doppelte Zeilen.

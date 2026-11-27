# Google Sheets Anbindung einrichten (einmalig ca. 4 Minuten)

> [!TIP]
> **Komplette Schritt-für-Schritt-Anleitung inkl. GitHub Pages, lokaler Installation & Zusammenarbeit:**
> Siehe [`ANLEITUNG_Kollegium_Einrichtung.md`](ANLEITUNG_Kollegium_Einrichtung.md).

Damit alle Auswertungen der Kinder automatisch zentral in einer Google-Tabelle landen (**ohne** JSON-Dateien einsammeln oder auswerten zu müssen) **und Spielstände an Schul-PCs später wieder geladen werden können**, richte einmalig die kostenlose Apps-Script-Brücke ein:

1. **Google-Tabelle anlegen**
   - Öffne [Google Sheets](https://sheets.google.com) und erstelle eine neue leere Tabelle (z. B. `Informatik 5-6 – Lernreise Kapitel 0`).

2. **Apps Script einfügen**
   - Klicke in der Tabelle oben im Menü auf **Erweiterungen → Apps Script**.
   - Lösche den vorhandenen Platzhalter-Code (`function myFunction() {}`).
   - Kopiere den gesamten Inhalt der Datei [`google_apps_script/Code.gs`](google_apps_script/Code.gs) hinein und speichere (Disketten-Symbol oder `Strg + S`).

3. **Als Web-App bereitstellen**
   - Klicke oben rechts auf **Bereitstellen → Neue Bereitstellung**.
   - Klicke links auf das Zahnrad neben *Typ auswählen* und wähle **Web-App**.
   - Stelle ein:
     - **Ausführen als:** `Ich` (dein Google-Konto)
     - **Zugriff haben:** `Jeder` *(wichtig, damit die Browser der Schülerinnen und Schüler ohne Google-Login speichern und laden dürfen)*
   - Klicke auf **Bereitstellen**.
   - Erscheint beim ersten Mal die Google-Meldung *„Google hat diese App nicht überprüft“*: klicke auf **Erweitert → Zu „Unbenanntes Projekt“ (unsicher) wechseln → Zulassen**.
   - Kopiere die angezeigte **Web-App-URL** (beginnt mit `https://script.google.com/macros/s/.../exec`).

4. **URL in `config.js` eintragen**
   - Öffne in deinem GitHub-Fork (oder bei lokaler Installation im Programmordner) die Datei `config.js`.
   - Trage die kopierte URL bei `endpointUrl` ein (Vorlage siehe [`config.example.js`](config.example.js)):
     ```js
     window.PC00_CONFIG = {
       endpointUrl: 'https://script.google.com/macros/s/DEINE_ID/exec',
       autoSync: true,
       teacherLabel: 'Lehrkraft'
     };
     ```
   - Auf GitHub speicherst du die Änderung direkt über **Commit changes…** (GitHub Pages übernimmt sie innerhalb von ca. 1 Minute).

5. **Fertig – Auswertung ohne JSON!**
   - Im Tabellenblatt **`Übersicht`** siehst du für jedes Kind sofort alle 6 Stationen (`✓` / `◐` / `○` inkl. Prozent & Sternen), Gesamt-Stempel, Gesamt-Sterne, Abzeichen und Zeitstempel.
   - Im zweiten Tabellenblatt **`Spielstaende`** werden automatisch die vollständigen Zwischenstände unter `klasse|vorname|initial` gesichert – meldet sich ein Kind eine Woche später an einem anderen Schul-PC wieder mit `Klasse + Vorname + 1. Buchstabe Nachname` an, wird sein bisheriger Spielstand automatisch wiederhergestellt und zusammengeführt.

> [!IMPORTANT]
> **Datenschutz (DSGVO):** Gib die Google-Tabelle selbst **niemals** öffentlich mit Lese- oder Schreibrechten frei – sie bleibt ausschließlich für dich und berechtigte Fachkolleginnen und -kollegen zugänglich.

---

## Update auf eine neue Version von `Code.gs`

Falls du `Code.gs` schon früher bereitgestellt hast, musst du die URL in `config.js` **nicht** ändern – aktualisiere einfach die bestehende Bereitstellung:

1. In deiner Google-Tabelle auf **Erweiterungen → Apps Script** gehen, den Code durch das neue `google_apps_script/Code.gs` ersetzen und speichern (`Strg + S`).
2. Rechts oben auf **Bereitstellen → Bereitstellungen verwalten** klicken.
3. Bei deiner aktiven Bereitstellung auf das **Stift-Symbol (Bearbeiten)** klicken, unter **Version** auf **Neue Version** stellen und auf **Bereitstellen** klicken. Fertig!

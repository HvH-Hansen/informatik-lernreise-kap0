# Anleitung für Kolleginnen & Kollegen: Eigene Lernreise mit GitHub Pages, Google Sheets & lokaler Installation

Diese Anleitung erklärt Schritt für Schritt und ohne technisches Vorwissen, wie du die **Informatik Lernreise Kapitel 0** für deine eigene Klasse einrichtest, Spielstände automatisch in **Google Sheets** speicherst (**ohne** eine einzige JSON-Datei einsammeln oder auswerten zu müssen), die Lernreise bei Bedarf **lokal auf Windows, macOS oder Linux** installierst und selbst am Repository mitarbeitest.

---

## Überblick: Welcher Weg passt zu dir?

| Ziel | Empfohlener Weg | Aufwand |
|---|---|---|
| **Im Unterricht mit eigener Klasse nutzen** (Browser-Link für SuS, automatische Auswertung & Cloud-Spielstand) | **Teil 1 + Teil 2:** Eigener GitHub-Fork mit GitHub Pages + eigene Google-Tabelle | ca. 5–7 Minuten (einmalig) |
| **Offline / auf dem eigenen Rechner starten** (Windows, macOS oder Linux, z. B. zum Testen oder ohne Internet) | **Teil 3:** Fertiges Installationspaket von *GitHub Releases* herunterladen | ca. 1–2 Minuten |
| **Inhalte verbessern, Aufgaben ergänzen oder Fehler melden** | **Teil 4:** Branch & Pull Request (oder direkte Mitarbeit im Team-Repo) | laufend |

---

## Teil 1: Eigene GitHub-Pages-Seite für deine Klasse einrichten (ca. 3 Min.)

Mit **GitHub Pages** erhältst du eine eigene kostenlose Schul-Webadresse (`https://<dein-benutzername>.github.io/informatik-lernreise-kap0/`), über die deine Schülerinnen und Schüler direkt im Browser arbeiten können.

1. **Bei GitHub anmelden**
   - Öffne [github.com](https://github.com) und melde dich an (oder lege kostenlos ein Konto an).
2. **Repository forken (eigene Kopie anlegen)**
   - Öffne das Haupt-Repository: [github.com/HvH-Hansen/informatik-lernreise-kap0](https://github.com/HvH-Hansen/informatik-lernreise-kap0).
   - Klicke oben rechts auf **Fork → Create fork** (Option *Copy the main branch only* aktiv lassen).
   - Du bist jetzt in deiner eigenen Kopie unter `github.com/<dein-benutzername>/informatik-lernreise-kap0`.
3. **Wichtig (DSGVO): `config.js` sofort auf deine eigene Schule/Klasse umstellen**
   - Öffne in deinem neuen Fork die Datei [`config.js`](config.js) und klicke oben rechts auf das **Stift-Symbol (Edit this file)**.
   - Standardmäßig steht dort noch die Beispiel-/Vorlagen-URL des Haupt-Repos. **Ersetze `endpointUrl`** durch:
     - entweder deine eigene URL aus **Teil 2** (empfohlen), oder
     - vorübergehend einen leeren Text `endpointUrl: ''` (dann läuft alles im lokalen Browser- & IServ-Backup-Modus, und es werden keine Daten an eine fremde Tabelle gesendet).
   - Speichere über **Commit changes…**.
4. **GitHub Pages einschalten**
   - Gehe in deinem Fork auf **Settings** (oben in der Leiste) → links im Menü auf **Pages**.
   - Stelle unter **Build and deployment**:
     - **Source:** `Deploy from a branch`
     - **Branch:** `main` und Ordner `/ (root)`
   - Klicke auf **Save**.
5. **Live-Adresse abrufen**
   - Nach ca. 1–2 Minuten erscheint oben auf der Pages-Seite deine fertige Internetadresse:
     `https://<dein-benutzername>.github.io/informatik-lernreise-kap0/`
   - Diesen Link kannst du direkt in IServ, Teams, Padlet oder als Lesezeichen an den Schul-PCs verteilen.

---

## Teil 2: Google Sheets einrichten – Spielstände speichern & auswerten ohne JSON-Dateien (ca. 4 Min.)

Damit Kinder ihren Spielstand über mehrere Unterrichtsstunden und **auf verschiedenen Schul-PCs** automatisch behalten und du als Lehrkraft alle Ergebnisse übersichtlich in einer Tabelle siehst, ohne jemals JSON-Dateien einzusammeln:

### Schritt 1: Leere Google-Tabelle erstellen
1. Öffne [sheets.google.com](https://sheets.google.com) in deinem Lehrer-Google-Konto.
2. Erstelle eine neue leere Tabelle, z. B. mit dem Namen `Informatik 5-6 – Lernreise Kapitel 0 (Klasse 5a)`.

### Schritt 2: Apps-Script-Brücke (`Code.gs`) einfügen
1. Klicke in der Google-Tabelle oben im Menü auf **Erweiterungen → Apps Script**.
2. Lösche den vorhandenen Platzhalter (`function myFunction() {}`) komplett.
3. Öffne die Datei [`google_apps_script/Code.gs`](google_apps_script/Code.gs) im Repository, kopiere den **gesamten** Inhalt und füge ihn in das Apps-Script-Fenster ein.
4. Speichere mit `Strg + S` (bzw. `Cmd + S`) oder dem Disketten-Symbol.

### Schritt 3: Als Web-App bereitstellen
1. Klicke im Apps-Script-Editor oben rechts auf **Bereitstellen → Neue Bereitstellung**.
2. Klicke links neben *Typ auswählen* auf das **Zahnrad-Symbol** und wähle **Web-App**.
3. Stelle exakt diese zwei Punkte ein:
   - **Ausführen als:** `Ich` *(dein Google-Konto)*
   - **Zugriff haben:** `Jeder` *(wichtig, damit Schülerinnen und Schüler im Unterricht ohne eigenes Google-Konto speichern und Spielstände laden dürfen)*
4. Klicke auf **Bereitstellen**.

### Schritt 4: Google-Sicherheitsdialog einmalig freigeben
Beim allerersten Bereitstellen zeigt Google eine Standard-Warnung, weil du das Skript selbst in deinem Konto angelegt hast:
1. Klicke auf **Zugriff autorisieren** und wähle dein Google-Konto.
2. Erscheint die Meldung *„Google hat diese App nicht überprüft“*: klicke links unten auf **Erweitert** und dann auf **Zu „Unbenanntes Projekt“ (unsicher) wechseln**.
3. Bestätige unten rechts mit **Zulassen**.
4. Kopiere anschließend die angezeigte **Web-App-URL** (sie beginnt mit `https://script.google.com/macros/s/.../exec`).

### Schritt 5: Web-App-URL in deinem GitHub-Fork eintragen
1. Öffne in deinem GitHub-Fork die Datei `config.js` → **Stift-Symbol (Bearbeiten)**.
2. Trage deine kopierte URL bei `endpointUrl` ein:
   ```js
   window.PC00_CONFIG = {
     endpointUrl: 'https://script.google.com/macros/s/DEINE_EIGENE_ID/exec',
     autoSync: true,
     teacherLabel: 'Lehrkraft'
   };
   ```
3. Klicke auf **Commit changes…** (GitHub Pages baut automatisch in ca. 30–60 Sekunden neu).

### Schritt 6: Funktionsprüfung & Auswertung ohne JSON
1. Öffne deine eigene GitHub-Pages-URL im Browser und lade einmal hart neu (`Strg + F5` bzw. `Cmd + Shift + R`).
2. Melde dich testweise als Beispielkind an, z. B.:
   - Klasse: `5a`
   - Vorname: `Test`
   - Initial (1. Buchstabe Nachname): `X`
3. Bearbeite in Station **0.1 Fachbegriffe** eine Aufgabe und schließe den Player über **Zurück zur Karte** (oder sende im Reiter *Abgeben* manuell).
4. Prüfe deine Google-Tabelle – es werden automatisch zwei Tabellenblätter angelegt:
   - **`Übersicht` (Auswertung für die Lehrkraft – ohne JSON!):**
     Zeigt je Kind übersichtlich `Schüler-ID`, `Klasse`, `Vorname`, `Initial`, `Stempel (x / 6)`, `Sterne (x / 18)`, den Status aller 6 Stationen (`✓` erledigt mit `%` und Sternen, `◐` angefangen, `○` offen), gesammelte `Abzeichen` und `Letzte Abgabe`. Du kannst direkt in Google Sheets nach Klasse oder Namen filtern und sortieren.
   - **`Spielstaende` (Cloud-Speicher für Schul-PCs):**
     Speichert automatisch den vollständigen Arbeitsstand unter `klasse|vorname|initial`. Meldet sich ein Kind eine Woche später an einem **anderen** Schul-PC wieder exakt mit `Klasse + Vorname + Initial` an, lädt die Lernreise seinen Spielstand automatisch aus der Cloud und führt ihn intelligent zusammen (`mergeSnapshots`), sodass bereits erledigte Aufgaben niemals verloren gehen.

> [!IMPORTANT]
> **Datenschutz (DSGVO / § 48 SchulG NRW):**
> Die Web-App-URL ermöglicht dem Browser der Lernreise das Speichern und Laden. Die **Google-Tabelle selbst** darf jedoch **niemals** über *Teilen → Jeder mit dem Link* freigegeben werden! Sie bleibt privat in deinem Google-Konto bzw. nur für berechtigte Fachkolleginnen und -kollegen freigegeben.

---

## Teil 3: Lernreise lokal auf dem eigenen Rechner installieren (Windows, macOS, Linux)

Unter [**GitHub Releases**](https://github.com/HvH-Hansen/informatik-lernreise-kap0/releases) stehen fertige Installationspakete inkl. `SHA256SUMS.txt` für alle gängigen Betriebssysteme bereit. Alle Pakete werden aus Sicherheitsgründen mit einer **neutralen `config.js`** (`endpointUrl: ''`) ausgeliefert, damit keine fremden Google-Tabellen angesprochen werden.

| System | Datei im Release | Installation & Start |
|---|---|---|
| **Windows (Installer)** | `informatik-lernreise-kap0-v<VERSION>-windows-setup.exe` | Doppelklick auf die `.exe` → legt Startmenü- & Desktop-Verknüpfung an. |
| **Windows (Portabel)** | `informatik-lernreise-kap0-v<VERSION>-windows-x64.zip` | Entpacken → `Start_Lernreise.bat` starten (oder `install_windows.ps1` per Rechtsklick *Mit PowerShell ausführen* für Desktop-Verknüpfung). |
| **macOS** | `informatik-lernreise-kap0-v<VERSION>-macos-apfs.dmg` / `.pkg` / `-macos-universal.zip` | `.dmg` öffnen & `Informatik Lernreise Kap0.app` in `Programme` ziehen (oder `.pkg` ausführen; bei `.zip` optional `./install_macos.sh`). |
| **Linux (Debian / Ubuntu)** | `informatik-lernreise-kap0_<VERSION>_all.deb` | `sudo apt install ./informatik-lernreise-kap0_<VERSION>_all.deb` → Start über Anwendungsmenü oder `informatik-lernreise-kap0`. |
| **Linux (Universal)** | `informatik-lernreise-kap0-v<VERSION>-linux-x86_64.tar.gz` / `.tar.xz` | Entpacken → `./install_linux.sh` ausführen. |

**Lokal auch mit Google Sheets verbinden (optional):**
Möchtest du auch bei einer lokalen Installation (z. B. über USB-Stick oder Schulserver) direkt in deine Google-Tabelle speichern, trage deine Web-App-URL einfach in die `config.js` im Installationsordner ein. Bei Updates per Installer/Paket bleibt eine bereits angepasste `config.js` erhalten.

---

## Teil 4: Updates holen & gemeinsam am Lernpfad mitarbeiten

### Updates vom Haupt-Repository übernehmen (im eigenen Fork)
1. Öffne deinen GitHub-Fork im Browser.
2. Wenn oben **„This branch is … commits behind HvH-Hansen:main“** steht, klicke auf **Sync fork → Update branch**.
3. Falls GitHub wegen deiner angepassten `config.js` einen Hinweis zeigt, achte darauf, dass deine `endpointUrl` in `config.js` erhalten bleibt.

### Eigene Verbesserungen zurückgeben (Pull Request / Team-Mitarbeit)
- **Als Fork-Mitwirkende:** Erstelle einen Branch (z. B. `feat/station-04-aufgabe`), mache deine Änderungen und eröffne einen **Pull Request** gegen `HvH-Hansen/informatik-lernreise-kap0`. **Wichtig:** Committe dabei **nicht** deine private `config.js`-URL!
- **Als direkt eingeladene Kollegin / Kollege (Collaborator):**
  1. Repository klonen:
     ```powershell
     git clone https://github.com/HvH-Hansen/informatik-lernreise-kap0.git
     cd informatik-lernreise-kap0
     ```
  2. Lokale Git-Hooks (DSGVO-Schutz + automatische Versionierung) aktivieren:
     - **Windows:** `py -3 scripts/release_manager.py --action install-hooks`
     - **macOS / Linux:** `python3 scripts/release_manager.py --action install-hooks`
  3. Lokal testen (`py -3 scripts/serve_local.py --open-browser` bzw. `--selftest`) und sauber per Branch + Pull Request oder Commit nach [`CONTRIBUTING.md`](CONTRIBUTING.md) einreichen.

---

## Teil 5: Häufige Fragen & Fehlerbehebung

- **„Ich habe `Code.gs` aktualisiert, aber es ändert sich nichts.“**
  In Apps Script reicht Speichern nicht: Klicke oben rechts auf **Bereitstellen → Bereitstellungen verwalten → Stift-Symbol (Bearbeiten) → Version: Neue Version → Bereitstellen**. Deine URL in `config.js` bleibt dabei gleich!
- **„Im Browser steht noch ‚Offline-Modus‘ / es erscheint kein Senden-Button.“**
  Lade die Seite mit `Strg + F5` (macOS: `Cmd + Shift + R`) komplett neu, damit `config.js` nicht aus dem Browser-Cache kommt, und prüfe, ob `endpointUrl` in `config.js` mit `https://script.google.com/macros/s/.../exec` beginnt.
- **„Der Schulbrowser blockiert Google Apps Script.“**
  Dann funktioniert automatisch der eingebaute **JSON-Backup-Export** im Tab *Abgeben*, den Schülerinnen und Schüler bei Bedarf in IServ hochladen können.

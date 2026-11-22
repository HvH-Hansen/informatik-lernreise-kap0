# Sicherheits- & Datenschutzrichtlinie (Security & DSGVO Policy)

## 1. Datenschutz & Schülerdaten (DSGVO / § 48 SchulG NRW)
Die **Informatik Lernreise Kapitel 0** trennt strikt zwischen öffentlichem Lernmaterial und schulischer Auswertung:
- **Statische Auslieferung ohne Schülerdaten im Repo:** Über GitHub Pages (`index.html`, `config.js`) werden ausschließlich statische Aufgaben- und UI-Dateien ausgeliefert. Im Repository selbst werden keinerlei Schülerdaten gespeichert.
- **Datensparsame Kennung:** Schülerinnen und Schüler melden sich lediglich mit `Klasse | Vorname | Initial` (erster Buchstabe des Nachnamens) an.
- **Zugriffsbeschränkung für Google Sheets:** Das Apps-Script-Backend (`google_apps_script/Code.gs`) nimmt Spielstände und Zusammenfassungen über `doPost`/`doGet` entgegen, damit Browser ohne Google-Konto im Unterricht arbeiten können. Die verknüpfte Google-Sheets-Tabelle (`Übersicht` und `Spielstaende`) darf jedoch **niemals** öffentlich mit Lese- oder Schreibrechten im Internet geteilt werden – der Zugriff auf die Tabelle selbst muss auf die berechtigten Lehrkräfte beschränkt bleiben.
- **Keine Zugangsdaten im Repository:** Es werden weder Passwörter noch API-Keys, OAuth-Tokens oder Schülerlisten im Repository eingecheckt.

## 2. Unterstützte Versionen
| Version | Unterstützt | Hinweis |
|---|---|---|
| `0.3.x` (aktuell) | Ja | Aktive Weiterentwicklung & Sicherheits-/Datenschutz-Updates |
| `< 0.3.0` | Nein | Frühere Initialstände ohne standardisiertes Release- & Governance-Setup |

## 3. Sicherheitslücke oder Datenschutzvorfall melden
Solltest du eine Sicherheitslücke (z. B. XSS in Lerninhalten, fehlerhafte Eingabebereinigung im Apps Script oder versehentlich offengelegte personenbezogene Daten) entdecken:
1. Erstelle **kein** öffentliches GitHub Issue mit sensiblen Details.
2. Kontaktiere das Repository-Team direkt über GitHub (**Security Advisories -> Report a vulnerability**) oder über die im GitHub-Profil hinterlegte Kontaktmöglichkeit.
3. Beschreibe die betroffene Datei bzw. Station, die Reproduktionsschritte und mögliche Auswirkungen.

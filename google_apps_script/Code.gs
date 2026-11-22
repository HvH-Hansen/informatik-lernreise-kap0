// Google Apps Script Backend für: Lernreise Kapitel 0 (Informatik Klasse 5/6)
// Anleitung: Siehe ANLEITUNG_Google_Sheets_Anbindung.md

var SHEET_NAME = 'Übersicht';
var HEADERS = [
  'Schüler-ID',
  'Klasse',
  'Vorname',
  'Initial',
  'Stempel',
  'Sterne',
  '0.1 Fachbegriffe',
  '0.2 Maus & Tastatur',
  '0.3 Arbeiten am PC',
  '0.4 Textverarbeitung',
  '0.5 Infos im Internet',
  '0.6 Präsentation',
  'Abzeichen',
  'Letzte Abgabe',
  'Rohdaten (JSON)'
];

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  return jsonResponse({
    ok: true,
    service: 'Lernreise Kapitel 0',
    status: 'aktiv'
  });
}

function formatStation(u) {
  if (!u) return '○ 0/0';
  var done = Number(u.pflicht_erledigt || 0);
  var total = Number(u.pflicht_gesamt || 0);
  var pct = Number(u.punkte_prozent || 0);
  var stars = Number(u.sterne || 0);
  if (u.status === 'done' || (total > 0 && done >= total)) {
    var starStr = '';
    for (var i = 0; i < stars; i++) starStr += '⭐';
    return '✓ ' + done + '/' + total + ' · ' + pct + '% · ' + (starStr || '☆');
  }
  if (u.status === 'started' || done > 0) {
    return '◐ ' + done + '/' + total + ' · ' + pct + '%';
  }
  return '○ 0/' + total;
}

function ensureSheet(ss) {
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    var headerRange = sheet.getRange(1, 1, 1, HEADERS.length);
    headerRange
      .setFontWeight('bold')
      .setFontColor('#ffffff')
      .setBackground('#15303f')
      .setVerticalAlignment('middle');
    sheet.setFrozenRows(1);
    headerRange.createFilter();
    sheet.setColumnWidth(1, 160);
    sheet.setColumnWidth(2, 70);
    sheet.setColumnWidth(3, 120);
    sheet.setColumnWidth(4, 70);
    sheet.setColumnWidth(5, 85);
    sheet.setColumnWidth(6, 85);
    for (var c = 7; c <= 12; c++) sheet.setColumnWidth(c, 165);
    sheet.setColumnWidth(13, 180);
    sheet.setColumnWidth(14, 165);
    sheet.setColumnWidth(15, 220);
  }
  return sheet;
}

function buildCompactRawJson(data) {
  var compactUnits = (data.einheiten || []).map(function (u) {
    return {
      id: u.id,
      status: u.status,
      sterne: u.sterne,
      pflicht_erledigt: u.pflicht_erledigt,
      pflicht_gesamt: u.pflicht_gesamt,
      zusatz_erledigt: u.zusatz_erledigt,
      punkte_prozent: u.punkte_prozent,
      tasks: u.roh_stand && u.roh_stand.tasks ? u.roh_stand.tasks : null
    };
  });
  var str = JSON.stringify({
    schueler: data.schueler,
    gespeichert: data.gespeichert,
    zusammenfassung: data.zusammenfassung,
    einheiten: compactUnits
  });
  if (str.length > 48000) {
    str = str.slice(0, 48000) + '…';
  }
  return str;
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return jsonResponse({ ok: false, error: 'Keine Daten empfangen' });
    }
    var data = JSON.parse(e.postData.contents);
    var s = data.schueler || {};
    var klasse = String(s.klasse || '').trim();
    var vorname = String(s.vorname || '').trim();
    var initial = String(s.initial || '').trim().toUpperCase();

    if (!klasse || !vorname || !initial) {
      return jsonResponse({ ok: false, error: 'Unvollständige Schülerdaten' });
    }

    var schuelerId = (klasse + '|' + vorname + '|' + initial).toLowerCase();
    var zus = data.zusammenfassung || {};
    var stempelText = Number(zus.stempel || 0) + ' / ' + Number(zus.stempel_max || 6);
    var sterneText = Number(zus.sterne || 0) + ' / ' + Number(zus.sterne_max || 18);
    var abzeichen = Array.isArray(zus.abzeichen) ? zus.abzeichen.join(', ') : '';

    var unitMap = {};
    var einheiten = Array.isArray(data.einheiten) ? data.einheiten : [];
    for (var i = 0; i < einheiten.length; i++) {
      if (einheiten[i] && einheiten[i].id) {
        unitMap[String(einheiten[i].id)] = einheiten[i];
      }
    }

    var nowStr = Utilities.formatDate(new Date(), 'Europe/Berlin', 'dd.MM.yyyy HH:mm:ss');
    var rowValues = [
      schuelerId,
      klasse,
      vorname,
      initial,
      stempelText,
      sterneText,
      formatStation(unitMap['0.1']),
      formatStation(unitMap['0.2']),
      formatStation(unitMap['0.3']),
      formatStation(unitMap['0.4']),
      formatStation(unitMap['0.5']),
      formatStation(unitMap['0.6']),
      abzeichen,
      nowStr,
      buildCompactRawJson(data)
    ];

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ensureSheet(ss);

    var lastRow = sheet.getLastRow();
    var targetRow = -1;
    if (lastRow >= 2) {
      var idCol = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
      for (var r = 0; r < idCol.length; r++) {
        if (String(idCol[r][0]).trim().toLowerCase() === schuelerId) {
          targetRow = r + 2;
          break;
        }
      }
    }

    var updated = false;
    if (targetRow > 0) {
      sheet.getRange(targetRow, 1, 1, rowValues.length).setValues([rowValues]);
      updated = true;
    } else {
      sheet.appendRow(rowValues);
    }

    return jsonResponse({
      ok: true,
      updated: updated,
      schuelerId: schuelerId,
      timestamp: nowStr
    });
  } catch (err) {
    return jsonResponse({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

// Google Apps Script Backend für: Lernreise Kapitel 0 (Informatik Klasse 5/6)
// Unterstützt automatisches Speichern (Übersicht + Spielstände) UND Wiederherstellen über Klasse|Vorname|Initial.
// Anleitung: Siehe ANLEITUNG_Google_Sheets_Anbindung.md

var SHEET_NAME = 'Übersicht';
var STATE_SHEET_NAME = 'Spielstaende';

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

var STATE_HEADERS = ['Schüler-ID', 'Aktualisiert', 'Spielstand (JSON)'];
var STATION_IDS = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6'];
var STATION_ACH = { '0.1': 's01', '0.2': 's02', '0.3': 's03', '0.4': 's04', '0.5': 's05', '0.6': 's06' };

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function normalizeId(klasse, vorname, initial) {
  return (String(klasse || '').trim() + '|' + String(vorname || '').trim() + '|' + String(initial || '').trim()).toLowerCase();
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

function ensureStateSheet(ss) {
  var sheet = ss.getSheetByName(STATE_SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(STATE_SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(STATE_HEADERS);
    var headerRange = sheet.getRange(1, 1, 1, STATE_HEADERS.length);
    headerRange
      .setFontWeight('bold')
      .setFontColor('#ffffff')
      .setBackground('#15303f')
      .setVerticalAlignment('middle');
    sheet.setFrozenRows(1);
    sheet.setColumnWidth(1, 180);
    sheet.setColumnWidth(2, 165);
    sheet.setColumnWidth(3, 360);
  }
  return sheet;
}

function findRowById(sheet, id) {
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return -1;
  var idCol = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
  for (var r = 0; r < idCol.length; r++) {
    if (String(idCol[r][0]).trim().toLowerCase() === id) {
      return r + 2;
    }
  }
  return -1;
}

function loadSnapshotById(ss, id) {
  var stateSheet = ss.getSheetByName(STATE_SHEET_NAME);
  if (!stateSheet) {
    return { ok: true, found: false, schuelerId: id };
  }
  var rowIdx = findRowById(stateSheet, id);
  if (rowIdx < 0) {
    return { ok: true, found: false, schuelerId: id };
  }
  var row = stateSheet.getRange(rowIdx, 1, 1, 3).getValues()[0];
  var snapshot = null;
  try {
    snapshot = JSON.parse(String(row[2] || ''));
  } catch (err) {
    return { ok: true, found: false, schuelerId: id };
  }
  return {
    ok: true,
    found: true,
    schuelerId: id,
    updatedAt: row[1],
    snapshot: snapshot
  };
}

function doGet(e) {
  try {
    if (e && e.parameter && e.parameter.action === 'load' && e.parameter.id) {
      var id = String(e.parameter.id).trim().toLowerCase();
      if (!id) return jsonResponse({ ok: false, error: 'Keine Schüler-ID angegeben' });
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      return jsonResponse(loadSnapshotById(ss, id));
    }
    return jsonResponse({
      ok: true,
      service: 'Lernreise Kapitel 0',
      status: 'aktiv',
      supportsLoad: true
    });
  } catch (err) {
    return jsonResponse({ ok: false, error: String(err) });
  }
}

function countStationTasks(raw) {
  if (!raw || !raw.tasks) return 0;
  var n = 0;
  var keys = Object.keys(raw.tasks);
  for (var i = 0; i < keys.length; i++) {
    var t = raw.tasks[keys[i]];
    if (t && t.status && t.status !== 'offen') n++;
  }
  return n;
}

function countSnapshotProgress(snap) {
  if (!snap) return 0;
  var total = 0;
  if (snap.stations) {
    for (var i = 0; i < STATION_IDS.length; i++) {
      total += countStationTasks(snap.stations[STATION_IDS[i]]);
    }
  } else if (Array.isArray(snap.einheiten)) {
    for (var j = 0; j < snap.einheiten.length; j++) {
      total += countStationTasks(snap.einheiten[j].roh_stand);
    }
  }
  return total;
}

function savedTimeMs(raw) {
  if (!raw || !raw.lastSavedAt) return 0;
  var ms = new Date(raw.lastSavedAt).getTime();
  return isNaN(ms) ? 0 : ms;
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

function mergeSnapshots(existingSnap, incomingData) {
  var unitMap = {};
  var einheiten = Array.isArray(incomingData.einheiten) ? incomingData.einheiten : [];
  for (var i = 0; i < einheiten.length; i++) {
    if (einheiten[i] && einheiten[i].id) {
      unitMap[String(einheiten[i].id)] = einheiten[i];
    }
  }

  var existingStations = (existingSnap && existingSnap.stations) ? existingSnap.stations : {};
  var existingSummaries = (existingSnap && existingSnap.summaries) ? existingSnap.summaries : {};

  var mergedStations = {};
  var mergedSummaries = {};

  for (var sIdx = 0; sIdx < STATION_IDS.length; sIdx++) {
    var stId = STATION_IDS[sIdx];
    var incU = unitMap[stId] || null;
    var incRaw = incU && incU.roh_stand ? incU.roh_stand : null;
    var incSum = incU ? {
      id: stId,
      status: incU.status || 'open',
      sterne: Number(incU.sterne || 0),
      pflicht_erledigt: Number(incU.pflicht_erledigt || 0),
      pflicht_gesamt: Number(incU.pflicht_gesamt || 0),
      zusatz_erledigt: Number(incU.zusatz_erledigt || 0),
      punkte_prozent: Number(incU.punkte_prozent || 0)
    } : null;

    var exRaw = existingStations[stId] || null;
    var exSum = existingSummaries[stId] || null;

    var incCnt = countStationTasks(incRaw);
    var exCnt = countStationTasks(exRaw);
    var incMs = savedTimeMs(incRaw);
    var exMs = savedTimeMs(exRaw);

    var useIncoming = false;
    if (incCnt > exCnt) {
      useIncoming = true;
    } else if (incCnt === exCnt) {
      if (incCnt > 0) {
        useIncoming = incMs >= exMs;
      } else if (!exRaw) {
        useIncoming = true;
      }
    }

    if (useIncoming) {
      if (incRaw) mergedStations[stId] = incRaw;
      if (incSum) mergedSummaries[stId] = incSum;
    } else {
      if (exRaw) mergedStations[stId] = exRaw;
      if (exSum) mergedSummaries[stId] = exSum;
      else if (incSum) mergedSummaries[stId] = incSum;
    }
  }

  var stempel = 0;
  var sterne = 0;
  var anyStarted = false;
  var badges = [];

  for (var bIdx = 0; bIdx < STATION_IDS.length; bIdx++) {
    var id = STATION_IDS[bIdx];
    var sm = mergedSummaries[id];
    if (!sm) continue;
    if (sm.status !== 'open' || sm.pflicht_erledigt > 0) anyStarted = true;
    sterne += Number(sm.sterne || 0);
    if (sm.status === 'done' || (sm.pflicht_gesamt > 0 && sm.pflicht_erledigt >= sm.pflicht_gesamt)) {
      stempel++;
      if (STATION_ACH[id]) badges.push(STATION_ACH[id]);
    }
  }
  if (anyStarted) badges.unshift('start');
  if (stempel === STATION_IDS.length) badges.push('master');

  return {
    snapshot: {
      schueler: incomingData.schueler,
      begleiter: incomingData.begleiter || (existingSnap && existingSnap.begleiter) || 'fuchs',
      gespeichert: incomingData.gespeichert || new Date().toISOString(),
      stations: mergedStations,
      summaries: mergedSummaries,
      abzeichen: badges
    },
    stempel: stempel,
    stempelMax: STATION_IDS.length,
    sterne: sterne,
    sterneMax: STATION_IDS.length * 3,
    abzeichen: badges
  };
}

function serializeSnapshotSafe(snap) {
  var str = JSON.stringify(snap);
  if (str.length <= 45000) return str;

  var copy = JSON.parse(str);
  var keys = Object.keys(copy.stations || {});
  for (var i = 0; i < keys.length; i++) {
    var st = copy.stations[keys[i]];
    if (st) {
      delete st.idle;
      delete st.stationSec;
    }
  }
  str = JSON.stringify(copy);
  if (str.length <= 49000) return str;

  delete copy.summaries;
  return JSON.stringify(copy).slice(0, 49000);
}

function buildCompactRawJson(merged) {
  var str = JSON.stringify({
    schueler: merged.snapshot.schueler,
    gespeichert: merged.snapshot.gespeichert,
    stempel: merged.stempel,
    sterne: merged.sterne,
    summaries: merged.snapshot.summaries
  });
  if (str.length > 48000) str = str.slice(0, 48000) + '…';
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
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    if (data && data.action === 'load' && data.id) {
      return jsonResponse(loadSnapshotById(ss, String(data.id).trim().toLowerCase()));
    }

    var s = data.schueler || {};
    var klasse = String(s.klasse || '').trim();
    var vorname = String(s.vorname || '').trim();
    var initial = String(s.initial || '').trim().toUpperCase();

    if (!klasse || !vorname || !initial) {
      return jsonResponse({ ok: false, error: 'Unvollständige Schülerdaten' });
    }

    var schuelerId = normalizeId(klasse, vorname, initial);
    var stateSheet = ensureStateSheet(ss);
    var existingRes = loadSnapshotById(ss, schuelerId);
    var existingSnap = existingRes.found ? existingRes.snapshot : null;

    var existingCount = countSnapshotProgress(existingSnap);
    var incomingCount = countSnapshotProgress(data);
    if (existingCount > 0 && incomingCount === 0) {
      return jsonResponse({
        ok: true,
        skippedEmpty: true,
        schuelerId: schuelerId
      });
    }

    var merged = mergeSnapshots(existingSnap, data);
    var nowStr = Utilities.formatDate(new Date(), 'Europe/Berlin', 'dd.MM.yyyy HH:mm:ss');

    var snapJson = serializeSnapshotSafe(merged.snapshot);
    var stateRowValues = [schuelerId, nowStr, snapJson];
    var stateRowIdx = findRowById(stateSheet, schuelerId);
    if (stateRowIdx > 0) {
      stateSheet.getRange(stateRowIdx, 1, 1, stateRowValues.length).setValues([stateRowValues]);
    } else {
      stateSheet.appendRow(stateRowValues);
    }

    var overviewSheet = ensureSheet(ss);
    var sumMap = merged.snapshot.summaries || {};
    var rowValues = [
      schuelerId,
      klasse,
      vorname,
      initial,
      merged.stempel + ' / ' + merged.stempelMax,
      merged.sterne + ' / ' + merged.sterneMax,
      formatStation(sumMap['0.1']),
      formatStation(sumMap['0.2']),
      formatStation(sumMap['0.3']),
      formatStation(sumMap['0.4']),
      formatStation(sumMap['0.5']),
      formatStation(sumMap['0.6']),
      merged.abzeichen.join(', '),
      nowStr,
      buildCompactRawJson(merged)
    ];

    var targetRow = findRowById(overviewSheet, schuelerId);
    var updated = false;
    if (targetRow > 0) {
      overviewSheet.getRange(targetRow, 1, 1, rowValues.length).setValues([rowValues]);
      updated = true;
    } else {
      overviewSheet.appendRow(rowValues);
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

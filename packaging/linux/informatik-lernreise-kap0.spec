Name:           informatik-lernreise-kap0
Version:        0.4.0
Release:        1%{?dist}
Summary:        Interaktive Informatik-Lernreise Kapitel 0 (Klasse 5/6)

License:        MIT
URL:            https://github.com/HvH-Hansen/informatik-lernreise-kap0
Source0:        informatik-lernreise-kap0-v%{version}-source.tar.gz

BuildArch:      noarch
Recommends:     python3 >= 3.8

%description
Mediatown – Interaktive, browserbasierte Informatik-Lernreise für Klasse 5/6
(6 Stationen: Fachbegriffe, Maus & Tastatur, Arbeiten am PC, Textverarbeitung,
Infos im Internet, Präsentation) mit optionaler Google-Sheets-Auswertung.

%prep
%setup -q -n informatik-lernreise-kap0-v%{version}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/informatik-lernreise-kap0
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

cp -a VERSION LICENSE NOTICE README.md CHANGELOG.md \
      ANLEITUNG_Kollegium_Einrichtung.md ANLEITUNG_Google_Sheets_Anbindung.md \
      index.html config.example.js Start_Lernreise.command \
      google_apps_script assets %{buildroot}/opt/informatik-lernreise-kap0/
mkdir -p %{buildroot}/opt/informatik-lernreise-kap0/scripts
cp -a scripts/serve_local.py %{buildroot}/opt/informatik-lernreise-kap0/scripts/
cp config.example.js %{buildroot}/opt/informatik-lernreise-kap0/config.js

cat > %{buildroot}%{_bindir}/informatik-lernreise-kap0 <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="/opt/informatik-lernreise-kap0"
cd "$APP_DIR"
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1; then
    if "$cand" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then
      exec "$cand" "$APP_DIR/scripts/serve_local.py" --open-browser "$@"
    fi
  fi
done
exec xdg-open "$APP_DIR/index.html"
EOF
chmod 0755 %{buildroot}%{_bindir}/informatik-lernreise-kap0

install -m 0644 packaging/linux/informatik-lernreise-kap0.desktop \
  %{buildroot}%{_datadir}/applications/informatik-lernreise-kap0.desktop
install -m 0644 assets/icon.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/informatik-lernreise-kap0.svg

%files
%license LICENSE
%doc README.md CHANGELOG.md NOTICE ANLEITUNG_Kollegium_Einrichtung.md
/opt/informatik-lernreise-kap0
%config(noreplace) /opt/informatik-lernreise-kap0/config.js
%{_bindir}/informatik-lernreise-kap0
%{_datadir}/applications/informatik-lernreise-kap0.desktop
%{_datadir}/icons/hicolor/scalable/apps/informatik-lernreise-kap0.svg

%changelog
* Fri Nov 27 2026 HvH-Hansen <noreply@github.com> - 0.4.0-1
- Cross-OS-Pakete, Kollegiums-Anleitung und automatische Release-Pipeline.

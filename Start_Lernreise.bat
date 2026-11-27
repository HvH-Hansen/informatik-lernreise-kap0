@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "PY_CMD="
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if not errorlevel 1 set "PY_CMD=py -3"

if "%PY_CMD%"=="" (
    python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
    if not errorlevel 1 set "PY_CMD=python3"
)

if "%PY_CMD%"=="" (
    python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
    if not errorlevel 1 set "PY_CMD=python"
)

if not "%PY_CMD%"=="" (
    echo Starte Informatik Lernreise Kapitel 0 ueber lokalen Webserver ^(%PY_CMD%^)...
    %PY_CMD% scripts\serve_local.py --open-browser %*
    if not errorlevel 1 goto :eof
)

echo [HINWEIS] Python 3 wurde nicht gefunden - oeffne index.html direkt im Standardbrowser.
start "" "%~dp0index.html"

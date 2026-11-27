#Requires -Version 5.1
<#
.SYNOPSIS
    Installiert die Informatik Lernreise Kapitel 0 lokal unter Windows.
.DESCRIPTION
    Kopiert bei Bedarf die Lernreise-Dateien in das Zielverzeichnis (bewahrt eine vorhandene config.js),
    prueft den lokalen Starter (falls Python 3 vorhanden) und legt Desktop- sowie Startmenue-Verknuepfungen an.
#>
[CmdletBinding()]
param(
    [string]$InstallDir = "",
    [switch]$InPlace,
    [switch]$NoShortcut
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path (Join-Path $ScriptDir "index.html")) {
    $SourceDir = $ScriptDir
} else {
    $SourceDir = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
}

if ([string]::IsNullOrWhiteSpace($InstallDir)) {
    if ($InPlace -or (Test-Path (Join-Path $ScriptDir "index.html"))) {
        $InstallDir = $SourceDir
    } else {
        $InstallDir = Join-Path $env:LOCALAPPDATA "Informatik_Lernreise_Kap0"
    }
}

Write-Host "=== Informatik Lernreise Kapitel 0 Installer (Windows) ===" -ForegroundColor Cyan
Write-Host "Installationsverzeichnis: $InstallDir"

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

$NormSrc = [System.IO.Path]::GetFullPath($SourceDir).TrimEnd('\')
$NormDst = [System.IO.Path]::GetFullPath($InstallDir).TrimEnd('\')

if ($NormSrc -ne $NormDst) {
    foreach ($file in @("index.html", "config.example.js", "Start_Lernreise.bat", "README.md", "CHANGELOG.md", "ANLEITUNG_Kollegium_Einrichtung.md", "ANLEITUNG_Google_Sheets_Anbindung.md", "LICENSE", "NOTICE", "VERSION")) {
        $srcFile = Join-Path $SourceDir $file
        if (Test-Path $srcFile) {
            Copy-Item -Path $srcFile -Destination (Join-Path $InstallDir $file) -Force
        }
    }
    foreach ($dir in @("assets", "google_apps_script", "scripts")) {
        $srcSub = Join-Path $SourceDir $dir
        if (Test-Path $srcSub) {
            Copy-Item -Path $srcSub -Destination $InstallDir -Recurse -Force
        }
    }
}

$TargetCfg = Join-Path $InstallDir "config.js"
$ExampleCfg = Join-Path $InstallDir "config.example.js"
if (-not (Test-Path $TargetCfg) -and (Test-Path $ExampleCfg)) {
    Copy-Item -Path $ExampleCfg -Destination $TargetCfg
    Write-Host "Neutrale config.js erstellt (Offline-/Lokalmodus; Google-Sheets-URL bei Bedarf nachtragen)." -ForegroundColor Green
} else {
    Write-Host "Bestehende config.js wurde beibehalten." -ForegroundColor Yellow
}

$PythonCmd = $null
foreach ($cand in @("py -3", "python3", "python")) {
    try {
        $parts = $cand -split " "
        if ($parts.Length -gt 1) {
            & $parts[0] @($parts[1..($parts.Length - 1)]) -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" 2>&1 | Out-Null
        } else {
            & $parts[0] -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" 2>&1 | Out-Null
        }
        if ($LASTEXITCODE -eq 0) {
            $PythonCmd = $parts
            break
        }
    } catch {}
}

if ($PythonCmd) {
    Write-Host "Pruefe lokalen Starter (--selftest)..."
    $ServeScript = Join-Path $InstallDir "scripts\serve_local.py"
    if (Test-Path $ServeScript) {
        if ($PythonCmd.Length -gt 1) {
            & $PythonCmd[0] @($PythonCmd[1..($PythonCmd.Length - 1)]) $ServeScript --selftest
        } else {
            & $PythonCmd[0] $ServeScript --selftest
        }
    }
} else {
    Write-Host "[HINWEIS] Kein Python 3 gefunden - Start_Lernreise.bat oeffnet index.html direkt im Standardbrowser." -ForegroundColor Yellow
}

if (-not $NoShortcut) {
    $WshShell = New-Object -ComObject WScript.Shell
    $BatPath = Join-Path $InstallDir "Start_Lernreise.bat"
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $StartMenuDir = Join-Path ([Environment]::GetFolderPath("Programs")) "Informatik Lernreise Kapitel 0"
    New-Item -ItemType Directory -Force -Path $StartMenuDir | Out-Null

    foreach ($TargetDir in @($DesktopPath, $StartMenuDir)) {
        $LnkPath = Join-Path $TargetDir "Informatik Lernreise Kap. 0.lnk"
        $Shortcut = $WshShell.CreateShortcut($LnkPath)
        $Shortcut.TargetPath = $BatPath
        $Shortcut.WorkingDirectory = $InstallDir
        $Shortcut.Description = "Informatik Lernreise Kapitel 0 starten"
        $Shortcut.Save()
    }
    Write-Host "Desktop- und Startmenue-Verknuepfung erstellt." -ForegroundColor Green
}

Write-Host "`nInstallation abgeschlossen! Start mit Start_Lernreise.bat" -ForegroundColor Green

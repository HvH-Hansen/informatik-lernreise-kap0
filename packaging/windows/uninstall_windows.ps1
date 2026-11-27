#Requires -Version 5.1
<#
.SYNOPSIS
    Entfernt die Verknuepfungen der Informatik Lernreise Kapitel 0 unter Windows.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "SilentlyContinue"
$DesktopLnk = Join-Path ([Environment]::GetFolderPath("Desktop")) "Informatik Lernreise Kap. 0.lnk"
$StartMenuDir = Join-Path ([Environment]::GetFolderPath("Programs")) "Informatik Lernreise Kapitel 0"

if (Test-Path $DesktopLnk) { Remove-Item $DesktopLnk -Force }
if (Test-Path $StartMenuDir) { Remove-Item $StartMenuDir -Recurse -Force }

Write-Host "Verknuepfungen entfernt (Ordner und config.js blieben unangetastet)." -ForegroundColor Green

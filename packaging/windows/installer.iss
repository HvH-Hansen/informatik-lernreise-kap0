; Inno Setup 6 Script für Informatik Lernreise Kapitel 0 (Windows)
#define MyAppName "Informatik Lernreise Kapitel 0"
#define MyAppVersion "0.4.0"
#define MyAppPublisher "HvH-Hansen (Hermann-von-Helmholtz-Realschule Wuppertal)"
#define MyAppURL "https://github.com/HvH-Hansen/informatik-lernreise-kap0"
#define MyAppExeName "Start_Lernreise.bat"

[Setup]
AppId={{C3A7D21E-9B44-4E2A-B8E1-62F0A87D4902}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
DefaultDirName={localappdata}\Informatik_Lernreise_Kap0
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\..\LICENSE
OutputDir=..\..\dist\v{#MyAppVersion}
OutputBaseFilename=informatik-lernreise-kap0-v{#MyAppVersion}-windows-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\..\VERSION"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\NOTICE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\ANLEITUNG_Kollegium_Einrichtung.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\ANLEITUNG_Google_Sheets_Anbindung.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\index.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\config.example.js"; DestDir: "{app}"; Flags: ignoreversion
; Neutrale config.js aus config.example.js bereitstellen (bestehende Benutzer-config.js beim Update erhalten)
Source: "..\..\config.example.js"; DestDir: "{app}"; DestName: "config.js"; Flags: ignoreversion onlyifdoesntexist
Source: "..\..\Start_Lernreise.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\google_apps_script\*"; DestDir: "{app}\google_apps_script"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\..\scripts\serve_local.py"; DestDir: "{app}\scripts"; Flags: ignoreversion
Source: "..\..\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ".\install_windows.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\uninstall_windows.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Google-Sheets- & GitHub-Anleitung"; Filename: "{app}\ANLEITUNG_Kollegium_Einrichtung.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: shellexec postinstall skipifsilent

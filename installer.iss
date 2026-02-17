; Inno Setup script for DnD Logger
; Installs to %LOCALAPPDATA% — no admin rights required.

#define MyAppName "DnD Logger"
#ifndef MyAppVersion
  #define MyAppVersion "1.0.0"
#endif
#define MyAppPublisher "DnDLogger"
#define MyAppExeName "DnD Logger.exe"

[Setup]
AppId={{8F2C4A6D-1B3E-4D5F-9A7C-2E8B6D0F3A1C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=installer_output
OutputBaseFilename=DnDLogger_Setup_{#MyAppVersion}
SetupIconFile=assets\images\app\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
RestartApplications=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\DnD Logger\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[Code]
function GetAppLangCode(): String;
var
  Lang: String;
begin
  Lang := ActiveLanguage;
  if Lang = 'french' then Result := 'fr'
  else if Lang = 'german' then Result := 'de'
  else if Lang = 'spanish' then Result := 'es'
  else if Lang = 'italian' then Result := 'it'
  else if Lang = 'dutch' then Result := 'nl'
  else if Lang = 'portuguese' then Result := 'pt'
  else Result := 'en';
end;

procedure WriteLanguageConfig;
var
  ConfigDir, ConfigPath, Json: String;
begin
  ConfigDir := ExpandConstant('{userappdata}\{#MyAppName}');
  ForceDirectories(ConfigDir);
  ConfigPath := ConfigDir + '\config.json';
  if not FileExists(ConfigPath) then
  begin
    Json := '{' + #13#10 + '  "language": "' + GetAppLangCode + '"' + #13#10 + '}';
    SaveStringToFile(ConfigPath, Json, False);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    WriteLanguageConfig;
end;

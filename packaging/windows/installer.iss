#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

[Setup]
AppId={{6E3B1C7A-4F2D-4B8E-9A51-2C7D8E0F1A93}
AppName=YT Audio Downloader
AppVersion={#AppVersion}
AppPublisher=TI-Carlos
AppPublisherURL=https://github.com/B4ruk/yt-audio-downloader
DefaultDirName={autopf}\YT Audio Downloader
DefaultGroupName=YT Audio Downloader
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
LicenseFile=..\..\LICENSE
SetupIconFile=..\..\assets\icon.ico
UninstallDisplayIcon={app}\YT-Audio-Downloader.exe
OutputDir=..\..\release
OutputBaseFilename=YT-Audio-Downloader-{#AppVersion}-windows-x64-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\..\dist\YT-Audio-Downloader\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\YT Audio Downloader"; Filename: "{app}\YT-Audio-Downloader.exe"
Name: "{group}\{cm:UninstallProgram,YT Audio Downloader}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\YT Audio Downloader"; Filename: "{app}\YT-Audio-Downloader.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\YT-Audio-Downloader.exe"; Description: "{cm:LaunchProgram,YT Audio Downloader}"; Flags: nowait postinstall skipifsilent

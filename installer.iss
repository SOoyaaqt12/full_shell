; installer.iss
[Setup]
AppName=DaffaShell
AppVersion=1.0
DefaultDirName={pf}\DaffaShell
DefaultGroupName=DaffaShell
OutputBaseFilename=DaffaShellInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "installer\full_shell.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer\hacker_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DaffaShell"; Filename: "{app}\full_shell.exe"; IconFilename: "{app}\hacker_icon.ico"
Name: "{commondesktop}\DaffaShell"; Filename: "{app}\full_shell.exe"; IconFilename: "{app}\hacker_icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\full_shell.exe"; Description: "Run DaffaShell"; Flags: nowait postinstall skipifsilent

dim fso: set fso = CreateObject("Scripting.FileSystemObject")
dim CurrentDirectory
CurrentDirectory = fso.GetAbsolutePathName(".")

set WshShell = WScript.CreateObject("WScript.Shell" )
set oShellLink = WshShell.CreateShortcut( WshShell.SpecialFolders("desktop") & "\Keylock.lnk")
oShellLink.TargetPath = CurrentDirectory  & "\Keylock.exe"
oShellLink.WindowStyle = 1
oShellLink.WorkingDirectory=CurrentDirectory  
oShellLink.IconLocation = CurrentDirectory  & "\icons\short_icon.ico"
oShellLink.Save

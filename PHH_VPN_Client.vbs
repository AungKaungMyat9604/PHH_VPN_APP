' Double-clickable launcher for PHH VPN Client (Windows - No Console Window)
' This VBScript runs the app without showing a command prompt window

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
objShell.CurrentDirectory = strScriptPath

' Check if virtual environment exists
If Not objFSO.FolderExists("venv") Then
    ' Run setup script
    objShell.Run "cmd /c setup_venv.bat", 1, True
End If

' Run the app (hidden window)
objShell.Run "cmd /c venv\Scripts\activate.bat && python vpn_app.py", 0, False

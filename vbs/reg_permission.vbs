Set objWMIService = GetObject("winmgmts:\\.\root\Cimv2")
Set objTrustee = objWMIService.Get("Win32_Trustee").SpawnInstance_()
objTrustee.Domain = "BUILTIN"
objTrustee.Name = "Administrators"
objTrustee.SID = Array(1,2,0,0,0,0,0,5,32,0,0,0,32,2,0,0)
objTrustee.SidLength = 16
objTrustee.SIDString = "S-1-5-32-544"

Set objNewACE = objWMIService.Get("Win32_ACE").SpawnInstance_()
objNewACE.AccessMask = 983103
objNewACE.AceType = 0
objNewACE.AceFlags = 2
objNewACE.Trustee = objTrustee

Const HKLM = &H80000002
strKeyPath = "SAM\SAM"
Set oReg = GetObject("Winmgmts:\root\default:StdRegProv")
RetVal = oReg.GetSecurityDescriptor(HKLM,strKeyPath,wmiSecurityDescriptor)
DACL = wmiSecurityDescriptor.DACL
ReDim objNewDacl(0)
Set objNewDacl(0) = objNewACE
For each objACE in DACL
    Ubd = UBound(objNewDacl)
    ReDim preserve objNewDacl(Ubd+1)
    Set objNewDacl(Ubd+1) = objACE
Next
wmiSecurityDescriptor.DACL = objNewDacl
RetVal = oReg.SetSecurityDescriptor(HKLM,strKeyPath,wmiSecurityDescriptor)
from module import *
from module import wmiconnect

def enablerdp(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    if int(isenable)==2: #偷懒
        dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
        iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
        StdRegProv, resp = iWbemServices.GetObject("StdRegProv")
        rdpport = StdRegProv.GetDWORDValue(2147483650,
                                           "SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp",
                                           "PortNumber")
        print("[*] RDP Port:{}".format(rdpport.uValue))
        dcom.disconnect()
        exit()
    if int(isenable)!=1 and  int(isenable)!=0:
        print("[-] Pluse Query Help,Thanks....")
        exit()

    print("[*] Enable/Disable RDP")
    dcom,iWbemLevel1Login=wmiconnect.wmiconnect(ip,username,password,domain,hashes,aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2/TerminalServices', NULL, NULL)
    iWbemServices.get_dce_rpc().set_auth_level(RPC_C_AUTHN_LEVEL_PKT_PRIVACY)
    iWbemLevel1Login.RemRelease()
    WQL = r"""SELECT * FROM Win32_TerminalServiceSetting"""
    iEnumWbemClassObject = iWbemServices.ExecQuery(WQL)
    iWbemClassObject = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
    if int(isenable)==1:
        iWbemClassObject.SetAllowTSConnections(1, 1) #Enable RDP
    else:
        iWbemClassObject.SetAllowTSConnections(0, 0)  # Disable RDP

    iEnumWbemClassObject = iWbemServices.ExecQuery(WQL)
    iWbemClassObject = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
    result = dict(iWbemClassObject.getProperties())
    if result['AllowTSConnections']['value']==1:
        print("[+] Enable RDP Open Sucess")
    elif result['AllowTSConnections']['value']==0:
        print("[+] Disable RDP Sucess")
    iWbemServices.RemRelease()

    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    StdRegProv, resp = iWbemServices.GetObject("StdRegProv")
    rdpport=StdRegProv.GetDWORDValue(2147483650,"SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp","PortNumber")
    print("[*] RDP Port:{}".format(rdpport.uValue))
    dcom.disconnect()


def rdpshadow(ip='', username='', password='',domain='',hashes='',aesKey='',shadow=0):
    idnumber=[-1,0,1,2,3,4]
    if shadow not in idnumber:
        print("[-] Shadow ID:0 or 1 or 2 or 3 or 4")
        exit()
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    StdRegProv, resp = iWbemServices.GetObject("StdRegProv")
    if shadow==-1:
        deleteshadow=StdRegProv.DeleteValue(2147483650, "Software\\Policies\\Microsoft\\Windows NT\\Terminal Services","Shadow")
        if deleteshadow.ReturnValue==0:
            print("[+] Delete Shadow reg key Sucess")
    else:
        shadowid = StdRegProv.SetDWORDValue(2147483650, "Software\\Policies\\Microsoft\\Windows NT\\Terminal Services","Shadow",shadow)
        print("[*] Set RDP Shdaow ID:{}".format(shadow))
        if shadowid.ReturnValue==0:
            print("[+] Set RDP Shadow ID Sucess")
        else:
            print("[-] Set RDP Shadow ID Failure")
    dcom.disconnect()

def Login_with_empty_password(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    print("[*] Login with empty password Setting")
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    StdRegProv, resp = iWbemServices.GetObject("StdRegProv")
    if isenable==0:
        txt="Enable Login with empty password"
        limitblankpassworduse = StdRegProv.SetDWORDValue(2147483650, "SYSTEM\\CurrentControlSet\\Control\\Lsa", "limitblankpassworduse",0)
    else:
        txt="Disable Login with empty password"
        limitblankpassworduse = StdRegProv.SetDWORDValue(2147483650, "SYSTEM\\CurrentControlSet\\Control\\Lsa","limitblankpassworduse", 1)

    if limitblankpassworduse.ReturnValue==0:
        print("[+] {} Sucess".format(txt))
    else:
        print("[-] {} Failure".format(txt))
    dcom.disconnect()
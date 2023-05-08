from module import *
from module import wmiconnect
from module import printReply
def userquery(ip='', username='', password='',domain='',hashes='',aesKey=''):
    print("[*] UserAccount")
    dcom,iWbemLevel1Login=wmiconnect.wmiconnect(ip,username,password,domain,hashes,aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin("//./root/cimv2", NULL, NULL)
    iWbemLevel1Login.RemRelease()
    win32UserAccount, _ = iWbemServices.GetObject("Win32_UserAccount")
    UserAccount = iWbemServices.ExecQuery("SELECT * from Win32_UserAccount")
    userlist=printReply.printReply(UserAccount)
    user_splist = userlist.split("\n")
    for user in range(0, len(user_splist)):
        try:
           print(user_splist[user])

        except Exception as error:
            pass

    dcom.disconnect()

def user_rid_query(ip='', username='', password='',domain='',hashes='',aesKey=''):
    print("[*] User RID Query")
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    iWbemLevel1Login.RemRelease()
    win32UserAccount, _ = iWbemServices.GetObject("Win32_UserAccount")
    iEnumWbemClassObject = iWbemServices.ExecQuery("SELECT * from Win32_UserAccount")
    while True:
        try:
            Userinfo = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
            Domain = Userinfo.Domain
            Name = Userinfo.Name
            Disabled = Userinfo.Disabled
            rid = hex(int(Userinfo.SID.split("-")[-1])).lstrip("0x")
            print("Domain:{} Name:{} Disabled:{} Rid:{}".format(Domain,Name,Disabled,rid))
        except Exception as err:
            if str(err).find("WBEM_S_FALSE") > 0:
                break
    dcom.disconnect()


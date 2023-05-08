from module import *
from module import wmiconnect

def Firewall_setting(ip='', username='', password='',domain='',hashes='',aesKey='',arg=""):
    if arg[0:5] != "query" and arg != "start" and arg != "stop":
        print("[-] Pluse Query Help,Thanks....")
        exit()


    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    try:
        iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/StandardCimv2', NULL, NULL)
    except Exception as error:
        if "WBEM_E_INVALID_NAMESPACE" in str(error):
            print(
                "[*] The OS possible:Windows7/Windows Server 2008,Not Found //./root/StandardCimv2 NameSpace\nUnable to configure firewall rules")
            dcom.disconnect()
            exit()
    WQL="SELECT * FROM MSFT_NetFirewallProfile"
    if "query"==arg:
        firewall_list=iWbemServices.ExecQuery(WQL)
        while True:
            try:
                pEnum = firewall_list.Next(0xffffffff, 1)[0]
                InstanceID=pEnum.InstanceID
                Name=pEnum.Name
                EnableID=pEnum.Enabled
                if int(EnableID)==1 or int(EnableID)==2:
                    status="ON"
                else:
                    status="OFF"
                print("InstanceID:{} Name:{} EnableID:{}".format(InstanceID,Name,status))
            except Exception as error:
                if "WBEM_S_FALSE" in str(error):
                    break
    elif "stop"==arg or "start"==arg:
        print("[*] {} Firewall".format(arg))
        if arg=="start":
            status=2
        elif arg=="stop":
            status=0
        user=input("Firewall Name:")
        WQL+=" where Name=\"{}\"".format(user)
        iEnumWbemClassObject = iWbemServices.ExecQuery(WQL)
        firewall_ProfileClass = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
        record = firewall_ProfileClass.getProperties()
        record = dict(record)
        firewall_ProfileInstance = firewall_ProfileClass.SpawnInstance()
        firewall_ProfileInstance.DisabledInterfaceAliases = ""
        firewall_ProfileInstance.Caption = "" if record['Caption']['value'] == None else record['Caption']['value']
        firewall_ProfileInstance.Enabled = status
        firewall_ProfileInstance.Description = "" if record['Caption']['value'] == None else record['Caption']['value']
        iWbemServices.PutInstance(firewall_ProfileInstance.marshalMe())
    dcom.disconnect()
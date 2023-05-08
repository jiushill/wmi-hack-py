from module import *
from module import wmiconnect

def winrm_enable(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    if int(isenable)!=1 and int(isenable)!=0:
        print("[-] Pluse Query Help,Thanks....")
        exit()
    print("[*] Enable/Disable winrm")
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    WQL = 'select * from Win32_Service where Name="WinRM"'
    iEnumWbemClassObject = iWbemServices.ExecQuery(WQL)
    iWbemClassObject = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
    if int(isenable)==1:
        if iWbemClassObject.StartService().ReturnValue==0 or iWbemClassObject.StartService().ReturnValue==10:
            print("[+] winrm Service Start")
    elif int(isenable)==0:
        stopcode=iWbemClassObject.StopService().ReturnValue
        print("[*] WinRm Stop Service Return Code:{}".format(stopcode))
        if stopcode==0 or stopcode==5:
            print("[+] winrm Service Stop")


    if int(isenable) == 1:
        print("[*] Enable Winrm Service")
        InstanceIDlist=["WINRM-HTTP-In-TCP","WINRM-HTTP-In-TCP-PUBLIC"]
        try:
            iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/StandardCimv2', NULL, NULL)
        except Exception as error:
            if "WBEM_E_INVALID_NAMESPACE" in str(error):
                iWbemServices=None

        if iWbemServices!=None:
            for InstanceIDName in InstanceIDlist:
                try:
                    WQL2 = "SELECT * FROM MSFT_NetProtocolPortFilter where InstanceID = \"{}\"".format(InstanceIDName)
                    firewall_list = iWbemServices.ExecQuery(WQL2)
                    while True:
                            pEnum = firewall_list.Next(0xffffffff, 1)[0]
                            InstanceID = pEnum.InstanceID
                            print("[*] Enable Firewall Rule InstanceID:{}".format(InstanceID))
                            MSFT_NetProtocolPortFilter = iWbemServices.ExecQuery(
                                "select * from MSFT_NetFirewallRule where InstanceID=\"{}\"".format(InstanceID)).Next(0xffffffff, 1)[0]
                            result = dict(MSFT_NetProtocolPortFilter.getProperties())
                            Enabled = MSFT_NetProtocolPortFilter.Enabled
                            if Enabled == 2:
                                firewall_Instance = MSFT_NetProtocolPortFilter.SpawnInstance()
                                firewall_Instance.Enabled = 1
                                firewall_Instance.CreationClassName = "fuckyouaasasasaasas"
                                firewall_Instance.PolicyRuleName = ""
                                firewall_Instance.SystemCreationClassName = ""
                                firewall_Instance.SystemName = ""
                                # allow=2, allowBypass=3, Block=4
                                firewall_Instance.Action = 2
                                firewall_Instance.Caption = ""
                                firewall_Instance.CommonName = ""
                                firewall_Instance.ConditionListType = 3
                                firewall_Instance.Description = ""
                                firewall_Instance.Direction = 1
                                firewall_Instance.DisplayGroup = ""
                                firewall_Instance.DisplayName = "AAAAAAAAAAAAAAA"
                                firewall_Instance.EdgeTraversalPolicy = 0
                                firewall_Instance.ElementName = "                 "
                                firewall_Instance.EnforcementStatus = [0]
                                firewall_Instance.ExecutionStrategy = 2
                                firewall_Instance.LocalOnlyMapping = False
                                firewall_Instance.LooseSourceMapping = False
                                firewall_Instance.Mandatory = ""
                                firewall_Instance.Owner = ""
                                firewall_Instance.PolicyDecisionStrategy = 2
                                firewall_Instance.PolicyKeywords = ""
                                firewall_Instance.PolicyRoles = ""
                                firewall_Instance.PolicyStoreSource = "PersistentStore"
                                firewall_Instance.PolicyStoreSourceType = 1
                                firewall_Instance.PrimaryStatus = 1
                                firewall_Instance.Profiles = 0
                                firewall_Instance.RuleGroup = ""
                                firewall_Instance.RuleUsage = ""
                                firewall_Instance.SequencedActions = 3
                                firewall_Instance.Status = "The rule was parsed successfully from the store."
                                firewall_Instance.StatusCode = 65536
                                iWbemServices.PutInstance(firewall_Instance.marshalMe())
                except Exception as error:
                    if "WBEM_S_FALSE" in str(error):
                         break
                    else:
                        print(error)
                        exit(1)
                print("[+] Enable WinRm Firewall allow Rule ok")
        else:
            print("[*] The OS possible:Windows7/Windows Server 2008,Not Found //./root/StandardCimv2 NameSpace\nUnable to configure firewall rules")
    dcom.disconnect()
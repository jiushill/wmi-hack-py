from module import *
from module import wmiconnect
import colorama

def FirewallRule_setting(ip='', username='', password='',domain='',hashes='',aesKey='',arg=""):
    if arg[0:5]!="query" and arg!="enable" and arg!="disable" and arg!="delete":
        print("[-] Pluse Query Help,Thanks....")
        exit()

    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    try:
        iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/StandardCimv2', NULL, NULL)
    except Exception as error:
        if "WBEM_E_INVALID_NAMESPACE" in str(error):
            print("[*] The OS possible:Windows7/Windows Server 2008,Not Found //./root/StandardCimv2 NameSpace\nUnable to configure firewall rules")
            dcom.disconnect()
            exit()
    if arg == "query1": #查启用
        wql="select * from MSFT_NetFirewallRule where Enabled=1"
        print("[*] Select Enable Firewall Rule")
    if arg == "query2": #查禁用
        wql="select * from MSFT_NetFirewallRule where Enabled=2"
        print("[*] Select Disable Firewall Rule")
    if arg == "query": #查全部
        wql="select * from MSFT_NetFirewallRule"
        print("[*] Select all Firewall Rule")
    if arg=="querya": #查入站
        wql="select * from MSFT_NetFirewallRule where Direction=1"
        print("[*] Select inbound Firewall Rule")
    elif arg=="queryb": #查出站
        wql="select * from MSFT_NetFirewallRule where Direction=2"
        print("[*] Select outbound Firewall Rule")
    elif arg=="query1a": #查启用的入站
        wql = "select * from MSFT_NetFirewallRule where Direction=1 and Enabled=1"
        print("[*] Select Enable inbound Firewall Rule")
    elif arg=="query2a": #查禁用的入站
        wql = "select * from MSFT_NetFirewallRule where Direction=1 and Enabled=2"
        print("[*] Select Disable inbound Firewall Rule")
    elif arg=="query1b": #查启用的出站
        wql = "select * from MSFT_NetFirewallRule where Direction=2 and Enabled=1"
        print("[*] Select Enable outbound Firewall Rule")
    elif arg=="query2b": #查禁用的出站
        wql = "select * from MSFT_NetFirewallRule where Direction=2 and Enabled=2"
        print("[*] Select Disable outbound Firewall Rule")
    elif arg=="query3": #特定ID查询
        user=input("InstanceID:")
        wql="select * from MSFT_NetFirewallRule where InstanceID=\"{}\"".format(user)
        print("[*] Select InstanceID Query")


    wql2 = "select * from MSFT_NetFirewallRule where InstanceID="
    if "query" in arg:
        MSFT_NetFirewallRule = iWbemServices.ExecQuery(wql)
        while True:
            try:
                pEnum = MSFT_NetFirewallRule.Next(0xffffffff, 1)[0]
                action=int(pEnum.Action)
                Description=pEnum.Description
                DisplayName=pEnum.DisplayName
                ElementName=pEnum.ElementName
                InstanceID=pEnum.InstanceID
                Enabled=int(pEnum.Enabled)
                if action==4:
                    type_="block connection"
                elif action==2:
                    type_="allow connection"
                if Enabled==1:
                    color=colorama.Fore.GREEN
                    enable_status=True
                else:
                    color=colorama.Fore.RED
                    enable_status=False
                MSFT_NetProtocolPortFilter=iWbemServices.ExecQuery("select * from MSFT_NetProtocolPortFilter where InstanceID=\"{}\"".format(InstanceID)).Next(0xffffffff, 1)[0]
                MSFT_NetProtocolPortFilter_LocalPort=MSFT_NetProtocolPortFilter.LocalPort
                MSFT_NetProtocolPortFilter_RemotePort=MSFT_NetProtocolPortFilter.RemotePort
                MSFT_NetProtocolPortFilter_Protocol=MSFT_NetProtocolPortFilter.Protocol
                output=color+"Type:{} {} {} {} InstanceID:{} Enable:{} || Protocol:{} LocalPort:{} RemotePort:{}".format(type_,Description,DisplayName,ElementName,InstanceID,enable_status,MSFT_NetProtocolPortFilter_Protocol,MSFT_NetProtocolPortFilter_LocalPort,MSFT_NetProtocolPortFilter_RemotePort)+colorama.Style.RESET_ALL
                print(output)
            except Exception as error:
                if "WBEM_S_FALSE" in str(error):
                    break
                else:
                    pass
    elif arg=="disable" or arg=="enable": #禁用防火墙某条规则
        print("[*] {} FirewallRule".format(arg))
        InstanceID=input("Input {} InstanceID:".format(arg))
        if arg=="disable":
            status=2
        elif arg=="enable":
            status=1
        wql2+='"{}"'.format(InstanceID)
        print(wql2)
        # 不能直接调用Disable方法，无法调用成功。只能强制覆盖
        '''
        disable = iWbemServices.ExecQuery(wql2)
        pEnum = disable.Next(0xffffffff, 1)[0]
        print(pEnum.Disable)
        '''
        try:
            iEnumWbemClassObject = iWbemServices.ExecQuery(wql2)
            firewall_RuleClass = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
            # firewall_RuleClass.Enable
            record = firewall_RuleClass.getProperties()
            record = dict(record)
            firewall_Instance = firewall_RuleClass.SpawnInstance()
            firewall_Instance.Enabled = status
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
            print(iWbemServices.PutInstance(firewall_Instance.marshalMe()))
        except Exception as error:
            if str(error).find("S_FALSE")>0:
                print("[-] Not Found InstanceID:{} Firewall a Roule".format(InstanceID))

    elif arg=="delete":
        ID=input("Delete Firewall InstanceID:")
        try:
            iEnumWbemClassObject = iWbemServices.ExecQuery("SELECT * FROM MSFT_NetFirewallRule where InstanceID = \"%s\"" % ID)
            firewall_RuleClass = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
            record = dict(firewall_RuleClass.getProperties())
            print(iWbemServices.DeleteInstance('MSFT_NetFirewallRule.CreationClassName="{}",PolicyRuleName="{}",SystemCreationClassName="{}",SystemName="{}"'.format(record['CreationClassName']['value'],record['PolicyRuleName']['value'],record['SystemCreationClassName']['value'],record['SystemName']['value'])))
        except Exception as error:
            if str(error).find("S_FALSE")>0:
                print("[-] Not Found InstanceID:{} Firewall a Roule".format(ID))
    dcom.disconnect()
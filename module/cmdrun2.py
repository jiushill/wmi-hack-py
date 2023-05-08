from module import *
from module import wmiconnect
from module import checkError
from module import vbsrun
import os
import uuid
import time
import re
import base64

def execcmd(ip, username, password, domain, hashes, aesKey,cmd,types="",current_path=""):
    print("[*] vbs schtasks run command")
    uid=str(uuid.uuid1())
    uid2=str(uuid.uuid1())
    print("[*] ouput command to file:C:\\Windows\\Temp\\{}.txt".format(uid))
    format_vbs=os.path.join(os.getcwd(),"vbs","exec2_command.vbs")
    if types=="fake_shell":
        tmpdata = open(format_vbs, "r",encoding="utf-8").read()
        cmd_format = r'''Action.arguments = chr(34) & "/c cd /d PATH_REPLACE&AAAAAAAAAAAA >> C:\Windows\Temp\BBBBBBBBBBB 2>C:\Windows\Temp\DDDDDDDDDDer_.txt&echo [S] >> C:\Windows\Temp\BBBBBBBBBBB&cd >> C:\Windows\Temp\BBBBBBBBBBB&echo [E] >> C:\Windows\Temp\BBBBBBBBBBB" & chr(34) '''
        th = re.search("Action.arguments = .*", tmpdata)
        tmp = tmpdata.replace(th.group(), cmd_format.replace("PATH_REPLACE","\" & Base64Decode(\"{}\") & \"".format(base64.b64encode(current_path.encode()).decode())).replace("AAAAAAAAAAAA","\" & Base64Decode(\"{}\") & \"".format(base64.b64encode(cmd.encode()).decode())).replace("BBBBBBBBBBB",uid+".txt").replace("CCCCCCCCCCCCC",uid).replace("DDDDDDDDDD",uid)).replace("BBBBBBBBBBB",uid+".txt").replace("CCCCCCCCCCCCC",uid).replace("DDDDDDDDDD",uid)
    else:
        tmp=open(format_vbs,"r",encoding="utf-8").read().replace("AAAAAAAAAAAA",cmd).replace("BBBBBBBBBBB",uid+".txt").replace("CCCCCCCCCCCCC",uid).replace("DDDDDDDDDD",uid)
    exec_vbs_path = os.path.join(os.getcwd(), "output", "exec2_command.vbs")
    outputvbs=open(exec_vbs_path,"w",encoding="utf-8")
    outputvbs.write(tmp)
    outputvbs.close()
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey,exec_vbs_path,uid2)
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
   # iWbemLevel1Login.RemRelease()
    iWbemServices2 = iWbemLevel1Login.NTLMLogin('//./root/subscription', NULL, NULL)

    while True:
        try:
            readscript, _ = iWbemServices2.GetObject('ActiveScriptEventConsumer.Name="{}"'.format(uid))
            break
        except Exception as error:
            if "WBEM_E_NOT_FOUND" in str(error):
                pass
            else:
                print(error)
    cmdoutput = readscript.ScriptText

    if len(cmdoutput) > 0:
        try:
            decodetext = base64.b64decode(cmdoutput).decode("utf-8")
        except:
            print("[-] utf-8 decode Failure")
            decodetext = base64.b64decode(cmdoutput).replace(b"\x00", b"")
    else:
        decodetext = ""
    #  dcom.disconnect()
    print("------------------------------------------------Result------------------------------------------------")
    print(decodetext)
    vbsrun.delete(ip, username, password, domain, hashes, aesKey,uid2)
    dele_output_vbs_path = os.path.join(os.getcwd(), "output", "dele_file.vbs")
    tmp2 = open(os.path.join(os.getcwd(), "vbs", "dele_file.vbs"), "r", encoding="utf-8").read().replace("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "C:\\Windows\\Temp\\{}".format(uid+".txt")).replace("DDDDDDDDDD",uid)
    open(dele_output_vbs_path, "w", encoding="utf-8")
    print(tmp2, file=open(dele_output_vbs_path, "a", encoding="utf-8"))
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, dele_output_vbs_path)
    #延时等待命令执行结果输出的文件全部删除
    #time.sleep(2.5)
    vbsrun.delete(ip, username, password, domain, hashes, aesKey, "Example")
    return decodetext
from module import *
from module import wmiconnect
from module import vbsrun
import uuid
import base64
import os

def ls(ip='', username='', password='',domain='',hashes='',aesKey='',targetpath=''):
    vbs_teample_path=os.path.join(os.getcwd(),"vbs","listdir.vbs")
    output_vbs_path=os.path.join(os.getcwd(),"output","listdir.vbs")
    uid=str(uuid.uuid1())
    vbsid=str(uuid.uuid1())
    temp=open(vbs_teample_path,"r",encoding="utf-8").read().replace("AAAAAAAAAAAAAAAAAAAA",base64.b64encode(targetpath.encode()).decode()).replace("BBBBBBBBBBBBBBBBBBBBBBB",uid)
    newfile = open(output_vbs_path, "w", encoding="utf-8")
    newfile.write(temp)
    newfile.close()
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, output_vbs_path, vbsid)
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemLevel1Login.RemRelease()
    iWbemServices2 = iWbemLevel1Login.NTLMLogin('//./root/subscription', NULL, NULL)
    # while死循环判断vbs不用写文件判断，爽
    while True:
        try:
            readscript, _ = iWbemServices2.GetObject('ActiveScriptEventConsumer.Name="{}"'.format(uid))
            break
        except Exception as error:
            if "WBEM_E_NOT_FOUND" in str(error):
                pass
            else:
                print(error)
    fileodata = base64.b64decode(readscript.ScriptText).decode()
    print("==============================={}===============================".format(targetpath))
    print(fileodata)
    vbsrun.delete(ip, username, password, domain, hashes, aesKey,vbsid)
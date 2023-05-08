from module import *
from module import wmiconnect
from module import printReply
import time
def getProcessList(ip='', username='', password='',domain='',hashes='',aesKey='',query=False):
    print("[*] Get Process List")
    result_echoformat=""
    dcom,iWbemLevel1Login=wmiconnect.wmiconnect(ip,username,password,domain,hashes,aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin("//./root/cimv2", NULL, NULL)
    iWbemLevel1Login.RemRelease()
    win32Process, _ = iWbemServices.GetObject("Win32_Process")
    ProcessList = iWbemServices.ExecQuery("SELECT * from Win32_Process")
    process_result = printReply.printReply(ProcessList)
    split_process_result=process_result.split("\n")
    for process in range(1,len(process_result)):
        try:
            fg_process=split_process_result[process].split("|")
            processname=fg_process[1].lstrip().rstrip()
            create_process_time=time.strftime("%Y-%m-%d-%H:%M:%S",time.strptime(fg_process[9].split(".")[0].lstrip().rstrip(),"%Y%m%d%H%M%S"))
            processpid=fg_process[10].lstrip().rstrip()
            commandline=fg_process[-2].lstrip().rstrip()
            echoformat="{} {} {} {}".format(processname,processpid,commandline,create_process_time)
            result_echoformat+=echoformat+"\r\n"
            print(echoformat)

        except Exception as error:
            pass

    if query == True:
        print("========================================TASKLIST QUERY====================================================")
        print()
        from module import check
        check.process_check(result_echoformat)
    dcom.disconnect()
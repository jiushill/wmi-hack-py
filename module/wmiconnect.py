from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dcom.wmi import IWbemServices
from impacket.dcerpc.v5.dcomrt import DCOMConnection
from impacket.dcerpc.v5.dtypes import NULL
from impacket.structure import Structure
from impacket.smbconnection import SMBConnection, SMB_DIALECT, SMB2_DIALECT_002, SMB2_DIALECT_21
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_PKT_PRIVACY
import logging
import sys

def wmiconnect(ip='', username='', password='',domain='',hashes='',aesKey=''):
    if hashes!=None and len(hashes) > 0:
        lmhash, nthash = hashes.split(':')
    else:
        lmhash, nthash = ("", "")

    result=""
  #  smbConnection = SMBConnection(ip, ip)
    try:
        dcom = DCOMConnection(ip, username, password, domain, lmhash, nthash, aesKey, oxidResolver=True,doKerberos=False, kdcHost=None)
        iInterface = dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login, wmi.IID_IWbemLevel1Login)
        iWbemLevel1Login = wmi.IWbemLevel1Login(iInterface)
        return (dcom,iWbemLevel1Login)

    except  (Exception, KeyboardInterrupt) as e:
        if logging.getLogger().level == logging.DEBUG:
            import traceback
            traceback.print_exc()
        logging.error(str(e))
       # if smbConnection is not None:
       #     smbConnection.logoff()
        dcom.disconnect()
        sys.stdout.flush()
        sys.exit(1)

    dcom.disconnect()
    sys.exit(1)
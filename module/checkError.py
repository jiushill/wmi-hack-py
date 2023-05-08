from module import *
import logging
def checkError(banner, resp):
    call_status = resp.GetCallStatus(0) & 0xffffffff  # interpret as unsigned
    if call_status != 0:
        from impacket.dcerpc.v5.dcom.wmi import WBEMSTATUS
        try:
            error_name = WBEMSTATUS.enumItems(call_status).name
        except ValueError:
            error_name = 'Unknown'
        logging.error('%s - ERROR: %s (0x%08x)' % (banner, error_name, call_status))
    else:
        logging.info('%s - OK' % banner)

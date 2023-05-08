from module import *
import sys
import logging
from io import StringIO
def printReply(iEnum):
    current=sys.stdout
    sys.stdout = StringIO()
    printHeader = True
    while True:
        try:
            pEnum = iEnum.Next(0xffffffff, 1)[0]
            record = pEnum.getProperties()
            if printHeader is True:
                print('|', end=' ')
                for col in record:
                    print('%s |' % col, end=' ')
                print()
                printHeader = False
            print('|', end=' ')
            for key in record:
                if type(record[key]['value']) is list:
                    for item in record[key]['value']:
                        print(item, end=' ')
                    print(' |', end=' ')
                else:
                    print('%s |' % record[key]['value'], end=' ')
            print()
        except Exception as e:
            if logging.getLogger().level == logging.DEBUG:
                import traceback
                traceback.print_exc()
                sys.exit(1)
            if str(e).find('S_FALSE') < 0:
                raise
            else:
                break

    result=sys.stdout.getvalue()
    sys.stdout = current
    return result
    iEnum.RemRelease()
    sys.stdout=current
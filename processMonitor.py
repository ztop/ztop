"""
Per-Process 5 days Mon 2/10/14 Fri 2/14/14 18

28 CPU/Memory/Network stats 1 wk Mon 2/10/14 Fri 2/14/14 backend

29 Port Information 1 wk Mon 2/10/14 Fri 2/14/14 backend

30 File Info/Statistics 1 wk Mon 2/10/14 Fri 2/14/14 backend
"""

import psutil
#from ztop import memoize
from memoize import memoize

class PerProcess:
    #@memoize(ttl=3)
    def collect(self, pid):
        try:
            pid.dict = pid.as_dict(['username', 'nice', 'name', 'status'])
        except psutil.NoSuchProcess:
            pass

if __name__ == "__main__":
    import time
    from pprint import pprint
    per = PerProcess()
    while True:
        procs = []
        for p in psutil.process_iter():
            per.collect(p)
            procs.append(p)

        pprint( procs )
        time.sleep(1)
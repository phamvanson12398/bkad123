
import subprocess as sub
import time
import json
import logging
import os
import sys
PATH_CORE = os.environ.get('pathcore')
sys.path.insert(0, PATH_CORE+"libraries")
from watchdog import * 




if __name__ == '__main__':
	wd = WatchDog()
	while 1:
		wd.check()
		time.sleep(5)

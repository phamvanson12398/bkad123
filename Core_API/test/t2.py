import time
import os
import threading

def test():
	print ("start thread")
	time.sleep(10)
	print ("end thread")

def test2():
	print ("1")
	thread = threading.Thread(target=test)
	thread.start()
	print ("2")
	return 0

print (test2())

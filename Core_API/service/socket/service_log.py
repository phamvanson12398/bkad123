import socketio
import psutil
import requests
import json
import os

import time





def readfile(fn, fr, ofset):
	f=open(fn,"r+")
	f.seek(fr,0)
	data=f.read()
	f.close()
	return (data)

while  1:
	try:
		sio = socketio.Client()

		sio.connect('http://localhost:6600',namespaces=['/'])

		my_watcher = {}


		while 1:
			# update info 
			r = requests.post(url = "http://localhost:3000/api/monitoring/service_logs")
			print("update data!")
			service_logs = json.loads(r.text)["data"]
			for i in range(5):
				for sl in service_logs:
					if sl["watched"] == 1:
						size = os.path.getsize(sl["directory"])
						if sl["id"] not in my_watcher:
							my_watcher[sl["id"]] = size
							continue
						elif  size <= my_watcher[sl["id"]] :
							my_watcher[sl["id"]] = size
						else:
							print("\t-",sl["directory"],"---","new log!" )
							from_byte = my_watcher[sl["id"]]
							ofset = size - from_byte
							newdata =  readfile(sl["directory"], from_byte, ofset)
							my_watcher[sl["id"]] = size
							sio.emit('echo_watch_service_log' , {"data":newdata,"id":sl["id"]}  , namespace='/')

			time.sleep(1)
	except:
		time.sleep(1)
		



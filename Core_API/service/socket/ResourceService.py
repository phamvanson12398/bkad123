import socketio

# standard Python
from clickhouse_driver import Client
import psutil
import requests
import json
import time


def CHConnect():
	return Client(host='localhost',port=9000, password='123', database='bvg')

while 1:
	try:
		sio = socketio.Client()
		sio.connect('http://localhost:6600',namespaces=['/'])


		for i in range(1000000):
			cpu = psutil.cpu_percent(interval=1)
			mem = psutil.cpu_percent(interval=1)
			sio.emit('echo_resource', {
			"resource": {
				"time":int(time.time()),
				"cpu": cpu,
				"ram" :mem
			}
		}, namespace='/')
			data = {
		            "cpu": cpu,
		            "disk": 0,
		            "ram": mem
			}


			a = requests.post('http://127.0.0.1:3000/api/monitoring/system_resources', 
				data =json.dumps(data),headers={'CONTENT_TYPE': 'application/json'})
			conn = CHConnect()
			conn.execute( 
		    	'INSERT INTO bvg.system_resource (cpu,disk,ram) VALUES ',
		    	[data] )


			print (i,a)
	except:
		time.sleep(1)



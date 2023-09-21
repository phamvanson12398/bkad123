import socketio
import psutil
# standard Python
from clickhouse_driver import Client
import json
import requests
import time


def CHConnect():
	return Client(host='localhost',port=9000, password='123', database='bvg')

def push_traffic(inpu,output,interface):
	data = {
            "input": inpu,
            "interface": interface,
            "output": output
		}
	a = requests.post('http://127.0.0.1:3000/api/monitoring/traffic_resources', 
		data =json.dumps(data),headers={'CONTENT_TYPE': 'application/json'})

	conn = CHConnect()
	conn.execute( 
    	'INSERT INTO bvg.traffic_resource (input,interface,output) VALUES ',
    	[data] )



	return a
while 1 :
	try:
		sio = socketio.Client()
		sio.connect('http://127.0.0.1:6600',namespaces=['/'])

		last_tp = {}
		list_card = ["eno1","eno2", "enp1s0f0", "enp1s0f1"]
		while True :

			t_now = int(time.time())
			tp = psutil.net_io_counters(pernic=True)
			new_tp   = {}
			result = {}
			for  i in list_card:
				if i in tp:
					new_tp[i] = {"in": tp[i].bytes_recv , "out":tp[i].bytes_sent}
				else:
					result[i] = {
						"time" :t_now,
						"input" :0,
						"output" : 0
					}
					continue
				if i in last_tp:
					result[i] = {
						"time" :t_now,
						"input" :new_tp[i]["in"] - last_tp[i]["in"] ,
						"output" : new_tp[i]["out"] - last_tp[i]["out"]
					}
					push_traffic(result[i]["input"],result[i]["output"],i)
					# print ()

				else:
					result[i] = {
						"time" :t_now,
						"input" :0,
						"output" : 0
					}
					continue

			last_tp = new_tp

			sio.emit('echo_throughput', {"throughput":result}  , namespace='/')
			time.sleep(1)

	except Exception as exp:
		raise (exp)
		time.sleep(1)










# sio.emit('echo_resource', {'foo': 'bar'})



from aiohttp import web
import socketio
import shlex
import time
import os
import subprocess
import socket
import telnetlib
sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)
import requests
import json

mydict= {}
mydict["resource"] = []
mydict["throughput"] = []
mydict["vpn_status"] = []
mydict["notify"] = []
service_log = {
			1 : [],
			2 : [],
			3 : [],
			4 : [],
			5 : [],
			6 : [],
			7 : [],
			8 : [],
			9 : []
			# 10 : [],
			# 11 : [],
			# 12 : []
			}
async def index(request):
	"""Serve the client-side application."""
	with open('index.html') as f:
		return web.Response(text=f.read(), content_type='text/html')

@sio.event
def connect(sid, environ):
	print("connect ", sid)

@sio.event
def join_resource(sid,message):
	mydict["resource"].append(sid)
	print ("enter room",mydict["resource"])

@sio.event
async def echo_resource(sid,message):
	# print("Echooooooooo")
	for i in mydict["resource"] :
		await sio.emit('resource', message, room=i)



@sio.event
def join_throughput(sid,message):
	mydict["throughput"].append(sid)
	print ("enter room",mydict["throughput"])

@sio.event
async def echo_throughput(sid,message):
	print("Echooooooooo throughput")
	for i in mydict["throughput"] :
		await sio.emit('throughput', message, room=i)



# Notify 
@sio.event
def join_notify(sid,message):
	mydict["notify"].append(sid)
	print ("enter room",mydict["notify"])

@sio.event
async def echo_notify(sid,message):
	print("Echooooooooo notify")
	for i in mydict["notify"] :
		await sio.emit('s_notify', message, room=i)






@sio.event
async def echo_vpn_status(sid,message):
	print("Echooooooooo vpn status")
	for i in mydict["vpn_status"] :
		await sio.emit('vpn_status', message, room=i)




@sio.event
async def s_ping(sid,json):
	process = subprocess.Popen(shlex.split("ping %s -w 30" % json["ip"]), stdout=subprocess.PIPE)
	timeout = time.time() + 30
	while time.time() < timeout:
		output = process.stdout.readline()
		if output == '' and process.poll() is not None:
			break
		if output:
			await sio.emit('s_ping', {'data': output.strip().decode() },room=sid)
	rc = process.poll()

@sio.event
async def s_tracert(sid,json):
	process = subprocess.Popen(shlex.split("traceroute %s" % json["ip"]), stdout=subprocess.PIPE)
	timeout = time.time() + 30
	while time.time() < timeout:
		output = process.stdout.readline()
		if output == '' and process.poll() is not None:
			break
		if output:
			await sio.emit('s_tracert', {'data': output.strip().decode() },room=sid)
	rc = process.poll()
	

@sio.event
async def s_telnet(sid,json):
	process = subprocess.Popen(shlex.split("nmap -p %s %s" % (json["port"],json["ip"])), stdout=subprocess.PIPE)
	timeout = time.time() + 30
	while time.time() < timeout:
		output = process.stdout.readline()
		if output == '' and process.poll() is not None:
			break
		if output:
			await sio.emit('s_telnet', {'data': output.strip().decode() },room=sid)
	rc = process.poll()


@sio.event
def disconnect(sid):
	print('disconnect ', sid)
	if sid in mydict["throughput"]:
		mydict["throughput"].remove(sid)
	if sid in mydict["resource"]:
		mydict["resource"].remove(sid)


@sio.event
def leave_service_log(sid):
	try:
		for i in service_log:
			if sid in service_log[i]:
				service_log[i].remove(sid)
	except:
		pass


@sio.event
async def echo_watch_service_log(sid,message):
	print ("echo ",message)
	for i in service_log[message["id"]] :
		await sio.emit('watch_service_log', {"data":message["data"]}, room=i)

@sio.event
async def watch_service_log(sid,message):
	if message["id"] not in service_log:
		service_log[message["id"]] = []
	service_log[message["id"]].append(sid)

	print ("enter room service_log",service_log[message["id"]])

	url = "http://localhost:3000/monitoring/service_logs/%d" % message["id"] 

	# r = requests.put(url,data=json.dumps({'watched':1}))
	# print (r,url)







if __name__ == '__main__':
	web.run_app(app,host='0.0.0.0',port=6600)

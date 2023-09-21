import os
import sys
import re
import json
import time
import datetime
import calendar

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import or_

from libraries.statuscode import *
from libraries.general import *
from sqlalchemy import or_
from pyroute2 import IPRoute
import netifaces

from model.model import ConnectDB
from model.service_model import (NetworkInterface, Network, GroupNetwork, 
	GroupNetworkHaveNetwork)

PPP_PATH = "/etc/ppp"

class InterfaceCore():

	def __init__(self):
		self.Session = ConnectDB()
		self.ipr = IPRoute()

	def init_interface(self):
		try:
			session = self.Session()
			system_interfaces = session.query(NetworkInterface).\
				filter(NetworkInterface.is_virtual == 0).all()
			_int = netifaces.interfaces()
			print ("--------------------------------------\n")
			print (_int)
			temp_int = session.query(NetworkInterface).all()
			for interface in temp_int:
				print (interface.__dict__['name'])
				if interface.__dict__['name'] not in _int:
					print ("DELETE: ", interface.__dict__['name'])
					test = session.query(NetworkInterface).\
						filter(NetworkInterface.name == interface.__dict__['name'])
					print (test.first().__dict__)
					test.delete()
			temp_int = session.query(NetworkInterface).all()
			system_interface_names = []
			for system_interface_name in system_interfaces:
				system_interface_names.append(system_interface_name.__dict__['name'])

			interface_name = netifaces.interfaces()
			for name in interface_name:
				if name not in system_interface_names:
					if "1000" not in name:
						if name not in temp_int:
							try:
								add = netifaces.ifaddresses(name)[netifaces.AF_INET][0]['addr']
								mask = netifaces.ifaddresses(name)[netifaces.AF_INET][0]['netmask']
							except:
								pass
							interface = NetworkInterface(
								name = name,
								ip_address = add,
								netmask = mask,
								status = 1,
								type = "VPN"
							)
							session.add(interface)
						else:
							try:
								add = netifaces.ifaddresses(name)[netifaces.AF_INET][0]['addr']
								mask = netifaces.ifaddresses(name)[netifaces.AF_INET][0]['netmask']
							except:
								pass
							interface = NetworkInterface(
								name = name,
								ip_address = add,
								netmask = mask,
								status = 1,
								type = "VPN"
							)
							session.query(NetworkInterface).\
								filter(NetworkInterface.name == name).update({
									'ip_address': add,
									'netmask': mask
								})
					else:
						add = netifaces.ifaddresses(name)[netifaces.AF_INET][0]['addr']
						mask = netifaces.ifaddresses(name)[netifaces.AF_INET][0]['netmask']
						gw = netifaces.ifaddresses(name)[netifaces.AF_INET][0]['peer']
						_name = name.split("ppp1000")[1]
						session.query(NetworkInterface).\
							filter(NetworkInterface.id == _name).update({
								'ip_address': add,
								'netmask': mask,
								'gateway': gw
							})
			try:
				session.commit()
			except Exception as exp:
				raise (exp)
				session.rollback()
				return False
		except Exception as exp:
			pass
			# return False
		finally:
			session.close()


	def set_interface(self):
		try:
			print ("SET INTERFACE")
			session = self.Session()
			interfaces = session.query(NetworkInterface).\
				filter(NetworkInterface.type != "VPN").all()
			
			for i in range(len(interfaces)):
				interfaces[i] = General.standardizedData(interfaces[i])

			conf_int = open('/etc/netplan/50-cloud-init.yaml', 'w')
			def_int = open('/etc/netplan/def')
			try:
				default_data = def_int.readlines()
				for data in default_data:
					conf_int.write(data)
				conf_int.write("network:\n  version: 2\n  ethernets:")
				for interface in interfaces:
					if interface['addressing_mode'] == 'PPPoE':
						# os.mkdir(f"{PPP_PATH}/peers/dsl_{interface['isp_name']}")
						fp_pppoe_conf = open(f"{PPP_PATH}/peers/"\
							f"dsl_{interface['isp_name']}_{interface['id']}", "w")
						fp_pppoe_def_config = open(f"{PPP_PATH}/peers/def_pppoe")
						dt_pppoe_def_config = fp_pppoe_def_config.read()
						dt_pppoe_def_config = dt_pppoe_def_config.replace(
							"$INT$", 
							interface['name']
						)
						dt_pppoe_def_config = dt_pppoe_def_config.replace(
							"$USER$", 
							interface['username']
						)
						dt_pppoe_def_config = dt_pppoe_def_config.replace(
							"$UNIT$", 
							f"1000{interface['id']}"
						)
						fp_pppoe_conf.write(dt_pppoe_def_config)
						fp_pppoe_conf.close()
						fp_pppoe_def_config.close()

						fp_pppoe_userpass = open(f"{PPP_PATH}/pppoe_acc")
						dt_pppoe_userpass = fp_pppoe_userpass.read()
						userpass = f"\"{interface['username']}\" * \"{interface['password']}\""
						if userpass not in dt_pppoe_userpass:
							dt_pppoe_userpass += f"\n{userpass}"
						fp_pppoe_userpass.close()
						fp_pppoe_userpass = open(f"{PPP_PATH}/pppoe_acc", "w")
						fp_pppoe_userpass.write(dt_pppoe_userpass)
						fp_pppoe_userpass.close()

						fp_server_chapsc = open(f"{PPP_PATH}/server_chapsc")
						dt_server_chapsc = fp_server_chapsc.read()
						fp_client_chapsc = open(f"{PPP_PATH}/client_chapsc")
						dt_client_chapsc = fp_client_chapsc.read()
						fp_server_chapsc.close()
						fp_client_chapsc.close()

						fp_chapsc = open(f"{PPP_PATH}/chap-secrets", "w")
						fp_chapsc.write(dt_server_chapsc)
						fp_chapsc.write("\n###CLIENT DATA###\n")
						fp_chapsc.write(dt_client_chapsc)
						fp_chapsc.write("\n###PPPoE DATA###\n")
						fp_chapsc.write(dt_pppoe_userpass)
						fp_chapsc.close()
						fp_papsc = open(f"{PPP_PATH}/pap-secrets")
						dt_papsc = fp_papsc.read()
						fp_papsc.close()
						fp_papsc = open(f"{PPP_PATH}/pap-secrets", "a")
						if userpass not in dt_papsc:
							fp_papsc.write(f"\n{userpass}")

						#Clone MAC address
						os.system(f"macchanger -m {interface['clone_mac']} {interface['name']}")

						os.system(f"poff dsl_{interface['isp_name']}_{interface['id']}")
						os.system("ifconfig {} down".format(interface['name']))
						if interface['status'] == 1:
							os.system("ifconfig {} up".format(interface['name']))
							os.system(f"pon dsl_{interface['isp_name']}_{interface['id']}")
							while True:
								interface_name = netifaces.interfaces()
								start = time.time()
								end = time.time()
								if end - start > 30: #Timeout 30s for config PPPoE
									os.system(f"poff dsl_{interface['isp_name']}_{interface['id']}")
									os.system("ifconfig {} down".format(interface['name']))
									return False
								if f"ppp1000{interface['id']}" in interface_name:
									name = f"ppp1000{interface['id']}"
									time.sleep(5) #Delay 5s for Interface get IP Address
									InterfaceCore.init_interface(self)
									try:
										session.commit()
									except Exception as exp:
										raise (exp)
										session.rollback()
										return False
									break
						else:
							session.query(NetworkInterface.id).\
								filter(NetworkInterface.id == interface['id']).update({
									'ip_address': "",
									'netmask': "",
									"gateway": ""
								})
							try:
								session.commit()
							except:
								session.rollback()
								pass
							finally:
								session.close()
					else:
						if interface['status'] == 1:
							conf_int.write(gen_int(interface['name'],
								interface['ip_address'],
								interface['netmask'],
								interface['gateway'],
								interface['addressing_mode']
							))
							os.system("ifconfig {} up".format(interface['name']))
						else:
							os.system("ifconfig {} down".format(interface['name']))

				conf_int.close()
				def_int.close()
				os.system("netplan apply")
			except Exception as exp:
				raise (exp)
				
		except Exception as exp:
			raise (exp)
			return False
		finally:
			session.close()

def getIntData():
	try:
		session = ConnectDB()()
		ipr = IPRoute()
		_int = []
		for link in ipr.get_links():
			_int.append(link.get_attr('IFLA_IFNAME'))
		interfaces = session.query(NetworkInterface).\
			filter(NetworkInterface.addressing_mode == "PPPoE").all()
		for i in range(len(interfaces)):
			interfaces[i] = General.standardizedData(interfaces[i])
		return interfaces, _int
	except Exception as exp:
		print (exp)
		return False
	finally:
		session.close()

def gen_int(name, add, netmask, gw, mode):
	print ("FLAG0")
	address = add + "/" + netmask2cidr(netmask)
	if mode == "Static":
		if gw == "":
			return "\n    {}:\n      addresses: [{}]\n      dhcp4: no\n      nameservers:\n        addresses: [8.8.8.8, 8.8.4.4]\n      optional: true".\
			format(name, address, gw)
		else:
			return "\n    {}:\n      addresses: [{}]\n      gateway4: {}\n      dhcp4: no\n      nameservers:\n        addresses: [8.8.8.8, 8.8.4.4]\n      optional: true".\
			format(name, address, gw)
	elif mode == "dhcp":
		print ("FLAG2")
		return "\n    {}:\n      dhcp4: true\n      optional: true".format(name)
	else:
		print ("FLAG3")
		return ""
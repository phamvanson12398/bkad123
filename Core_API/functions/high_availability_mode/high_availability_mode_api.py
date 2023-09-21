import datetime
import pathlib

from models.models import ConnectToDB, Config_HA, Virtual_Interface
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class HA_Mode_API(Resource):

	def get(self):
		return [{"mode_id":1, "mode_name":"active-active"}, {"mode_id":2, "mode_name":"active-passive"}, {"mode_id":3, "mode_name":"standalone"}]


class HA_API(Resource):

	def get(self):
		try: 
			session = Session()
			config_ha = editConfig(standardizedData(session.query(Config_HA).\
										filter(Config_HA.id == 1).one()))
			virtual_interface = session.query(Virtual_Interface).all()
			for i in range(len(virtual_interface)):
				virtual_interface[i] = standardizedData(virtual_interface[i])
			config_ha['virtual_interface'] = virtual_interface
			return config_ha
			
		except Exception as exp:
			print (exp)
			return status_code_400("")
		finally:
			session.close()
	
	def put(self):
		try:
			session = Session()
			data = request.get_json()
			data = editInput(data)
			session.query(Config_HA).\
				filter(Config_HA.id == 1).update(data['config'])
			try:
				if 'virtual_interface' in data:
					for i in range(len(data['virtual_interface'])):
						name = data['virtual_interface'][i]['interface_name']
						data1 = data['virtual_interface'][i]
						session.query(Virtual_Interface).filter(Virtual_Interface.interface_name == name).update(data1)
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("HIGH AVAILABILITY CONFIG SUCCESS", "")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()




def editConfig(config_ha):
	config_ha['config'] = {}	
	config_ha["config"]["device_priority"] = config_ha["device_priority"]
	config_ha["config"]["group_name"] = config_ha["group_name"]
	config_ha["config"]["group_password"] = config_ha["group_password"]
	config_ha["config"]["heartbeat_interfaces"] = config_ha["heartbeat_interfaces"]
	config_ha["config"]["heartbeat_netmask"] = config_ha["heartbeat_netmask"]
	config_ha["config"]["heartbeat_network"] = config_ha["heartbeat_network"]
	config_ha["config"]["operation_mode"] = config_ha["operation_mode"]
	del config_ha["device_priority"], config_ha["group_name"]
	del config_ha["group_password"], config_ha["heartbeat_interfaces"]
	del config_ha["heartbeat_netmask"], config_ha["heartbeat_network"]
	del config_ha["operation_mode"], config_ha["id"]
	return config_ha

def editInput(inputA):
	data = {}
	data['config'] = {}
	if 'config' in inputA:
		for i in inputA['config']:
			data['config'][i] = inputA['config'][i]
	if "high_availability_status" in inputA:
		data['config']["high_availability_status"] = inputA['high_availability_status']
	if 'virtual_interface' in inputA:
		data['virtual_interface'] = inputA['virtual_interface']
	return data
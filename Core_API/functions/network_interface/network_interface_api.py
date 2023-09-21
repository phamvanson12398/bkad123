import datetime
import pathlib

from models.models import ConnectToDB, NetworkInterface
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class InterfacesCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, NetworkInterface.__table__.columns, NetworkInterface
			)
			query = session.query(NetworkInterface)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in NetworkInterface.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				records[i] = standardizedData(records[i])
				records[i] = after_data(records[i])
			return status_code_200("", get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()

	def post(self): # tam tam
		try:
			session = Session()
			data = request.get_json()
			if data['type'] == 'LAN'  or data['type'] == 'WAN':
				interface = NetworkInterface(
					name = check_data(data, "name"),
					type = check_data(data, "type"),
					ip_address = check_data(data, "ip_address"),
					addressing_mode = check_data(data, "addressing_mode"),
					netmask = check_data(data, "netmask"),
					gateway = check_data(data, "gateway"),
					status = check_data(data, "status"),
					created_at = str(datetime.datetime.now()),
					updated_at = str(datetime.datetime.now()),
					ispname = check_data(data, "ispname"),
					username = check_data(data, "username"),
					password = check_data(data, "password"),
					mtu = check_data(data, "mtu"),
					fixed_ip = check_data(data, "fixed_ip"),
					clone_mac = check_data(data, "clone_mac")
				)
				session.add(interface)
				try:
					session.commit()
				except Exception as exp:
					print (exp)
					session.rollback()
					return status_code_500("database error 1")
				return status_code_200("Add Interfaces Success!", "")
			else:
				return status_code_400("verify error")
		except Exception as exp:
			raise (exp)
			return status_code_500("database error")
		finally:
			session.close()

class InterfacesAPI(Resource):

	def get(self, interface_id):
		try:
			session = Session()
			record = session.query(NetworkInterface).filter_by(id = interface_id).one()
			print(record)
			record = standardizedData(record)
			record = after_data(record)
			
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, interface_id): # tam tam
		try:
			session = Session()
			data = request.get_json()
			print(data)

			data['updated_at']= str(datetime.datetime.now())
			
			session.query(NetworkInterface).filter(NetworkInterface.id == interface_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("database error")
			return status_code_200("Edit Interface Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("database error")
		finally:
			session.close()

	def delete(self, interface_id):
		try:
			session = Session()
			# session.query(NetworkInterface).filter(NetworkInterface.id == interface_id).delete()
			data = {
				"type":None,
				"ip_address" : None,
				"addressing_mode" :None,
				"netmask" :None,
				"gateway" :None,
				"status" :None,
				"created_at": None,
				"updated_at": None,
				"ispname" :None,
				"username" :None,
				"password": None,
				"mtu": None,
				"fixed_ip" :None,
				"clone_mac": None
			}
			session.query(NetworkInterface).filter(NetworkInterface.id == interface_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("database error")
			return status_code_200("Delete Interface Success!", "")
		except Exception as exp: 
			return status_code_500(exp)
		finally:
			session.close()

def after_data(data):
	if not data['addressing_mode'] == 'PPPoE':
		del data['ispname'], data['username'], data['password'], data['mtu'], data['fixed_ip'], data['clone_mac']
		if data['addressing_mode'] == 'DHCP':
			del data['netmask'], data['gateway'], data['ip_address']
	else:
		data['pppoe'] = {'ispname':data['ispname'], 'username':data['username'], 
		'password':data['password'], 'mtu':data['mtu'], 'fixed_ip':data['fixed_ip'], 'clone_mac': data['clone_mac']}
		del data['ispname'], data['username'], data['password'], data['mtu'], data['fixed_ip'], data['clone_mac']
	return data

def check_data(data, name):
	if name in data:
		return data[name]
	else:
		return None

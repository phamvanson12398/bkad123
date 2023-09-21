import datetime
import pathlib

from sqlalchemy import or_
from flask import request
from flask_restful import Resource

from models.models import ConnectToDB, NetworkNat,NetworkInterface
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from .network_nat_core import NetworkNatCore

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()
NatCore = NetworkNatCore()

class NatCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, NetworkNat.__table__.columns, NetworkNat
			)
			query = session.query(NetworkNat)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in NetworkNat.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				member = []
				interface = records[i].network_interface
				interface = standardizedData(
					interface, None, {'id': 'id', 'name': 'name'}
				)
				records[i] = standardizedData(records[i], ["network_interface"])
				records[i]['interface'] = interface
			return status_code_200("", get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def post(self):
		try:
			session = Session()
			data = request.get_json()
			# protocol = ",".join(proto for proto in data['protocol'])
			networknat = NetworkNat(
				name = data['name'],
				protocol = data["protocol"],
				type = data['type'],
				ip_address = data['ip_address'],
				service = data['service'],
				ip_map = data['ip_map'],
				port_map = data['port_map'],
				status = data['status'],
				interface = data['interface']
			)
			# for interface_id in data['interface']:
			# 	try:
			# interface = session.query(NetworkInterface).filter_by(id = int(data['interface'])).one()
			# print (interface.__dict__)
				# except Exception as exp:
				# 	print(exp)
				# 	return status_code_400('code 400')
			# networknat.interface.append(interface)
			session.add(networknat)
			try:
				session.commit()
				# if NatCore.add_nat_rule() is False:
				# 	session.rollback()
				# 	return status_code_500("")
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("code 200","")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()

class NatAPI(Resource):

	def get(self, nat_id):
		try: 
			session = Session()
			group_interface = session.query(NetworkNat).\
				filter(NetworkNat.id == nat_id).one()
			interface = group_interface.network_interface
			interface = standardizedData(
				interface, None, {'id': 'id', 'name': 'name'}
			)
			group_interface = standardizedData(group_interface, ["network_interface"])
			group_interface['interface'] = interface
			# for interface in group_interface.interface:
			# 	interface = standardizedData(
			# 		interface, None, {'id': 'id', 'name': 'name'})
			# 	member.append(interface)
			# group_interface = standardizedData(group_interface)
			# group_interface['interface'] = member
			return status_code_200('', group_interface)
		except Exception as exp:
			print (exp)
			return status_code_400("")
		finally:
			session.close()
	
	def put(self, nat_id):
		try:
			session = Session()
			data = request.get_json()
			if 'protocol' in data:
				data['protocol'] = str(data['protocol'])
			session.query(NetworkNat).\
				filter(NetworkNat.id == nat_id).update(data)
			try:
				session.commit()
				if NatCore.add_nat_rule() is False:
					session.rollback()
					return status_code_500("")
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("Update Nat Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()

	def delete(self, nat_id):
		try:
			session = Session()
			session.query(NetworkNat).\
				filter(NetworkNat.id == nat_id).delete()
			try:
				session.commit()
				if NatCore.add_nat_rule() is False:
					session.rollback()
					return status_code_500("")
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("Delete Nat Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()



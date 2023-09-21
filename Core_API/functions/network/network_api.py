from sqlalchemy import or_

from models.models import ConnectToDB, Network
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class NetworkCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, Network.__table__.columns, Network
			)
			query = session.query(Network)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in Network.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				records[i] = standardizedData(records[i])			
			return status_code_200("", get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def post(self):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			network = Network(
				name = data['name'],
				ip_address = data['ip_address'],
				netmask = data['netmask'],
				description = data['description']
			)
			session.add(network)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add Network Success!","")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def options(self):
		try:
			data = {
				'name': {
					'default': None,
					'placeholder': 'Name',
					'required': True,
					'type': 'String'
				},
				'ip_address': {
					'default': None,
					'placeholder': 'IP Address',
					'required': True,
					'type': 'String'
				},
				'description': {
					'default': None,
					'placeholder': "Description",
					'required': True,
					'type': 'String'
				}
			}
			return status_code_200("", data)
		except Exception as exp:
			print (f"Error in [OPTIONS] network_api!: {exp}")
			return status_code_500("Error!")

class NetworkAPI(Resource):

	def get(self, network_id):
		try:
			session = Session()
			record = session.query(Network).filter_by(id = network_id).one()
			record = standardizedData(record)			
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, network_id):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			session.query(Network).filter(Network.id == network_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit Network Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, network_id):
		try:
			session = Session()
			session.query(Network).filter(Network.id == network_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete Network Success!", "")
		except Exception as exp: 
			return status_code_500(exp)
		finally:
			session.close()

def verify_input(data):
	try:
		str_error = ""

		return str_error
	except Exception as exp:
		print (exp)
		return False
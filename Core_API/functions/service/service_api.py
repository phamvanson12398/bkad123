from sqlalchemy import or_

from models.models import ConnectToDB, Service
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class ServiceCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, Service.__table__.columns, Service
			)
			query = session.query(Service)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in Service.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				records[i] = standardizedData(records[i])
				records[i]['protocol'] = records[i]['protocol'].split(",")
				records[i]['port'] = records[i]['port'].split(",")
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
			data['port'] = ",".join(i for i in data['port'])
			data['protocol'] = ",".join(i for i in data['protocol'])
			service = Service(
				name = data['name'],
				port = data['port'],
				protocol = data['protocol'],
				description = data['description']
			)
			session.add(service)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add Service Success!","")
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
				'port': {
					'default': None,
					'placeholder': 'Ports',
					'required': True,
					'type': 'String'
				},
				'protocol': {
					'default': None,
					'placeholder': 'Protocols',
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
			print (f"Error in [OPTIONS] Service_api!: {exp}")
			return status_code_500("Error!")

class ServiceAPI(Resource):

	def get(self, service_id):
		try:
			session = Session()
			record = session.query(Service).filter_by(id = service_id).one()
			record = standardizedData(record)
			record['protocol'] = record['protocol'].split(",")
			record['port'] = record['port'].split(",")
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, service_id):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			if "protocol" in data:
				data['protocol'] = ",".join(i for i in data['protocol'])
			if "port" in data:
				data['port'] = ",".join(i for i in data['port'])
			session.query(Service).filter(Service.id == service_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit Service Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, Service_id):
		try:
			session = Session()
			session.query(Service).filter(Service.id == Service_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete Service Success!", "")
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
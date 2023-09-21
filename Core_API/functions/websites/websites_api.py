import time
import pathlib

from models.models import ConnectToDB, Websites
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class WebsitesCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, Websites.__table__.columns, Websites
			)
			query = session.query(Websites)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in Websites.__table__.columns))
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
			data = request.get_json()
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			temp_name= str(time.time())
			if "key" in request.files :
				f = request.files['key']
				fn = "key_%s.key" %temp_name
				f.save(UPLOAD_FOLDER +fn)
				data["key"] = readfile(UPLOAD_FOLDER + fn)
			if "cert" in request.files :
				f = request.files['cert']
				fn = "cert_%s.crt" %temp_name
				f.save(UPLOAD_FOLDER +fn)
				data["cert"] = readfile(UPLOAD_FOLDER + fn)

			website = Websites(
				domain = data['domain'],
				ip_address = data['ip_address'],
				port = data['port'],
				listen_port = data['port'],
				ssl = data['ssl'],
				cache = data['cache'],
				key = data['key'],
				cert = data['cert'],
				status = 1
			)
			session.add(website)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add Website Success!","")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def options(self):
		try:
			data = {
				'domain': {
					'default': None,
					'placeholder': 'Domain',
					'required': True,
					'type': 'String'
				},
				'ip_address': {
					'default': None,
					'placeholder': 'IP Address',
					'required': True,
					'type': 'String'
				},
				'port': {
					'default': None,
					'placeholder': 'Port',
					'required': True,
					'type': 'String'
				},
				'listen_port': {
					'default': None,
					'placeholder': 'Listen Port',
					'required': True,
					'type': 'String'
				},
				'cache': {
					'default': 0,
					'allowed': [0, 1],
					'placeholder': None,
					'required': True,
					'type': 'Number'
				},
				'ssl': {
					'default': 1,
					'allowed': [0, 1],
					'placeholder': None,
					'required': True,
					'type': 'Number'
				},
				'key': {
					'default': None,
					'placeholder': 'Click here to browse file',
					'required': True,
					'type': 'File'
				},
				'cert': {
					'default': None,
					'placeholder': 'Click here to browse file',
					'required': True,
					'type': 'File'
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


class WebsitesAPI(Resource):

	def get(self, website_id):
		try:
			session = Session()
			record = session.query(Websites).filter_by(id = website_id).one()
			record = standardizedData(record)
			del record['key']
			del record['cert']
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, website_id):
		try:
			session = Session()
			data = request.get_json()
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			temp_name= str(time.time())
			if "key" in request.files :
				f = request.files['key']
				fn = "key_%s.key" %temp_name
				f.save(UPLOAD_FOLDER +fn)
				data["key"] = readfile(UPLOAD_FOLDER + fn)
			if "cert" in request.files :
				f = request.files['cert']
				fn = "cert_%s.crt" %temp_name
				f.save(UPLOAD_FOLDER +fn)
				data["cert"] = readfile(UPLOAD_FOLDER + fn)
			if False and check_null(data) is False :
				return status_code_400("Request Data Error!")
			session.query(Websites).filter(Websites.id == website_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit Website Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, website_id):
		try:
			session = Session()
			session.query(Websites).filter(Websites.id == website_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete Website Success!", "")
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
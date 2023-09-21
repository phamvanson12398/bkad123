import datetime
import pathlib

from models.models import ConnectToDB, ACSH
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class ACSHCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, ACSH.__table__.columns, ACSH
			)
			query = session.query(ACSH)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in ACSH.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				records[i] = standardizedData(records[i])
			return status_code_200("", get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()

	def post(self):
		try:
			session = Session()
			data = request.get_json()
			acsh = ACSH(
				address = data['address'],
				domain = data['domain'],
				service_status = data['service_status'],
				status = data['status'],
				port = data['port'],
				description = data['description']
			)
			session.add(acsh)
			try:
				session.commit()
			except Exception as exp:
				raise (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("code 200","")
		except Exception as exp:
			raise (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()	



class ACSHAPI(Resource):

	def get(self, acsh_id):
		try:
			session = Session()
			record = session.query(ACSH).filter_by(id = acsh_id).one()
			record = standardizedData(record)
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()
	
	def put(self, acsh_id):
		try:
			session = Session()
			data = request.get_json()
			session.query(ACSH).\
				filter(ACSH.id == acsh_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("Update ACSH Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()

	def delete(self, acsh_id):
		try:
			session = Session()
			session.query(ACSH).\
				filter(ACSH.id == acsh_id).delete()
			try:
				session.commit()
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("Delete ACSH Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()



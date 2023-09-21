import datetime
import pathlib

from models.models import ConnectToDB, Routes
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class RoutesCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, Routes.__table__.columns, Routes
			)
			query = session.query(Routes)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in Routes.__table__.columns))
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
			routes = Routes(
				created_at = str(datetime.datetime.now()),
				description = data['description'],
				destination = data['destination'],
				gateway = data['gateway'],
				metric = data['metric'],
				name = data['name'],
				netmask = data['netmask'],
				status = data['status'],
				updated_at = str(datetime.datetime.now())
			)
			session.add(routes)
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



class RoutesAPI(Resource):

	def get(self, routes_id):
		try:
			session = Session()
			record = session.query(Routes).filter_by(id = routes_id).one()
			record = standardizedData(record)
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()
	
	def put(self, routes_id):
		try:
			session = Session()
			data = request.get_json()
			data['updated_at']= str(datetime.datetime.now())
			session.query(Routes).\
				filter(Routes.id == routes_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("Update routes Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()

	def delete(self, routes_id):
		try:
			session = Session()
			session.query(Routes).\
				filter(Routes.id == routes_id).delete()
			try:
				session.commit()
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("Delete routes Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()



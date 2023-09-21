import datetime
import pathlib

from models.models import ConnectToDB, AccessControlList
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class AccessControlListCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, AccessControlList.__table__.columns, AccessControlList
			)
			query = session.query(AccessControlList)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in AccessControlList.__table__.columns))
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
			accesscontrollist = AccessControlList(
				address = data['address'],
				type = data['type'],
				description = data['description'],
				status = data['status']
			)
			session.add(accesscontrollist)
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



class AccessControlListAPI(Resource):

	def get(self, acl_id):
		try:
			session = Session()
			record = session.query(AccessControlList).filter_by(id = acl_id).one()
			record = standardizedData(record)
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()
	
	def put(self, acl_id):
		try:
			session = Session()
			data = request.get_json()
			session.query(AccessControlList).\
				filter(AccessControlList.id == acl_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("Update ACL Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()

	def delete(self, acl_id):
		try:
			session = Session()
			session.query(AccessControlList).\
				filter(AccessControlList.id == acl_id).delete()
			try:
				session.commit()
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("Delete ACL Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()



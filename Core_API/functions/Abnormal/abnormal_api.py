from sqlalchemy import or_

from models.models import ConnectToDB, Abnormal
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class AbnormalCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, Abnormal.__table__.columns, Abnormal
			)
			query = session.query(Abnormal)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in Abnormal.__table__.columns))
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


class AbnormalAPI(Resource):

	def get(self, abnormal_id):
		try:
			session = Session()
			record = session.query(Abnormal).filter_by(id = abnormal_id).one()
			record = standardizedData(record)			
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, abnormal_id):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			session.query(Abnormal).filter(Abnormal.id == abnormal_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit Abnormal Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

def verify_input(data):
	try:
		str_error = ""
		for param in data:
			if param != "status":
				str_error += "Request Data Error!"
		return str_error
	except Exception as exp:
		print (exp)
		return False
from sqlalchemy import or_

from models.models import ConnectToDB, LearningMode
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class LearningModeCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, LearningMode.__table__.columns, LearningMode
			)
			query = session.query(LearningMode)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in LearningMode.__table__.columns))
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
			learning_mode = LearningMode(
				name = data['name'],
				learning_time = data['learning_time'],
				iteration = data['iteration'],
				learning_type = data['learning_type']
			)
			session.add(learning_mode)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add Learning Mode Success!","")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

class LearningModeAPI(Resource):

	def get(self, learning_mode_id):
		try:
			session = Session()
			record = session.query(LearningMode).filter_by(id = learning_mode_id).one()
			record = standardizedData(record)			
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, learning_mode_id):
		try:
			session = Session()
			if learning_mode_id == 0:
				return status_code_400("You can't edit this record!")
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			session.query(LearningMode).filter(LearningMode.id == learning_mode_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit Learning Mode Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, learning_mode_id):
		try:
			session = Session()
			if learning_mode_id == 0:
				return status_code_400("You can't delete this record!")
			session.query(LearningMode).filter(LearningMode.id == learning_mode_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete Learning Mode Success!", "")
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
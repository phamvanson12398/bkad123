from sqlalchemy import or_

from models.models import ConnectToDB, Signature
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class SignatureCollectionAPI(Resource):

	def get(self,profile_id):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, Signature.__table__.columns, Signature
			)
			query = session.query(Signature).filter_by(ad_profile=profile_id)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in Signature.__table__.columns))
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


class SignatureAPI(Resource):

	def get(self,profile_id, signature_id):
		try:
			session = Session()
			record = session.query(Signature).filter_by(id = signature_id).one()
			record = standardizedData(record)			
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self,profile_id, signature_id):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			session.query(Signature).filter(Signature.id == signature_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit Signature Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

def verify_input(data):
	try:
		str_error = ""
		for param in data:
			print (param)
			if param != "status":
				str_error += "Request Data Error!"
		return str_error
	except Exception as exp:
		print (exp)
		return False
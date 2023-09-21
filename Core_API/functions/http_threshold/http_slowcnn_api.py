from sqlalchemy import or_

from models.models import ConnectToDB, HttpSlowConnection
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class HttpSlowConnectionCollectionAPI(Resource):

	def get(self,profile_id):
		try:
			session = Session()
			parameters = request.args
			
			print ("PROFILE ID = ", profile_id)
			limit, page, offset, order = getDefault(
				parameters, HttpSlowConnection.__table__.columns, HttpSlowConnection
			)
			query = session.query(HttpSlowConnection).filter(HttpSlowConnection.profile == profile_id)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in HttpSlowConnection.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				records[i] = standardizedData(records[i])
				records[i]['data'] = records[i]['data'].split(",")
				if records[i]['input_type'] == "check_box" or records[i]['input_type'] == "combo_box":
					records[i]['member'] = []
					records[i]['member_name'] = records[i]['member_name'].split(",")
					records[i]['member_value'] = records[i]['member_value'].split(",")
					for j in range(len(records[i]['member_name'])):
						records[i]['member'].append({
							'name': records[i]['member_name'][j],
							'value': records[i]['member_value'][j]
						})
				del records[i]['member_name']
				del records[i]['member_value']
			return status_code_200("", get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()
	def post(self,profile_id):
		try:
			session = Session()
			parameters = request.args
			
			data = request.json
			data['profile'] = profile_id
			
			http_slowcnn = HttpSlowConnection(
				name = data['name'],
				description = data['description'],
				status = data['status'],
				input_type = data["input_type"],
				input_id = data["input_id"],
				profile=data["profile"],
				data=data["data"],
				member_name = data["member_name"],
				member_value = data["member_value"]


			)
			session.add(http_slowcnn)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add HTTP url Threshold Success!","")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()


class HttpSlowConnectionAPI(Resource):

	def get(self, profile_id,http_slowcnn_id):
		try:
			session = Session()
			parameters = request.args
			
			record = session.query(HttpSlowConnection).filter(HttpSlowConnection.profile == profile_id).filter_by(id = http_slowcnn_id).one()
			record = standardizedData(record)
			record['data'] = record['data'].split(",")
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self,profile_id, http_slowcnn_id):
		try:
			session = Session()
			parameters = request.args
			
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			if "data" in data:
				data['data'] = ','.join(i for i in data['data'])
			session.query(HttpSlowConnection).filter(HttpSlowConnection.profile == profile_id).filter(HttpSlowConnection.id == http_slowcnn_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Config Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

def verify_input(data):
	try:
		str_error = ""
		for key in data:
			if key not in ["data", "status"]:
				str_error += "Request data error!"
				break
		return str_error
	except Exception as exp:
		print (exp)
		return False
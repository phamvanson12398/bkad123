import datetime
from dateutil.relativedelta import *
from sqlalchemy import or_

from models.models import ConnectToDB, ATAS, LearningMode
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *
from datetime import date
from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class ATASCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, ATAS.__table__.columns, ATAS
			)
			query = session.query(ATAS)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in ATAS.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				learning_mode = records[i].learn_mode
				profile = records[i].ad_profile
				learning_mode = {
					'id': learning_mode.id,
					'name': learning_mode.name,
					'learning_time': learning_mode.learning_time,
					'iteration': learning_mode.iteration,
					'learning_type': learning_mode.learning_type
				}
				profile = {
					'id': profile.id,
					'name': profile.name
				}
				records[i] = standardizedData(records[i],["learn_mode", "ad_profile"])			
				records[i]['learning_mode'] = learning_mode
				records[i]['profile'] = profile
			return status_code_200("", get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()

	# def post(self):
	# 	try:
	# 		session = Session()
	# 		data = request.json
	# 		error = verify_input(data)
	# 		if error != "" or error is False:
	# 			return status_code_400("Request Data Error!")
	# 		ad_profile = ATAS(
	# 			name = data['name'],
	# 			learning_mode = data['learning_mode'],
	# 			start_date = data['start_date'],
	# 			end_date = data['end_date'],
	# 			start_time = data['start_time'],
	# 			description = data['description'],
	# 			apply = data['apply']
	# 		)
	# 		session.add(ad_profile)
	# 		try:
	# 			session.commit()
	# 		except Exception as exp:
	# 			print (exp)
	# 			session.rollback()
	# 			return status_code_500("")
	# 		return status_code_200("Add ATAS Success!","")
	# 	except Exception as exp:
	# 		print (exp)
	# 		return status_code_500("")
	# 	finally:
	# 		session.close()

class ATASAPI(Resource):

	def get(self, atas_id):
		try:
			session = Session()
			record = session.query(ATAS).filter_by(id = atas_id).one()
			learning_mode = record.learn_mode
			profile = record.ad_profile
			learning_mode = {
				'id': learning_mode.id,
				'name': learning_mode.name,
				'learning_time': learning_mode.learning_time,
				'iteration': learning_mode.iteration,
				'learning_type': learning_mode.learning_type
			}
			profile = {
				'id': profile.id,
				'name': profile.name
			}
			record = standardizedData(record,["learn_mode", "ad_profile"])			
			record['learning_mode'] = learning_mode
			record['profile'] = profile
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, atas_id):
		try:
			session = Session()
			parameters = request.args
			data = {}

			if "action" in parameters and parameters["action"] in ["apply_now","stop_now","re_learn", "start_now"]:
				if parameters['action'] == "start_now":
					today = datetime.datetime.now()
					data['progress'] = "Starting"
					data["start_date"] = today.strftime("%Y-%m-%d")
					data["start_time"] = today.strftime("%H:%M:%S")
					data["status"] = 1
				elif parameters['action'] == "stop_now":
					data['progress'] = ""
					data["status"] = 2
				elif parameters['action'] == "re_learn":
					data['progress'] = ""
					data["status"] = 0
				else:       # apply_now
					data['progress'] = "Applied"
					data["status"] = 3
			else:
				data = request.json		
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			# if check_null(data) is False:
			# 	return status_code_400("Request Data Error!")
			
			
			if "start_time" not in data:
				data['start_time'] = "00:00:00"
			if "start_date" in data and "start_time" in data:
				start = data['start_date'] + " " + data['start_time']
				start_date = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
				session = Session()
				if "learning_mode" in data:
					lmode_id = data['learning_mode']
				else:
					lmode_id = session.query(ATAS).\
						filter(ATAS.id == atas_id).first().learning_mode
				learning_mode = session.query(LearningMode).\
					filter(LearningMode.id == lmode_id).first()
				if learning_mode.learning_type == "days":
					ltype = 1
					ltime = ltype * learning_mode.learning_time * learning_mode.iteration
					end_date = start_date + datetime.timedelta(days=ltime)
				elif learning_mode.learning_type == "weeks":
					ltype = 7
					ltime = ltype * learning_mode.learning_time * learning_mode.iteration
					end_date = start_date + datetime.timedelta(days=ltime)
				else:
					ltime = learning_mode.learning_time * learning_mode.iteration
					end_date = start_date + relativedelta(months=+ltime)
				
				data['end_date'] = end_date

			session.query(ATAS).filter(ATAS.id == atas_id).update(data)
			try:
				session.commit()	
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			record = session.query(ATAS).filter(ATAS.id == atas_id).first()
			learning_mode = record.learn_mode
			profile = record.ad_profile
			learning_mode = {
				'id': learning_mode.id,
				'name': learning_mode.name,
				'learning_time': learning_mode.learning_time,
				'iteration': learning_mode.iteration,
				'learning_type': learning_mode.learning_type
			}
			profile = {
				'id': profile.id,
				'name': profile.name
			}
			record = standardizedData(record,["learn_mode", "ad_profile"])			
			record['learning_mode'] = learning_mode
			record['profile'] = profile
			return status_code_200("Edit ATAS Success!", record)
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, atas_id):
		try:
			session = Session()
			session.query(ATAS).filter(ATAS.id == atas_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete ATAS Success!", "")
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
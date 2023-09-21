import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy import or_

from models.models import ConnectToDB, ADProfile, ATAS, TcpGeneral, TcpGeneralDef, TcpSlowConnection, TcpSlowConnectionDef
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

Session = ConnectToDB()

class ADProfileCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, ADProfile.__table__.columns, ADProfile
			)
			query = session.query(ADProfile)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in ADProfile.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				flag = 0
				if records[i].atas is not None and records[i].atas.status == 1:
					flag = 1
				records[i] = standardizedData(records[i])
				records[i]['atas'] = 0
				if flag == 1:
					records[i]['atas'] = 1				
			return status_code_200("", get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def post(self):
		try:
			session = Session()
			current_time = datetime.datetime.now()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			ad_profile = ADProfile(
				name = data['name'],
				mode = data['mode'],
				description = data['description']
			)
			session.add(ad_profile)
			try:
				session.commit()
				atas = ATAS(
					name = data['name'],
					learning_mode = 0,
					start_time = current_time,
					start_date = current_time,
					end_date = current_time,
					apply = 1,
					status = 0,
					progress = "Not yet started",
					profile = ad_profile.id
				)
				session.add(atas)
				session.commit()
				tcp_general_def = session.query(TcpGeneralDef).all()
				tcp_slowcnn_def = session.query(TcpSlowConnectionDef).all()
				for config_line in tcp_general_def:
					config_line = standardizedData(config_line)
					config_line['profile'] = ad_profile.id
					tcp_general = TcpGeneral(
						name = config_line['name'],
						description = config_line['description'],
						data = config_line['data'],
						status = config_line['status'],
						input_type = config_line['input_type'],
						input_id = config_line['input_id'],
						member_name = config_line['member_name'],
						member_value = config_line['member_value'],
						profile = config_line['profile']
					)
					session.add(tcp_general)
				for config_line in tcp_slowcnn_def:
					config_line = standardizedData(config_line)
					config_line['profile'] = ad_profile.id
					tcp_slowcnn = TcpSlowConnection(
						name=config_line['name'],
						description=config_line['description'],
						data=config_line['data'],
						status=config_line['status'],
						input_type=config_line['input_type'],
						input_id=config_line['input_id'],
						member_name=config_line['member_name'],
						member_value=config_line['member_value'],
						profile=config_line['profile']
					)
					session.add(tcp_slowcnn)
				session.commit()
			except Exception as exp:
				raise (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add AD Profile Success!","")
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()

class ADProfileAPI(Resource):

	def get(self, profile_id):
		try:
			session = Session()
			record = session.query(ADProfile).filter_by(id = profile_id).one()
			flag = 0
			if record.atas is not None:
				 flag = 1
			record = standardizedData(record)
			record['atas'] = 0
			if flag == 1:
				record['atas'] = 1				
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, profile_id):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			session.query(ADProfile).filter(ADProfile.id == profile_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				raise (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit AD Profile Success!", "")
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, profile_id):
		try:
			session = Session()
			session.query(ADProfile).filter(ADProfile.id == profile_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete AD Profile Success!", "")
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
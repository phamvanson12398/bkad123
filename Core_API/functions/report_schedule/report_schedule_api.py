import datetime
import pathlib

from models.models import ConnectToDB, ReportSchedule
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class ReportScheduleCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, ReportSchedule.__table__.columns, ReportSchedule
			)
			query = session.query(ReportSchedule)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in ReportSchedule.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				records[i] = standardizedData(records[i])
				records[i]['type'] = strToList(records[i]['type'])
				records[i]['email'] = strToList(records[i]['email'])
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
			reportschedule = ReportSchedule(
				name = data['name'],
				frequency = data['frequency'],
				specific_day = data['specific_day'],
				start_time = data['start_time'],
				type = str(data['type']),
				email = str(data['email']),
				status = 0
			)
			session.add(reportschedule)
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

class ReportScheduleAPI(Resource):

	def get(self, report_id):
		try:
			session = Session()
			record = session.query(ReportSchedule).filter_by(id = report_id).one()
			
			record = standardizedData(record)
			record['type'] = strToList(record['type'])
			record['email'] = strToList(record['email'])
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()
	
	def put(self, report_id):
		try:
			session = Session()
			data = request.get_json()
			if 'type' in data:
				data['type'] = str(data['type'])
			if 'email' in data:
				data['email'] = str(data['email'])
			session.query(ReportSchedule).\
				filter(ReportSchedule.id == report_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("Update Report Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()

	def delete(self, report_id):
		try:
			session = Session()
			session.query(ReportSchedule).\
				filter(ReportSchedule.id == report_id).delete()
			try:
				session.commit()
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("Delete Report Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()



def strToList(str):
    str = str.replace('[', '').replace(']', '').replace("'", '')
    lis = list(str.split(', '))
    return lis



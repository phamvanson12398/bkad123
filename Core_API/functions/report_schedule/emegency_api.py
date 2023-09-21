import datetime
import pathlib

from models.models import ConnectToDB, Emegency
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class EmegencyCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, Emegency.__table__.columns, Emegency
			)
			query = session.query(Emegency)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in Emegency.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				records[i] = standardizedData(records[i])
				records[i]['report_email'] = strToList(records[i]['report_email'])
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
			emegency = Emegency(
				name = data['name'],
				number_of_event = data['number_of_event'],
				time_limited = data['time_limited'],
				report_email = str(data['report_email']),
				status = 0
			)
			session.add(emegency)
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

class EmegencyScheduleAPI(Resource):

	def get(self, emegency_id):
		try:
			session = Session()
			record = session.query(Emegency).filter_by(id = emegency_id).one()
			record = standardizedData(record)
			record['report_email'] = strToList(record['report_email'])
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()
	
	def put(self, emegency_id):
		try:
			session = Session()
			data = request.get_json()
			if 'report_email' in data:
				data['report_email'] = str(data['report_email'])
			session.query(Emegency).\
				filter(Emegency.id == emegency_id).update(data)
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

	def delete(self, emegency_id):
		try:
			session = Session()
			session.query(Emegency).\
				filter(Emegency.id == emegency_id).delete()
			try:
				session.commit()
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("Delete emegency Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()



def strToList(str):
    str = str.replace('[', '').replace(']', '').replace("'", '')
    lis = list(str.split(', '))
    return lis



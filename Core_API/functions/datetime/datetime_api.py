import datetime
import pathlib

from models.models import ConnectToDB, DateTime
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class DateTimeAPI(Resource):

	def get(self):
		try:
			session = Session()
			record = standardizedData(session.query(DateTime).filter_by(id = 1).one())
			del record['id']
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def post(self):
		try:
			session = Session()
			data = request.get_json()
			if checkdata(data) == True:
				session.query(DateTime).\
					filter(DateTime.id == 1).update(data)
				try:
					session.commit()
					record = standardizedData(session.query(DateTime).filter_by(id = 1).one())
					record = delrecord(record)
				except Exception as exp:
					print (exp)
					session.rollback()
					return status_code_500("code 500 1")
				return status_code_200("", record)
			else:
				return "input data error"
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()

def checkdata(data):
	if data['sync_time'] == 0 and data['system_time'] != '' and data['time_zone'] != '' and data['server'] == '':
		return True
	elif data['sync_time'] == 1 and data['system_time'] == '' and data['time_zone'] == '' and data['server'] != '':
	 	return True
	else:
		return False

def delrecord(record):
	if record['sync_time'] == 0:
		del record['id'], record['server']
	else:
		del record['id'], record['system_time'], record['time_zone']

	return record
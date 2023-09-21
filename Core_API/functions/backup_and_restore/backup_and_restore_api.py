import datetime
import pathlib

from models.models import ConnectToDB, BackUp, BackUpPlan
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class BackUpAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, BackUp.__table__.columns, BackUp
			)
			query = session.query(BackUp)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in BackUp.__table__.columns))
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
			backup = BackUp(
				name = data['name'],
				password = data['password'],
				description = data['description'],
				datetime = str(datetime.datetime.now())
			)
			session.add(backup)
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

class BackUpAPIs(Resource):

	def get(self, backup_id):
		try:
			session = Session()
			record = session.query(BackUp).filter(BackUp.id == backup_id).one()
			record = standardizedData(record)
			return status_code_200("", record)
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()	

	def delete(self, backup_id):
		try:
			session = Session()
			session.query(BackUp).\
				filter(BackUp.id == backup_id).delete()
			try:
				session.commit()
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("Delete backup Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

class BackUpPlanAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, BackUpPlan.__table__.columns, BackUpPlan
			)
			query = session.query(BackUpPlan)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in BackUpPlan.__table__.columns))
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
			backup_plan = BackUpPlan(
				status = data['status'],
				frequency = data['frequency'],
				specific_day = data['specific_day'],
				start_time = data['start_time'],
				start_date = data['start_date'],
				end_date = data['end_date']
			)
			session.add(backup_plan)
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

class Restore(Resource):
	# def options(self):
	# 	return status_code_200("","")
	def post(self):
		return status_code_200("Successful","")
		data = request.get_json()
		if not 'backup_id' in data or not 'source' in data or not 'file' in data or not 'password' in data:
			return status_code_500("Fail") 
		else:
			try: 
				session = Session()
				data = request.get_json()
				backup = session.query(BackUp).\
				filter(BackUp.id == data['backup_id']).one()
				backup = standardizedData(backup)
				if data['password'] == backup['password']:
					return status_code_200('id pass ok', '')
				else:
					return status_code_500('id ok pass ko ok')
			except Exception as exp:
				print (exp)
				return status_code_400("")
			finally:
				session.close()	
	# def get(self, backup_id):
	# 	print ("+++++++++++++++++++++++++++++++++++++++++++++++")
		
	# 	# fn = "static/backup/backup_%d" % backup_id
	# 	# if not os.path.isfile(fn):
	# 	# 	fn = "static/backup/" + "backup.zip"
	# 	return send_file(fn)










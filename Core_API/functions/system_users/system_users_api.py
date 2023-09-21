import datetime
import pathlib

from models.models import ConnectToDB, SystemUsers
from libraries.general import getDefault, standardizedData, readfile, check_null, convert_none_to_string
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource
from libraries.envi import *



Session = ConnectToDB()

class UsersCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, SystemUsers.__table__.columns, SystemUsers
			)
			query = session.query(SystemUsers)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in SystemUsers.__table__.columns))
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
			user = SystemUsers(
				username = data['username'],
				password = data['password'],
				status = 0
			)
			session.add(user)
			try:
				session.commit()
				record = standardizedData(session.query(SystemUsers).filter_by(username = data['username']).one())
				del record['avatar'], record['name']
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("CREATE USER SUCCESS", record)
		except Exception as exp:
			raise (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()	



class UserAPI(Resource):

	def get(self, user_id):
		try:
			session = Session()
			record = session.query(SystemUsers).filter_by(id = user_id).one()
			record = standardizedData(record)
			return record
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()
	
	def put(self, user_id):
		try:
			session = Session()
			data = request.form.to_dict()
			# print("###############################1")
			# print(data)
			# print("###############################@@@@@@@@@@@@@@@@@@@@@@")
			if "avatar" in request.files:
				f = request.files['avatar']
				fn = "user_%s." %user_id+ f.filename.split(".")[-1]
				f.save(PATH_IMAGE +fn)
				data["avatar"] = "/api/static/image/" +fn
			if "password" in data and data['password'] == "":
				del data["password"]
			# print("###############################2")
			# print(data)
			# print("###############################@@@@@@@@@@@@@@@@@@@@@@")
			data = convert_none_to_string(data)
			# print("###############################3")
			# print(data)
			# print("###############################@@@@@@@@@@@@@@@@@@@@@@")
			
			
			if False :
				return status_code_400(str_error)
			else:
				current_time = datetime.datetime.now()
				# print (data,param)
				# key = verifyEditData(data, param)
				# if key is False:
				# 	print ("debug!!!!!!")
				# 	return status_code_400('')
				session.query(SystemUsers).filter(SystemUsers.id == user_id).update(data)

				try:
					session.commit()
				except Exception as exp:
					print (exp)
					session.rollback()
					return status_code_500("Error!")

				return status_code_200('', {'id': user_id})
		except Exception as exp:
			print(exp)
			return status_code_500(exp)
		finally:
			session.close()




		# 	session = Session()
		# 	data = request.get_json()
		# 	session.query(SystemUsers).\
		# 		filter(SystemUsers.id == user_id).update(data)
		# 	try:
		# 		session.commit()
		# 		record = standardizedData(session.query(SystemUsers).filter_by(id = user_id).one())
		# 		del record['username']
		# 	except Exception as exp:
		# 		print (exp)
		# 		session.rollback()
		# 		return status_code_500("code 500 1")
		# 	return status_code_200("USER UPDATE SUCCESS", record)
		# except Exception as exp:
		# 	print (exp)
		# 	return status_code_500("code 500 2")
		# finally:
		# 	session.close()

	def delete(self, user_id):
		try:
			session = Session()
			session.query(SystemUsers).\
				filter(SystemUsers.id == user_id).delete()
			try:
				session.commit()
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("DELETE SUCCESS", {})
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()



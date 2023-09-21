import datetime
import pathlib

from models.models import ConnectToDB, Operating_mode
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class Operating_modeAPI(Resource):

	def get(self):
		try: 
			session = Session()
			operating_mode = session.query(Operating_mode).\
				filter(Operating_mode.id == 1).one()
			operating_mode = standardizedData(operating_mode)
			del operating_mode['id']
			# return status_code_200('', operating_mode)
			return operating_mode
		except Exception as exp:
			print (exp)
			return status_code_400("code 400")
		finally:
			session.close()

	def post(self):
		try:
			session = Session()
			data = request.get_json()
			session.query(Operating_mode).\
				filter(Operating_mode.id == 1).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("", "")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()


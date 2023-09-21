from flask import Flask, request, jsonify ,send_file
from flask_restful import Resource, Api

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,get_jwt_claims)


from libraries.status_code import *
from libraries.general import *
from libraries.envi import *

import os 



class ImageData(Resource):
	def verify_input(self, data_to_verify):
		verify = True
		return True if verify == True else False
	
	def backup(self):
		pass
	
	
	def get(self,file_name):
		fn = PATH_IMAGE+ file_name
		if not os.path.isfile(fn):
			fn = PATH_IMAGE + "unknown.png"
		return send_file(fn, mimetype='image/gif')

	
class BackupData(Resource,):
	def verify_input(self, data_to_verify):
		verify = True
		return True if verify == True else False
	
	def backup(self):
		pass
	

	def get(self,backup_id):
		print ("+++++++++++++++++++++++++++++++++++++++++++++++@")
		fn = "static/backup/backup_%d" % backup_id
		print(fn)
		if not os.path.isfile(fn):
			fn = "static/backup/" + "backup.zip"
		print(fn)
		return send_file(fn)

	





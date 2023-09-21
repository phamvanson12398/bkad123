import datetime
import pathlib

from models.models import ConnectToDB, NetworkLoadBalancing,NetworkInterface
from libraries.general import getDefault, standardizedData, readfile, check_null
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class LoadBalancingCollectionAPI(Resource):

	def get(self):
		try: 
			session = Session()
			group_interface = session.query(NetworkLoadBalancing).\
				filter(NetworkLoadBalancing.id == 1).one()
			# member = []
			# for interface in group_interface.interface:
			# 	interface = standardizedData(
			# 		interface, None, {'id': 'id'})
			# 	interface = interface['id']
			# 	member.append(interface)
			group_interface = standardizedData(group_interface)
			group_interface['interface'] = cutStr(group_interface['interface'])
			return status_code_200('', group_interface)
		except Exception as exp:
			print (exp)
			return status_code_400("code 400")
		finally:
			session.close()

	def post(self):
		try:
			session = Session()
			data = request.get_json()
			for interface_id in data['interface']:
				try:
					interface = session.query(NetworkInterface).filter_by(id = int(interface_id)).one()
				except Exception as exp:
					raise(exp)
					return status_code_400('code 400')
				
			loadbalancing = NetworkLoadBalancing(
				id = 1,
				status = data['status'],
				command = data['command'],
				server = data['server'],
				timeout = data['timeout'],
				threshold = data['threshold'],
				interface = str(data['interface'])
			)
			
			session.add(loadbalancing)
			try:
				session.commit()
			except Exception as exp:
				raise (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("code 200","")
		except Exception as exp:
			# print(exp)
			raise (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()


	def put(self):
		try:
			session = Session()
			data = request.get_json()
			if 'interface' in data:
				for interface_id in data['interface']:
					try:
						interface = session.query(NetworkInterface).filter_by(id = int(interface_id)).one()
					except Exception as exp:
						raise(exp)
						return status_code_400('code 400')
			data["interface"] = str(data['interface'])
			session.query(NetworkLoadBalancing).\
				filter(NetworkLoadBalancing.id == 1).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("code 500 1")
			return status_code_200("Update Nat Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("code 500 2")
		finally:
			session.close()



def cutStr(str):
    str = str[1:-1].split(',')
    str = list(map(lambda x:int(x), str))
    return str
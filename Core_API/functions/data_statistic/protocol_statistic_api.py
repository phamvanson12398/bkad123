from datetime import datetime

from flask import request
from flask_restful import Resource

from models.clh_model import ConnectToDB
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *


class ProtocolDataStatisticCollectionAPI(Resource): 

	def get(self):
		try:
			client = ConnectToDB()
			parameters = request.args
			print (parameters)
			# if "protocol" not in parameters:
			# 	return status_code_400("Missing parameters!")
			if "from" in parameters and "to" in parameters:
				print ("FLAG 1")
				print (f"SELECT * FROM tcpdatastatistic WHERE\
						created_date >= toDate('{parameters['from']}') AND\
						created_date <= toDate('{parameters['to']}') ORDER BY created_at")
				raw_data = client.execute(
					f"SELECT * FROM tcpdatastatistic WHERE\
						created_date >= toDate('{parameters['from']}') AND\
						created_date <= toDate('{parameters['to']}') ORDER BY created_at"
				)
			else:
				print ("FLAG 2")
				raw_data = client.execute(
					f"SELECT * FROM tcpdatastatistic"
				)
			if len(raw_data) > 1000:
				# Ham lay trung binh du lieu
				pass
			data = []
			for i in range(len(raw_data)):
				data.append({
					'time': str(raw_data[i][1]),
					'packet_in': raw_data[i][2],
					'packet_out': raw_data[i][3],
					'bandwidth_in': raw_data[i][4],
					'bandwidth_out': raw_data[i][5],
					'percent': raw_data[i][6]
				})

			return status_code_200("", data)
		except Exception as exp:	
			print (exp)
			return status_code_500("")

class AddressDataStatisticCollectionAPI(Resource): 

	def get(self):
		try:
			client = ConnectToDB()
			parameters = request.args
			# if "address" not in parameters:
			# 	return status_code_400("Missing parameters!")
			if "from" in parameters and "to" in parameters:
				raw_data = client.execute(
					f"SELECT * FROM tcpdatastatistic WHERE\
						created_date >= toDate('{parameters['from']}') AND\
						created_date <= toDate('{parameters['to']}') ORDER BY created_at"
				)
			else:
				raw_data = client.execute(
					f"SELECT * FROM tcpdatastatistic ORDER BY created_at"
				)
			print (len(raw_data), raw_data)
			if len(raw_data) > 1000:
				# Ham lay trung binh du lieu
				pass
			data = []
			for i in range(len(raw_data)):
				data.append({
					'time': str(raw_data[i][1]),
					'packet_in': raw_data[i][2],
					'packet_out': raw_data[i][3],
					'bandwidth_in': raw_data[i][4],
					'bandwidth_out': raw_data[i][5],
					'percent': raw_data[i][6]
				})

			return status_code_200("", data)
		except Exception as exp:	
			print (exp)
			return status_code_500("")

class OthersDataStatisticCollectionAPI(Resource): 

	def get(self):
		try:
			client = ConnectToDB()
			parameters = request.args
			# if "other" not in parameters:
			# 	return status_code_400("Missing parameters!")
			if "from" in parameters and "to" in parameters:
				raw_data = client.execute(
					f"SELECT * FROM tcpdatastatistic WHERE\
						created_date >= toDate('{parameters['from']}') AND\
						created_date <= toDate('{parameters['to']}') ORDER BY created_at"
				)
			else:
				raw_data = client.execute(
					f"SELECT * FROM tcpdatastatistic ORDER BY created_at"
				)
			print (len(raw_data), raw_data)
			if len(raw_data) > 1000:
				# Ham lay trung binh du lieu
				pass
			data = []
			for i in range(len(raw_data)):
				data.append({
					'time': str(raw_data[i][1]),
					'packet_in': raw_data[i][2],
					'packet_out': raw_data[i][3],
					'bandwidth_in': raw_data[i][4],
					'bandwidth_out': raw_data[i][5],
					'percent': raw_data[i][6]
				})

			return status_code_200("", data)
		except Exception as exp:	
			print (exp)
			return status_code_500("")
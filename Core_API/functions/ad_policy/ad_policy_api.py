from sqlalchemy import or_

from models.models import ConnectToDB, ADPolicy, Network, GroupNetwork, ADPolicyHaveNetwork, ADPolicyHaveGroupNetwork
from libraries.general import getDefault, standardizedData, check_null 
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class ADPolicyCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, ADPolicy.__table__.columns, ADPolicy
			)
			query = session.query(ADPolicy)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in ADPolicy.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				target = []
				for network in records[i].network:
					network = standardizedData(
						network, None, {'id': 'id', 
							'name': 'name'}
					)
					network['type'] = 'obj'
					target.append(network)
				for group_network in records[i].group_network:
					group_network = standardizedData(
						group_network, None, {'id': 'id', 
							'name': 'name'}
					)
					group_network['type'] = 'gr_obj'
					target.append(group_network)
				profile = records[i].ad_profile
				profile = standardizedData(profile)
				records[i] = standardizedData(records[i], ['network', 'group_network'])
				del records[i]['ad_profile']
				records[i]['target'] = target
				records[i]['profile'] = profile
			return status_code_200("", get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def post(self):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			ad_policy = ADPolicy(
				name = data['name'],
				description = data['description'],
				profile = data['profile']
			)
			for target in data['target']:
				if target['type'] == "obj":
					try:
						network = session.query(Network).filter_by(id=int(target['id'])).one()
						print (network)
					except Exception as exp:
						return status_code_400('Not found target!')
					ad_policy.network.append(network)
				else:
					try:
						group_network = session.query(GroupNetwork).filter_by(id=int(target['id'])).one()
					except Exception as exp:
						raise (exp)
						return status_code_400('Not found target!')
					ad_policy.group_network.append(group_network)
			session.add(ad_policy)
			try:
				session.commit()
			except Exception as exp:
				raise (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add AD Policy Success!","")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

class ADPolicyAPI(Resource):

	def get(self, ad_policy_id):
		try:
			session = Session()
			record = session.query(ADPolicy).filter_by(id = ad_policy_id).one()
			target = []
			for network in record.network:
				network = standardizedData(
					network, None, {
						'id': 'id', 
						'name': 'name'
					})
				network['type'] = "obj"
				target.append(network)
			for group_network in record.group_network:
				group_network = standardizedData(
					group_network, None, {
						'id': 'id', 
						'name': 'name'
					})
				group_network['type'] = "gr_obj"
				target.append(group_network)
			profile = record.ad_profile
			profile = standardizedData(profile)
			record = standardizedData(record, ['network', 'group_network'])
			del record["ad_profile"]
			record['target'] = target
			record['profile']  = profile
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, ad_policy_id):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			if 'target' in data:
				session.query(ADPolicyHaveNetwork).\
					filter(ADPolicyHaveNetwork.policy_id == ad_policy_id).delete()
				session.query(ADPolicyHaveGroupNetwork).\
					filter(ADPolicyHaveGroupNetwork.policy_id == ad_policy_id).delete()
				for target in data['target']:
					if target['type'] == "obj":
						link = ADPolicyHaveNetwork(
							policy_id=ad_policy_id,
							network_id=target['id']
						)
						session.add(link)
					else:
						link = ADPolicyHaveGroupNetwork(
							policy_id=ad_policy_id,
							group_network_id=target['id']
						)
						session.add(link)
				try:
					session.commit()
				except Exception as exp:
					session.rollback()
					return status_code_400('Request data error!')
				del data['target']
			session.query(ADPolicy).filter(ADPolicy.id == ad_policy_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit AD Policy Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, ad_policy_id):
		try:
			session = Session()
			session.query(ADPolicy).filter(ADPolicy.id == ad_policy_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete AD Policy Success!", "")
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
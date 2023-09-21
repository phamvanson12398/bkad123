from sqlalchemy import or_

from models.models import ConnectToDB, Network, GroupNetwork, GroupNetworkHaveNetwork
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class GroupNetworkCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, GroupNetwork.__table__.columns, GroupNetwork
			)
			query = session.query(GroupNetwork)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in GroupNetwork.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				member = []
				for network in records[i].network:
					network = standardizedData(
						network, None, {'id': 'id', 
							'name': 'name', 
							'ip_address': 'ip_address', 
							'netmask': 'netmask'}
					)
					member.append(network)
				records[i] = standardizedData(records[i], ['network'])
				records[i]['member'] = member
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
			group_network = GroupNetwork(
				name = data['name'],
				description = data['description']
			)
			for network_id in data['member']:
				try:
					network = session.query(Network).filter_by(id=int(network_id)).one()
				except Exception as exp:
					return status_code_400('Not found member!')
				group_network.network.append(network)
			session.add(group_network)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add Group Network Success!","")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def options(self):
		try:
			data = {
				'name': {
					'default': None,
					'placeholder': 'Name',
					'required': True,
					'type': 'String'
				},
				'member': {
					'default': None,
					'item': {
						'type': "Number"
					},
					'placeholder': 'Network Members',
					'required': True,
					'type': 'array'
				},
				'description': {
					'default': None,
					'placeholder': "Description",
					'required': True,
					'type': 'String'
				}
			}
			return status_code_200("", data)
		except Exception as exp:
			print (f"Error in [OPTIONS] network_api!: {exp}")
			return status_code_500("Error!")


class GroupNetworkAPI(Resource):

	def get(self, group_network_id):
		try:
			session = Session()
			record = session.query(GroupNetwork).filter_by(id = group_network_id).one()
			member = []
			for network in record.network:
				network = standardizedData(
					network, None, {
						'id': 'id', 
						'name': 'name', 
						'ip_address': 'ip_address', 
						'netmask': 'netmask'
					})
				member.append(network)
			record = standardizedData(record, ['network'])
			record['member'] = member
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, group_network_id):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			if 'member' in data:
				session.query(GroupNetworkHaveNetwork).\
					filter(GroupNetworkHaveNetwork.group_network_id == group_network_id).delete()
				for network_id in data['member']:
					link = GroupNetworkHaveNetwork(
						group_network_id=group_network_id,
						network_id=network_id
					)
					session.add(link)
				try:
					session.commit()
				except Exception as exp:
					session.rollback()
					return status_code_400('Request data error!')
				del data['member']
			session.query(GroupNetwork).filter(GroupNetwork.id == group_network_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit Group Network Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, group_network_id):
		try:
			session = Session()
			session.query(GroupNetwork).filter(GroupNetwork.id == group_network_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete Group Network Success!", "")
		except Exception as exp: 
			return status_code_500(exp)
		finally:
			session.close()


class NetworkGroupNetwork(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			group_networks = session.query(GroupNetwork)
			if 'search' in parameters:
				group_networks = group_networks.filter(
					or_(key.like(('%'+parameters['search']+'%'))\
					for key in GroupNetwork.__table__.columns)
				)
			group_networks = group_networks.all()

			for i in range(len(group_networks)):
				group_networks[i] = General.standardizedData(group_networks[i])
				group_networks[i]['type'] = 'gr_obj'
				group_networks[i]['preview'] = group_networks[i]['description']

				del group_networks[i]['description']
				del group_networks[i]['created_at']
				del group_networks[i]['updated_at']

			networks = session.query(Network)
			if 'search' in parameters:
				networks = networks.filter(
					or_(key.like(('%'+parameters['search']+'%'))\
					for key in Network.__table__.columns)
				)
			networks = networks.all()

			for i in range(len(networks)):
				networks[i] = General.standardizedData(networks[i])
				networks[i]['type'] = 'obj'
				networks[i]['preview'] = networks[i]['ip_address'] +\
					 "/" + netmask2cidr(networks[i]['netmask'])

				del networks[i]['ip_address']
				del networks[i]['netmask']
				del networks[i]['description']
				del networks[i]['created_at']
				del networks[i]['updated_at']

			net_and_gnet = networks + group_networks

			#Auto create network from Interfaces
			if 'context' in parameters:
				if parameters['context'] == "add_fw_destination":
					interfaces = session.query(NetworkInterface)
					if 'search' in parameters:
						interfaces = interfaces.filter(
							or_(key.like(('%'+parameters['search']+'%'))\
							for key in NetworkInterface.__table__.columns)
						)
					interfaces = interfaces.all()

					ints = []
					for i in range(len(interfaces)):
						interfaces[i] = General.standardizedData(interfaces[i])
						ints.append({
							"id": interfaces[i]['id'],
							"name": "[Port] " + interfaces[i]['name'],
							"type": "interface",
							"preview": "Auto Created by System!"
						})

					net_and_gnet = ints + net_and_gnet
			return status_code_200('', net_and_gnet)
		except Exception as exp:
			raise (exp)
			return status_code_400(exp)
		finally:
			session.close()

def verify_input(data):
	try:
		str_error = ""

		return str_error
	except Exception as exp:
		print (exp)
		return False
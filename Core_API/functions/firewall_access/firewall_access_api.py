import datetime
import pathlib
import os


from models.models import ConnectToDB, FireWallAccess, Network, GroupNetwork, Service, NetworkInterface, GroupService, FireWallAccessSource, FireWallAccessGroupSource, FireWallAccessDestinaton, FireWallAccessGroupDestinaton, FireWallAccessService, FireWallAccessGroupService, FireWallAccessInterface
from libraries.general import getDefault, standardizedData, readfile, check_null, is_number
from libraries.status_code import *
from sqlalchemy import or_
from flask import request
from flask_restful import Resource

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + "/static/keypair"

Session = ConnectToDB()

class FirewallAccessAPI(Resource):

	def get(self, firewall_policy_id):
		try: 
			session = Session()
			services = []
			sources = []
			destinations = []
			interfaces = []

			firewall_policy = session.query(FireWallAccess).\
				filter(FireWallAccess.id == firewall_policy_id).one()
			
			# interface = firewall_policy.interface
			# interface = standardizedData(
			# 	interface, None, {'id': 'id', 'name': 'name'}
			# )
			for interface in firewall_policy.firewall_interface:
				interface = standardizedData(
					interface, None, {'id': 'id', 'name': 'name'}
				)
				interfaces.append(interface)

			for service in firewall_policy.firewall_access_service:
				service = standardizedData(
					service, None, {'id': 'id', 'name': 'protocol'}
				)
				service['type'] = 'obj'
				services.append(service)

			for group_service in firewall_policy.firewall_access_group_service:
				group_service = standardizedData(
					group_service, None, {'id': 'id', 'name': 'name'}
				)
				group_service['type'] = 'gr_obj'
				services.append(group_service)

			for source in firewall_policy.firewall_access_source:
				source = standardizedData(
					source, None, {'id': 'id', 
					'name':'name', 
					'address': 'ip_address'}
				)
				source['type'] = 'obj'
				sources.append(source)

			for group_source in firewall_policy.firewall_access_group_source:
				group_source = standardizedData(
					group_source, None, {'id': 'id', 'name': 'name'}
				)
				group_source['type'] = 'gr_obj'
				sources.append(group_source)

			# ---Start the f** code - Khong biet tai sao can phai co doan code nay, chi biet thieu no thi code
			# khong chay duoc :(---
			session = Session()
			firewall_policy = session.query(FireWallAccess).\
				filter(FireWallAccess.id == firewall_policy_id).one()
			# ---End the f** code---

			for destination in firewall_policy.firewall_access_destination:
				destination = standardizedData(
					destination, None, {'id': 'id', 
					'name':'name', 
					'address': 'ip_address'}
				)
				destination['type'] = 'obj'
				destinations.append(destination)

			for group_destination in firewall_policy.firewall_access_group_destination:
				group_destination = standardizedData(
					group_destination, None, {'id': 'id', 'name': 'name'}
				)
				group_destination['type'] = 'gr_obj'
				destinations.append(group_destination)

			firewall_policy = standardizedData(firewall_policy, 
												['firewall_access_service',
												'firewall_access_source',
												'firewall_access_destination',
												'firewall_access_group_service',
												'firewall_access_group_source',
												'firewall_access_group_destination'])
			print("#4")
			firewall_policy['interface'] = interfaces
			print("#5")
			firewall_policy['service'] = services
			print("#6")
			firewall_policy['source'] = sources
			firewall_policy['destination'] = destinations

			print (firewall_policy)
			# return False
			session.close()
			return status_code_200('', firewall_policy)
		except Exception as exp:
			raise (exp)
			session.close()
			return status_code_500("Database error!")
		finally:
			pass
			# session.close()

	def put(self, firewall_policy_id):
		try:
			session = Session()
			data = request.json

			if 'interface' in data:
				session.query(FireWallAccessInterface).\
					filter(FireWallAccessInterface.firewall_id ==\
						firewall_policy_id).delete()
				for interface_id in data['interface']:
					firewall_access_interface = FireWallAccessInterface(
						firewall_id = firewall_policy_id,
						interface_id = interface_id
					)
					session.add(firewall_access_interface)
				try:
					session.commit()
				except Exception as exp:
					print (exp)
					session.rollback()
					return status_code_400('Request data error!')
				del data['interface']

			if 'service' in data:
				session.query(FireWallAccessService).\
					filter(FireWallAccessService.firewall_id ==\
						firewall_policy_id).delete()
				session.query(FireWallAccessGroupService).\
					filter(FireWallAccessGroupService.firewall_id ==\
						firewall_policy_id).delete()
				for service in data['service']:
					if service['type'] == 'obj':
						firewall_access_service = FireWallAccessService(
							firewall_id=firewall_policy_id,
							service_id=service['id']
						)
						session.add(firewall_access_service)
					elif service['type'] == 'gr_obj':
						firewall_access_group_service = FireWallAccessGroupService(
							firewall_id=firewall_policy_id,
							gr_service_id=service['id']
						)
						session.add(firewall_access_group_service)
				try:
					session.commit()
				except Exception as exp:
					print (exp)
					session.rollback()
					return status_code_400('Request data error!')
				del data['service']

			if 'source' in data:
				session.query(FireWallAccessSource).\
					filter(FireWallAccessSource.firewall_id ==\
						firewall_policy_id).delete()
				session.query(FireWallAccessGroupSource).\
					filter(FireWallAccessGroupSource.firewall_id ==\
						firewall_policy_id).delete()
				for source in data['source']:
					if source['type'] == 'obj':
						firewall_access_source = FireWallAccessSource(
							firewall_id=firewall_policy_id,
							network_id=source['id']
						)
						session.add(firewall_access_source)
					elif source['type'] == 'gr_obj':
						firewall_access_group_source = FireWallAccessGroupSource(
							firewall_id=firewall_policy_id,
							gr_network_id=source['id']
						)
						session.add(firewall_access_group_source)
				try:
					session.commit()
				except Exception as exp:
					print (exp)
					session.rollback()
					return status_code_400('Request data error!')
				del data['source']

			if 'destination' in data:
				session.query(FireWallAccessDestinaton).\
					filter(FireWallAccessDestinaton.firewall_id ==\
						firewall_policy_id).delete()
				session.query(FireWallAccessGroupDestinaton).\
					filter(FireWallAccessGroupDestinaton.firewall_id ==\
						firewall_policy_id).delete()
				for destination in data['destination']:
					if destination['type'] == 'obj':
						firewall_policy_destination = FireWallAccessDestinaton(
							firewall_id=firewall_policy_id,
							network_id=destination['id']
						)
						session.add(firewall_policy_destination)
					elif destination['type'] == 'gr_obj':
						firewall_policy_group_destination = FireWallAccessGroupDestinaton(
							firewall_id=firewall_policy_id,
							gr_network_id=destination['id']
						)
						session.add(firewall_policy_group_destination)
				try:
					session.commit()
				except Exception as exp:
					print (exp)
					session.rollback()
					return status_code_400('Request data error!')
				del data['destination']

			data['edited_at'] = str(datetime.datetime.now())
			# data['acc_updated'] = user_name
			session.query(FireWallAccess).\
				filter(FireWallAccess.id==firewall_policy_id).update(data)
			# firewall_core.add_policy(session)
			try:
				session.commit()
				# backup_policy()
				return status_code_200('', {"id": firewall_policy_id})
			except Exception as exp:
				raise (exp)
				session.rollback()
				return status_code_500("Error!")
		except Exception as exp:
			raise (exp)
			return status_code_500("Database error!")
		finally:
			session.close()


	def delete(self, firewall_policy_id):
		try:
			session = Session()
			# old_pos = session.query(FirewallPolicy).\
			# 	filter(FirewallPolicy.id == firewall_policy_id).first().__dict__['position']
			session.query(FireWallAccess).\
				filter(FireWallAccess.id == firewall_policy_id).delete()
			session.query(FireWallAccessService).\
				filter(FireWallAccessService.firewall_id ==\
					firewall_policy_id).delete()
			session.query(FireWallAccessGroupService).\
				filter(FireWallAccessGroupService.firewall_id ==\
					firewall_policy_id).delete()
			session.query(FireWallAccessSource).\
				filter(FireWallAccessSource.firewall_id ==\
					firewall_policy_id).delete()
			session.query(FireWallAccessGroupSource).\
				filter(FireWallAccessGroupSource.firewall_id ==\
					firewall_policy_id).delete()
			session.query(FireWallAccessDestinaton).\
				filter(FireWallAccessDestinaton.firewall_id ==\
					firewall_policy_id).delete()
			session.query(FireWallAccessGroupDestinaton).\
				filter(FireWallAccessGroupDestinaton.firewall_id ==\
					firewall_policy_id).delete()
			session.query(FireWallAccessInterface).\
				filter(FireWallAccessInterface.firewall_id ==\
					firewall_policy_id).delete()
			# policies = session.query(FirewallPolicy).all()
			# for policy in policies:
			# 	if policy.__dict__['position'] > old_pos:
			# 		session.query(FirewallPolicy).\
			# 			filter(FirewallPolicy.id == policy.__dict__['id']).update( 
			# 				{"position": policy.__dict__['position'] - 1}
			# 			)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("Database error!")
			return status_code_200("Delete FireWall Success!", "")
			# try:
			# 	firewall_core.add_policy()
			# except Exception as exp:
			# 	print (exp)
			# 	pass
			# backup_policy()
			# return status_code_200(
			# 	('Deleted record id = ' + str(firewall_policy_id)), {'id': firewall_policy_id}
			# )
		except Exception as exp: 
			raise (exp)
			return status_code_500("Database error!")
		finally:
			session.close()
		
class FirewallAccessCollectionAPI(Resource):


	def get(self):
		try:
			session = Session()
			# check_pos()
			parameters = request.args.to_dict()
			# parameters["orderBy"] = "position"
			# if  "orderType" not in parameters:
			# 	parameters["orderType"] = 'asc'
			try:
				limit, page, offset, order = getDefault(
					parameters, FireWallAccess.__table__.columns, FireWallAccess
				)
				query = session.query(FireWallAccess)
				if 'search' in parameters and parameters['search'] != '':
					search_values = parameters['search'].split(",")
					for search_value in search_values:
						query = query.filter(
							or_(key.like('%'+ search_value +'%')\
								for key in FireWallAccess.__table__.columns)
						)
				total_count = query.count()
				records = query.order_by(order).offset(offset).limit(limit).all()
				
				for i in range(len(records)):
					# interface = records[i].interface
					# interface = standardizedData(
					# 	interface, None, {'id': 'id', 'name': 'name'}
					# )

					services = []
					sources = []
					destinations = []
					interfaces = []

					for interface in records[i].firewall_interface:
						interface = standardizedData(
							interface, None, {'id': 'id', 
							'name': 'name'}
						)
						interfaces.append(interface)

					for service in records[i].firewall_access_service:
						service = standardizedData(
							service, None, {'id': 'id', 
							'name': 'name'}
						)
						service['type'] = 'obj'
						services.append(service)
					print("#1")
					for group_service in records[i].firewall_access_group_service:
						group_service = standardizedData(
							group_service, None, {'id': 'id', 
							'name': 'name'}
						)
						group_service['type'] = 'gr_obj'
						services.append(group_service)
					print("#2")
					for destination in records[i].firewall_access_destination:
						print (destination)
						destination = standardizedData(
							destination, None, {'id': 'id', 
							'name':'name'}
						)
						destination['type'] = 'obj'
						destinations.append(destination)
					for group_destination in records[i].firewall_access_group_destination:
						group_destination = standardizedData(
							group_destination, None, {'id': 'id', 
							'name': 'name'}
						)
						group_destination['type'] = 'gr_obj'
						destinations.append(group_destination)

					# ---Start the f** code - Khong biet tai sao can phai co doan code nay, chi biet thieu no thi code
					# khong chay duoc :(---
					session = Session()
					records[i] = session.query(FireWallAccess).\
						filter(FireWallAccess.id == records[i].id).one()
					# ---End the f** code---

					for source in records[i].firewall_access_source:
						source = standardizedData(
							source, None, {'id': 'id', 
							'name':'name'}
						)
						source['type'] = 'obj'
						sources.append(source)
					for group_source in records[i].firewall_access_group_source:
						group_source = standardizedData(
							group_source, None, {'id': 'id', 
							'name': 'name'}
						)
						group_source['type'] = 'gr_obj'
						sources.append(group_source)

					records[i] = standardizedData(records[i], 
												['firewall_access_service',
												'firewall_access_source',
												'firewall_access_destination',
												'firewall_access_group_service',
												'firewall_access_group_source',
												'firewall_access_group_destination'])
					records[i]['interface'] = interfaces
					records[i]['service'] = services
					records[i]['source'] = sources
					records[i]['destination'] = destinations
			except Exception as exp:
				session.rollback()
				raise (exp)
				return status_code_400(exp)
			return status_code_200('',get_data_with_page(records, limit, page, total_count))
		except Exception as exp:
			raise (exp)
			return status_code_500("Database error!")
		finally:
			session.close()


	def post(self):
		try:
			session = Session()
			data = request.get_json()
			
			firewall = FireWallAccess(
				name = data['name'],
				position = data['position'],
				action = data['action'],
				status = 1,
				created_at = str(datetime.datetime.now()),
				edited_at = str(datetime.datetime.now())	
			)
			try:
				for source in data['source']:
					if source['type'] == 'obj':
						source1 = session.query(Network).filter_by(id = int(source['id'])).one()
						firewall.firewall_access_source.append(source1)
					else:
						source1 = session.query(GroupNetwork).filter_by(id = int(source['id'])).one()
						firewall.firewall_access_group_source.append(source1)
					
				for destination in data['destination']:
					if destination['type'] == 'obj':
						destination1 = session.query(Network).filter_by(id = int(destination['id'])).one()
						firewall.firewall_access_destination.append(destination1)
					else:
						destination1 = session.query(GroupNetwork).filter_by(id = int(destination['id'])).one()
						firewall.firewall_access_group_destination.append(destination1)
				
				for service in data['service']:
					if service['type'] == 'obj':
						service1 = session.query(Service).filter_by(id = int(service['id'])).one()
						firewall.firewall_access_service.append(service1)
					else:
						service1 = session.query(GroupService).filter_by(id = int(service['id'])).one()
						firewall.firewall_access_group_service.append(service1)
				try:
					member = []
					for interface_id in data['interface']:
						try:
							interface = session.query(NetworkInterface).filter_by(id = interface_id).one()
						except Exception as exp:
							raise(exp)
							return status_code_400('code 400')
						firewall.firewall_interface.append(interface)
					# interface = session.query(NetworkInterface).filter_by(id = int(data['interface'])).one()
				except Exception as e:
					raise (e)
					return status_code_400('code 400')
				 
			except Exception as e:
				raise (e)
				return status_code_400('code 400')
			print(firewall.firewall_interface)
			session.add(firewall)
			try:
				session.commit()
			except Exception as exp:
				raise (exp)
				session.rollback()
				return status_code_500("database error")
			return status_code_200("Add FireWall Success!", "")
			
		except Exception as exp:
			raise (exp)
			return status_code_500("database error")
		finally:
			session.close()

def verify_input(data):
	str_error = ''

	if 'name' in data and data['name'] != "":
		if len(data['name']) < 3 or len(data['name']) > 30:
			str_error = str_error + 'Name : Format name incorrect\n'
	
	if 'position' in data and data['position'] != "":
		if is_number(data['position']) is False:
			str_error = str_error + 'Position: Format position incorrect\n'
	
	if 'action' in data and data['action'] != "":
		if data['action'] not in ["accept", "reject", "drop"]:
			str_error = str_error + 'Action: Format action incorrect\n'
	
	if 'interface' in data and data['interface'] != "":
		if is_number(data['interface']) is False:
			str_error = str_error + 'interface: Format interface incorrect\n'
	
	if 'logs' in data and data['logs'] != "":
		if is_number(data['logs']) is False:
			str_error = str_error + 'Logs: Format logs incorrect\n'
	
	if 'service' in data and data['service'] != "":
		for service in data['service']:
			if is_number(service['id']) is not True:
				str_error = str_error + 'Service: Format service incorrect\n'
				break

	if 'source' in data and data['source'] != "":
		for source in data['source']:
			if is_number(source['id']) is not True:
				str_error = str_error + 'Source: Format source incorrect\n'

	if 'destination' in data and data['destination'] != "":
		for destination in data['destination']:
			if is_number(destination['id']) is not True:
				str_error = str_error + 'Destination: Format destination incorrect\n'
	
	if 'description' in data and data['description'] != "":
		if len(data['description']) > 255:
			str_error = str_error + 'Description : Format description incorrect\n'

	return str_error


def backup_policy():
	try:
		os.system("iptables-save > /etc/policy_init.sh")
	except Exception as exp:
		return False
	finally:
		os.system("chmod +x /etc/policy_init.sh")

def returnID(id):
	return {"id" : id}
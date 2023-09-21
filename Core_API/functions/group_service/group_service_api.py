from sqlalchemy import or_

from models.models import ConnectToDB, Service, GroupService, GroupServiceHaveServices
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class GroupServiceCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, GroupService.__table__.columns, GroupService
			)
			query = session.query(GroupService)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in GroupService.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				member = []
				for service in records[i].service:
					service = standardizedData(
						service, None, {'id': 'id',
							'name': 'name', 
							'port': 'port',
							'protocol': 'protocol'}
					)
					member.append(service)
				records[i] = standardizedData(records[i], ['service'])
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
			group_Service = GroupService(
				name = data['name'],
				description = data['description']
			)
			for service_id in data['member']:
				try:
					service = session.query(Service).filter_by(id=int(service_id)).one()
				except Exception as exp:
					return status_code_400('Not found member!')
				group_Service.service.append(service)
			session.add(group_Service)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add Group Service Success!","")
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
					'placeholder': 'Service Members',
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
			print (f"Error in [OPTIONS] Service_api!: {exp}")
			return status_code_500("Error!")


class GroupServiceAPI(Resource):

	def get(self, group_service_id):
		try:
			session = Session()
			record = session.query(GroupService).filter_by(id = group_service_id).one()
			member = []
			for service in record.service:
				service = standardizedData(
					service, None, {
						'id': 'id', 
						'name': 'name', 
						'port': 'port',
						'protocol': 'protocol'
					})
				member.append(service)
			record = standardizedData(record, ['service'])
			record['member'] = member
			return status_code_200("", record)
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def put(self, group_service_id):
		try:
			session = Session()
			data = request.json
			error = verify_input(data)
			if error != "" or error is False:
				return status_code_400("Request Data Error!")
			if check_null(data) is False:
				return status_code_400("Request Data Error!")
			if 'member' in data:
				session.query(GroupServiceHaveServices).\
					filter(GroupServiceHaveServices.group_service_id == group_service_id).delete()
				for service_id in data['member']:
					link = GroupServiceHaveServices(
						group_service_id=group_service_id,
						service_id=service_id
					)
					session.add(link)
				try:
					session.commit()
				except Exception as exp:
					session.rollback()
					return status_code_400('Request data error!')
				del data['member']
			session.query(GroupService).filter(GroupService.id == group_service_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Edit Group Service Success!", "")
		except Exception as exp:
			raise (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, group_service_id):
		try:
			session = Session()
			session.query(GroupService).filter(GroupService.id == group_service_id).delete()
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Delete Group Service Success!", "")
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
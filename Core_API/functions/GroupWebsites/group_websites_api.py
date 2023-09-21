from sqlalchemy import or_

from models.models import ConnectToDB, Websites, GroupWebsites, GroupWebsitesHaveWebsites
from libraries.general import getDefault, standardizedData
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class GroupWebsitesCollectionAPI(Resource):

	def get(self):
		try:
			session = Session()
			parameters = request.args
			limit, page, offset, order = getDefault(
				parameters, GroupWebsites.__table__.columns, GroupWebsites
			)
			query = session.query(GroupWebsites)
			if "search" in parameters and parameters['search'] != "":
				search_values = parameters['search'].split(",")
				for search_value in search_values:
					query = query.filter(or_(key.like('%'+ search_value +'%')\
						for key in GroupWebsites.__table__.columns))
			total_count = query.count()
			records = query.order_by(order).offset(offset).limit(limit).all()
			for i in range(len(records)):
				member = []
				for website in records[i].websites:
					website = standardizedData(
						website, None, {'id': 'id', 'domain': 'domain', 'ip_address': 'ip_address'}
					)
					member.append(website)
				records[i] = standardizedData(records[i], ["websites"])
				records[i]['member'] = member
				print (records[i])
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
			group_website = GroupWebsites(
				name = data['name'],
				description = data['description']
			)
			for website_id in data['member']:
				try:
					website = session.query(Websites).filter_by(id = int(website_id)).one()
				except Exception as exp:
					return status_code_400('Not found member!')
				group_website.websites.append(website)
			session.add(group_website)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Add Group Website Success!","")
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
					'placeholder': 'Website Members',
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


class GroupWebsitesAPI(Resource):

	def get(self, group_website_id):
		try: 
			session = Session()
			group_website = session.query(GroupWebsites).\
				filter(GroupWebsites.id == group_website_id).one()
			member = []
			for website in group_website.websites:
				website = standardizedData(
					website, None, {'id': 'id', 'domain': 'domain', 'ip_address': 'ip_address'})
				member.append(website)
			group_website = standardizedData(group_website, ['websites'])
			group_website['member'] = member
			return status_code_200('', group_website)
		except Exception as exp:
			print (exp)
			return status_code_400("")
		finally:
			session.close()

	def put(self, group_website_id):
		try:
			session = Session()
			data = request.json
			str_error = verify_input(data)
			if str_error != '':
				return status_code_400(str_error)
			if 'member' in data:
				session.query(GroupWebsitesHaveWebsites).\
					filter(GroupWebsitesHaveWebsites.group_website_id == group_website_id).delete()
				for website_id in data['member']:
					link = GroupWebsitesHaveWebsites(
						group_website_id = group_website_id,
						website_id = website_id
					)
					session.add(link)
				try:
					session.commit()
				except Exception as exp:
					session.rollback()
					return status_code_400('Request data error!')
				del data['member']
			session.query(GroupWebsites).\
				filter(GroupWebsites.id == group_website_id).update(data)
			try:
				session.commit()
			except Exception as exp:
				print (exp)
				session.rollback()
				return status_code_500("")
			return status_code_200("Update Group Website Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

	def delete(self, group_website_id):
		try:
			session = Session()
			session.query(GroupWebsites).\
				filter(GroupWebsites.id == group_website_id).delete()
			try:
				session.commit()
			except Exception as exp:
				session.rollback() 
				return status_code_500(exp)
			return status_code_200("Delete Group Websites Success!", "")
		except Exception as exp:
			print (exp)
			return status_code_500("")
		finally:
			session.close()

def verify_input(data):
	try:
		str_error = ""

		return str_error
	except Exception as exp:
		print (exp)
		return False
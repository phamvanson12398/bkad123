from sqlalchemy import or_

from models.models import ConnectToDB, HttpThreshold, HttpThresholdValue
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class HttpHostThresholdCollectionAPI(Resource):

    def get(self,profile_id):
        try:
            session = Session()
            parameters = request.args
           
            limit, page, offset, order = getDefault(
                parameters, HttpThreshold.__table__.columns, HttpThreshold
            )
            query = session.query(HttpThreshold).filter(HttpThreshold.profile == profile_id).\
                filter(HttpThreshold.type == "host")
            if "search" in parameters and parameters['search'] != "":
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    query = query.filter(or_(key.like('%'+ search_value +'%')\
                        for key in HttpThreshold.__table__.columns))
            total_count = query.count()
            records = query.order_by(order).offset(offset).limit(limit).all()
            for i in range(len(records)):
                hosts = []
                for host in records[i].http_threshold_value:
                    hosts.append(host.value)
                records[i] = standardizedData(records[i], ['http_threshold_value'])
                records[i]['hosts'] = hosts
                del records[i]['type']
            return status_code_200("", get_data_with_page(records, limit, page, total_count))
        except Exception as exp:
            print (exp)
            return status_code_500("")
        finally:
            session.close()

    def post(self,profile_id):
        try:
            session = Session()
            parameters = request.args
            
            data = request.json
            data['profile'] = profile_id
            error = verify_input(data)
            if error != "" or error is False:
                return status_code_400("Request Data Error!")
            http_threshold = HttpThreshold(
                name = data['name'],
                packet_in = data['packet_in'],
                packet_out = data['packet_out'],
                bandwidth_in = data['bandwidth_in'],
                bandwidth_out = data['bandwidth_out'],
                percent = data['percent'],
                description = data['description'],
                prevention = data['prevention'],
                status = data['status'],
                profile = data['profile'],
                type = "host"
            )
            session.add(http_threshold)
            try:
                session.commit()
                for line in data['hosts']:
                    session.add(HttpThresholdValue(
                        http_threshold_id = http_threshold.id,
                        value = line
                    ))
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Add HTTP host Threshold Success!","")
        except Exception as exp:
            print (exp)
            return status_code_500("")
        finally:
            session.close()

    # def options(self):
    #     try:
    #         data = {
    #             'name': {
    #                 'default': None,
    #                 'placeholder': 'Name',
    #                 'required': True,
    #                 'type': 'String'
    #             },
    #             'member': {
    #                 'default': None,
    #                 'item': {
    #                     'type': "Number"
    #                 },
    #                 'placeholder': 'Network Members',
    #                 'required': True,
    #                 'type': 'array'
    #             },
    #             'description': {
    #                 'default': None,
    #                 'placeholder': "Description",
    #                 'required': True,
    #                 'type': 'String'
    #             }
    #         }
    #         return status_code_200("", data)
    #     except Exception as exp:
    #         print (f"Error in [OPTIONS] network_api!: {exp}")
    #         return status_code_500("Error!")


class HttpHostThresholdAPI(Resource):

    def get(self,profile_id, host_threshold_id):
        try:
            session = Session()
            parameters = request.args
            
            record = session.query(HttpThreshold).filter(HttpThreshold.profile == profile_id).\
                filter(HttpThreshold.type == "host").filter_by(id = host_threshold_id).one()
            record = standardizedData(record)
            return status_code_200("", record)
        except Exception as exp:
            print (exp)
            return status_code_500("")
        finally:
            session.close()

    def put(self, profile_id, host_threshold_id):
        try:
            session = Session()
            parameters = request.args
            
            data = request.json
            error = verify_input(data)
            if error != "" or error is False:
                return status_code_400("Request Data Error!")
            if check_null(data) is False:
                return status_code_400("Request Data Error!")
            if "hosts" in data:
                session.query(HttpThresholdValue).\
                    filter(HttpThresholdValue.http_threshold_id == host_threshold_id).delete()
                try:
                    session.commit()
                except Exception as exp:
                    print (exp)
                    session.rollback()
                    return status_code_500("Error!")
                for host in data['hosts']:
                    http_threshold_value = HttpThresholdValue(
                        http_threshold_id = host_threshold_id,
                        value = host
                    )
                    session.add(http_threshold_value)
                    try:
                        session.commit()
                    except Exception as exp:
                        print (exp)
                        session.rollback()
                        return status_code_500("Error!")
                del data['hosts']
            session.query(HttpThreshold).\
                filter(HttpThreshold.profile == profile_id).filter(HttpThreshold.type == "host").\
                filter(HttpThreshold.id == host_threshold_id).update(data)
            try:
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Edit HTTP host Threshold Success!", "")
        except Exception as exp:
            print (exp)
            return status_code_500("")
        finally:
            session.close()

    def delete(self,profile_id, host_threshold_id):
        try:
            session = Session()
            parameters = request.args
            
            session.query(HttpThreshold).filter(HttpThreshold.profile == profile_id).\
                filter(HttpThreshold.type == "host").\
                filter(HttpThreshold.id == host_threshold_id).delete()
            try:
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Delete HTTP host Threshold Success!", "")
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
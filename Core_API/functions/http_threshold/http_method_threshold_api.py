from sqlalchemy import or_

from models.models import ConnectToDB, HttpThreshold, HttpThresholdValue
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class HttpMethodThresholdCollectionAPI(Resource):

    def get(self,profile_id):
        try:
            session = Session()
            parameters = request.args
           
            limit, page, offset, order = getDefault(
                parameters, HttpThreshold.__table__.columns, HttpThreshold
            )
            query = session.query(HttpThreshold).filter(HttpThreshold.profile == profile_id).\
                filter(HttpThreshold.type == "method")
            if "search" in parameters and parameters['search'] != "":
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    query = query.filter(or_(key.like('%'+ search_value +'%')\
                        for key in HttpThreshold.__table__.columns))
            total_count = query.count()
            records = query.order_by(order).offset(offset).limit(limit).all()
            for i in range(len(records)):
                methods = []
                for method in records[i].http_threshold_value:
                    methods.append(method.value)
                records[i] = standardizedData(records[i], ['http_threshold_value'])
                records[i]['methods'] = methods
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
                packet_in = data["requests"]['in'],
                packet_out = data["requests"]['out'],
                bandwidth_in = data['bandwidth']['in'],
                bandwidth_out = data['bandwidth']['out'],
                percent = data['percent'],
                description = data['description'],
                prevention = "Drop",
                status = data['status'],
                profile = data['profile'],
                type = "method"
            )
            session.add(http_threshold)
            try:
                session.commit()
                for line in data['methods']:
                    session.add(HttpThresholdValue(
                        http_threshold_id = http_threshold.id,
                        value = line
                    ))
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Add HTTP Method Threshold Success!","")
        except Exception as exp:
            raise (exp)
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


class HttpMethodThresholdAPI(Resource):

    def get(self,profile_id, method_threshold_id):
        try:
            session = Session()
            parameters = request.args
           
            record = session.query(HttpThreshold).filter(HttpThreshold.profile == profile_id).\
                filter(HttpThreshold.type == "method").filter_by(id = method_threshold_id).one()
            record = standardizedData(record)
            return status_code_200("", record)
        except Exception as exp:
            print (exp)
            return status_code_500("")
        finally:
            session.close()

    def put(self, profile_id, method_threshold_id):
        try:
            session = Session()
            parameters = request.args
            
            data = request.json
            error = verify_input(data)
            if error != "" or error is False:
                return status_code_400("Request Data Error!")
            if check_null(data) is False:
                return status_code_400("Request Data Error!")
            if "methods" in data:
                session.query(HttpThresholdValue).\
                    filter(HttpThresholdValue.http_threshold_id == method_threshold_id).delete()
                try:
                    session.commit()
                except Exception as exp:
                    print (exp)
                    session.rollback()
                    return status_code_500("Error!")
                for method in data['methods']:
                    http_threshold_value = HttpThresholdValue(
                        http_threshold_id = method_threshold_id,
                        value = method
                    )
                    session.add(http_threshold_value)
                    try:
                        session.commit()
                    except Exception as exp:
                        print (exp)
                        session.rollback()
                        return status_code_500("Error!")
                del data['methods']
            session.query(HttpThreshold).\
                filter(HttpThreshold.profile == profile_id).filter(HttpThreshold.type == "method").\
                filter(HttpThreshold.id == method_threshold_id).update(data)
            try:
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Edit HTTP Method Threshold Success!", "")
        except Exception as exp:
            print (exp)
            return status_code_500("")
        finally:
            session.close()

    def delete(self,profile_id, method_threshold_id):
        try:
            session = Session()
            parameters = request.args
            
            session.query(HttpThreshold).filter(HttpThreshold.profile == profile_id).\
                filter(HttpThreshold.type == "method").\
                filter(HttpThreshold.id == method_threshold_id).delete()
            try:
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Delete HTTP Method Threshold Success!", "")
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
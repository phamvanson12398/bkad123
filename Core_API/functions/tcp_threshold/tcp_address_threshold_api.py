from sqlalchemy import or_

from models.models import ConnectToDB, Network, GroupNetwork, TcpThreshold, TcpThresholdHaveNetworks, TcpThresholdHaveGroupNetworks
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()

class TcpAddressThresholdCollectionAPI(Resource):

    def get(self,profile_id):
        try:
            session = Session()
            parameters = request.args
            
            limit, page, offset, order = getDefault(
                parameters, TcpThreshold.__table__.columns, TcpThreshold
            )
            query = session.query(TcpThreshold).filter(TcpThreshold.profile == profile_id).\
                filter(TcpThreshold.type == "address")
            if "search" in parameters and parameters['search'] != "":
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    query = query.filter(or_(key.like('%'+ search_value +'%')\
                        for key in TcpThreshold.__table__.columns))
            total_count = query.count()
            records = query.order_by(order).offset(offset).limit(limit).all()
            for i in range(len(records)):
                networks = []
                for network in records[i].network:
                    network = standardizedData(
                        network, None, {'id': 'id',
                            'name': 'name'}
                    )
                    network['type'] = "obj"
                    networks.append(network)
                for group_network in records[i].group_network:
                    group_network = standardizedData(
                        group_network, None, {'id': 'id',
                                        'name': 'name'}
                    )
                    group_network['type'] = "gr_obj"
                    networks.append(group_network)
                records[i] = standardizedData(records[i], ['network', 'group_network'])
                records[i]['networks'] = networks
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
            tcp_threshold = TcpThreshold(
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
                type = "address"
            )
            for member in data['networks']:
                if member['type'] == "obj":
                    try:
                        network = session.query(Network).filter_by(id=int(member['id'])).one()
                    except Exception as exp:
                        return status_code_400('Not found member!')
                    tcp_threshold.network.append(network)
                else:
                    try:
                        group_network = session.query(GroupNetwork).\
                            filter_by(id=int(member['id'])).one()
                    except Exception as exp:
                        return status_code_400("Not found member!!")
                    tcp_threshold.group_network.append(group_network)
            session.add(tcp_threshold)
            try:
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Add Address Threshold Success!","")
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


class TcpAddressThresholdAPI(Resource):

    def get(self,profile_id, address_threshold_id):
        try:
            session = Session()
            parameters = request.args
            
            
            record = session.query(TcpThreshold).filter(TcpThreshold.profile == profile_id).\
                filter(TcpThreshold.type == "address").filter_by(id = address_threshold_id).one()
            networks = []
            for network in record.network:
                network = standardizedData(
                    network, None, {
                        'id': 'id',
                        'name': 'name'
                    })
                network['type'] = "obj"
                networks.append(network)
            for group_network in record.group_network:
                group_network = standardizedData(
                    group_network, None, {
                        'id': 'id',
                        'name': 'name'
                    })
                group_network['type'] = "gr_obj"
                networks.append(group_network)
            record = standardizedData(record, ['network', 'group_network'])
            record['networks'] = networks
            del record['type']
            return status_code_200("", record)
        except Exception as exp:
            print (exp)
            return status_code_500("")
        finally:
            session.close()

    def put(self,profile_id, address_threshold_id):
        try:
            session = Session()
            parameters = request.args
            
            data = request.json
            error = verify_input(data)
            if error != "" or error is False:
                return status_code_400("Request Data Error!")
            if check_null(data) is False:
                return status_code_400("Request Data Error!")
            if 'networks' in data:
                session.query(TcpThresholdHaveNetworks).\
                    filter(TcpThresholdHaveNetworks.tcp_threshold_id == address_threshold_id).delete()
                session.query(TcpThresholdHaveGroupNetworks).\
                    filter(TcpThresholdHaveGroupNetworks.tcp_threshold_id == address_threshold_id).delete()
                for member in data['networks']:
                    if member['type'] == "obj":
                        link = TcpThresholdHaveNetworks(
                            tcp_threshold_id=address_threshold_id,
                            network_id=member['id']
                        )
                    else:
                        link = TcpThresholdHaveGroupNetworks(
                            tcp_threshold_id=address_threshold_id,
                            group_network_id=member['id']
                        )
                    session.add(link)
                try:
                    session.commit()
                except Exception as exp:
                    session.rollback()
                    return status_code_400('Request data error!')
                del data['networks']
            session.query(TcpThreshold).\
                filter(TcpThreshold.profile == profile_id).filter(TcpThreshold.type == "address").\
                filter(TcpThreshold.id == address_threshold_id).update(data)
            try:
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Edit Address Threshold Success!", "")
        except Exception as exp:
            print (exp)
            return status_code_500("")
        finally:
            session.close()

    def delete(self,profile_id, address_threshold_id):
        try:
            session = Session()
            parameters = request.args
            
            session.query(TcpThreshold).filter(TcpThreshold.profile == profile_id).\
                filter(TcpThreshold.id == address_threshold_id).delete()
            try:
                session.commit()
            except Exception as exp:
                print (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Delete Address Threshold Success!", "")
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
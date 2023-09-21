import os
import sys
import re
import json
import time
import datetime
import calendar


from sqlalchemy import or_, and_
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import flask_excel as excel
from flask_jwt_extended import jwt_required

from libraries.status_code import *
from libraries.general import *
from libraries.general import getDefault, standardizedData, readfile, check_null
# from libraries.verify_input import *
from models.clh_model import ConnectToDB, CHConnect
# from models.service_model import VPNLogs, ConfigLogs, SystemResource, TrafficResource, ServiceLog

app = Flask(__name__)

Session = ConnectToDB()


# class VPNLogsAPI(Resource):
#
#     # @check_permission
#     def get(self):
#         try:
#             session = Session()
#             parameters = request.args
#             limit, page, offset, order, _from, _to = getPeriodTimeDefault(
#                 parameters, VPNLogs.__table__.columns, VPNLogs
#             )
#             query = session.query(VPNLogs)
#             if 'search' in parameters:
#                 search_values = parameters['search'].split(",")
#                 for search_value in search_values:
#                     query = query.filter(
#                         or_(key.like('%' + search_value + '%') for key in VPNLogs.__table__.columns)
#                     )
#             query = query.filter(VPNLogs.datetime.between(_from, _to))
#
#             total_count = query.count()
#             records = query.order_by(order).offset(offset).limit(limit).all()
#             for i in range(len(records)):
#                 records[i] = General.standardizedData(records[i])
#                 records[i]['info'] = ["test info line 1", "test info line 2"]
#             return status_code_200('', get_data_with_page(records, limit, page, total_count))
#         except Exception as exp:
#             return status_code_500(exp)
#         finally:
#             session.close()
#
#     def post(self):
#         try:
#             session = Session()
#             data = request.json
#
#             data = convert_none_to_string(data)
#
#             if session.query(session.query(VPNLogs).filter(VPNLogs.port == data['port']) \
#                                      .filter(VPNLogs.event == data['event']) \
#                                      .filter(VPNLogs.datetime == data['datetime']) \
#                                      .exists()).scalar():
#                 return status_code_500("Check duplicated log")
#
#             # update user_name
#
#             session.query(VPNLogs).filter(VPNLogs.port == data['port']) \
#                 .filter(VPNLogs.ip_address == data['ip_address']) \
#                 .update({'user': data['user']})
#
#             my_log = VPNLogs(
#                 datetime=data['datetime'],
#                 user=data['user'],
#                 ip_address=data['ip_address'],
#                 ip_vpn=data['ip_vpn'],
#                 type=data['type'],
#                 tunnel=data['tunnel'],
#                 event=data['event'],
#                 port=data['port'],
#                 country=data['country']
#
#             )
#             session.add(my_log)
#
#             try:
#                 session.commit()
#             except Exception as exp:
#                 print(exp)
#                 session.rollback()
#                 return status_code_500("Check duplicated username")
#
#             return status_code_200('', {'id': my_log.id})
#         except Exception as exp:
#             return status_code_500(exp)
#         finally:
#             session.close()
#
#
# class VPNLogsDownloadAPI(Resource):
#
#     # @check_permission
#     def get(self):
#         try:
#             session = Session()
#             parameters = request.args
#             limit, page, offset, order, _from, _to = getPeriodTimeDefault(
#                 parameters, VPNLogs.__table__.columns, VPNLogs
#             )
#             query = session.query(VPNLogs)
#             if 'search' in parameters:
#                 search_values = parameters['search'].split(",")
#                 for search_value in search_values:
#                     query = query.filter(
#                         or_(key.like('%' + search_value + '%') for key in VPNLogs.__table__.columns)
#                     )
#             query = query.filter(VPNLogs.datetime.between(_from, _to)) \
#                 .order_by(order)
#             total_count = query.count()
#             records = query.all()
#             for i in range(len(records)):
#                 records[i] = General.standardizedData(records[i])
#
#             for i in range(len(records)):
#                 records[i] = {
#                     "No": records[i]['id'],
#                     "Date": records[i]['datetime'],
#                     "User": records[i]['user'],
#                     "IP Address": records[i]['ip_address'],
#                     "IP VPN": records[i]['ip_vpn'],
#                     "Type": records[i]['type'],
#                     "Tunnel": records[i]['tunnel'],
#                     "Event": records[i]['event']
#                 }
#             return excel.make_response_from_records(records, "csv", file_name="bvg_vpn_logs")
#         except Exception as exp:
#             return status_code_500(exp)
#         finally:
#             session.close()


# class ConfigLogsAPI(Resource):
#
#     # @check_permission
#     def get(self):
#         try:
#             session = Session()
#             parameters = request.args
#             limit, page, offset, order, _from, _to = getPeriodTimeDefault(
#                 parameters, ConfigLogs.__table__.columns, ConfigLogs
#             )
#             query = session.query(ConfigLogs)
#             if 'search' in parameters and parameters['search'] != '':
#                 search_values = parameters['search'].split(",")
#                 for search_value in search_values:
#                     query = query.filter(
#                         or_(key.like('%' + search_value + '%') for key in ConfigLogs.__table__.columns)
#                     )
#             query = query.filter(ConfigLogs.datetime.between(_from, _to))
#
#             total_count = query.count()
#             records = query.order_by(order).offset(offset).limit(limit).all()
#             for i in range(len(records)):
#                 records[i] = General.standardizedData(records[i])
#                 records[i]['info'] = ["test info line 1", "test info line 2"]
#             return status_code_200('', get_data_with_page(records, limit, page, total_count))
#         except Exception as exp:
#             return status_code_500(exp)
#         finally:
#             session.close()
#
#
# class ConfigLogsDownloadAPI(Resource):
#
#     # @check_permission
#     def get(self):
#         try:
#             session = Session()
#             parameters = request.args
#             limit, page, offset, order, _from, _to = getPeriodTimeDefault(
#                 parameters, ConfigLogs.__table__.columns, ConfigLogs
#             )
#             query = session.query(ConfigLogs)
#             if 'search' in parameters:
#                 search_values = parameters['search'].split(",")
#                 for search_value in search_values:
#                     query = query.filter(
#                         or_(key.like('%' + search_value + '%') for key in ConfigLogs.__table__.columns)
#                     )
#             query = query.filter(ConfigLogs.datetime.between(_from, _to)) \
#                 .order_by(order)
#             total_count = query.count()
#             records = query.all()
#             for i in range(len(records)):
#                 records[i] = General.standardizedData(records[i])
#
#             for i in range(len(records)):
#                 records[i] = {
#                     "No": records[i]['id'],
#                     "Date": records[i]['datetime'],
#                     "User": records[i]['user'],
#                     "IP Address": records[i]['ip_address'],
#                     "Action": records[i]['action'],
#                     "Contents": records[i]['content']
#                 }
#             return excel.make_response_from_records(records, "csv", file_name="bvg_config_logs")
#         except Exception as exp:
#             return status_code_500(exp)
#         finally:
#             session.close()


class SystemResourceAPI(Resource):

    # @check_permission
    def get(self):
        # return "123"
        try:
            # session = Session()
            parameters = request.args

            _from, _to = getPeriodTimeDefault2(
                parameters,
            )

            t1 = time.time()

            conn = CHConnect()
            data = conn.execute(
                "select cpu,ram,disk,datetime from bvg.system_resource where datetime > '{_from}' and datetime < '{_to}'".
                format(_from=_from, _to=_to))

            t2 = time.time()
            # for i in data:
            # 	del data['date']
            # 	del data['datetime']
            newdata = []
            for i in range(len(data)):
                tmp = {}
                tmp['cpu'] = data[i][0]
                tmp['ram'] = data[i][1]
                tmp['disk'] = data[i][2]
                tmp['datetime'] = str(data[i][3])
                newdata.append(tmp)
            t3 = time.time()
            print("######################################## ", t2 - t1, t3 - t2, t3 - t1, len(newdata))
            print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF!!!!!!!!!!!!!!!!!!!")
            print(len(newdata))
            check = General.get_average_data(newdata, 30, ["cpu", "ram", "disk"])
            print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC", check)
            return status_code_200('', check)

        # 	limit, page, offset, order, _from, _to = getPeriodTimeDefault(
        # 		parameters, SystemResource.__table__.columns, SystemResource
        # 	)

        # 	query = session.query(SystemResource)
        # 	if 'search' in parameters:
        # 		search_values = parameters['search'].split(",")
        # 		for search_value in search_values:
        # 			query = query.filter(
        # 				or_(key.like('%'+ search_value +'%') for key in SystemResource.__table__.columns)
        # 			)
        # 	query = query.filter(SystemResource.datetime.between(_from, _to))
        # 				 # .order_by(order).offset(offset).limit(limit)
        # 	total_count = query.count()
        # 	records = query.limit(1000).all()
        # 	for i in range(len(records)):
        # 		records[i] = General.standardizedData(records[i])
        # 	records = General.get_average_data(records, 50, ["ram", "cpu"])
        # 	return status_code_200('',records)
        except Exception as exp:
            raise (exp)
            return status_code_500(exp)
        # finally:
            # session.close()

    def post(self):
        try:
            session = Session()
            data = request.json

            data = convert_none_to_string(data)
            # missingParam = checkMissingParam(aparam, data)
            # if missingParam != '':
            # 	return status_code_400("Missing :" + missingParam)

            current_time = datetime.datetime.now()

            resource = SystemResource(
                cpu=data['cpu'],
                ram=data['ram'],
                disk=0,
                datetime=current_time
            )

            session.add(resource)

            try:
                session.commit()
            except Exception as exp:
                print(exp)
                session.rollback()
                return status_code_500("Check duplicated username")

            return status_code_200('', {'id': resource.id})
        except Exception as exp:
            return status_code_500(exp)
        finally:
            session.close()


class SystemResourceDownloadAPI(Resource):

    # @check_permission
    def get(self):
        try:
            session = Session()
            parameters = request.args
            limit, page, offset, order, _from, _to = getPeriodTimeDefault(
                parameters, SystemResource.__table__.columns, SystemResource
            )
            query = session.query(SystemResource)
            if 'search' in parameters:
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    query = query.filter(
                        or_(key.like('%' + search_value + '%') for key in SystemResource.__table__.columns)
                    )
            query = query.filter(SystemResource.datetime.between(_from, _to)) \
                .order_by(order)

            total_count = query.count()
            records = query.all()
            for i in range(len(records)):
                records[i] = General.standardizedData(records[i])

            for i in range(len(records)):
                records[i] = {
                    "No": records[i]['id'],
                    "Date": records[i]['datetime'],
                    "RAM": records[i]['ram'],
                    "CPU": records[i]['cpu'],
                    "Disk": records[i]['disk']
                }

            return excel.make_response_from_records(records, "csv", file_name="bvg_system_resource")
        except Exception as exp:
            return status_code_500(exp)
        finally:
            session.close()


class TrafficResourceAPI(Resource):

    # @check_permission
    def get(self):
        # return "123"
        try:
            session = ConnectDB()()
            parameters = request.args

            order, _from, _to = getPeriodTimeDefault2(
                parameters, SystemResource.__table__.columns, SystemResource
            )

            t1 = time.time()

            conn = CHConnect()
            data = conn.execute(
                "select input,output,interface,datetime from bvg.traffic_resource where datetime > '{_from}' and datetime < '{_to}'".
                format(_from=_from, _to=_to))

            t2 = time.time()

            newdata = []
            for i in range(len(data)):
                tmp = {}
                tmp['input'] = data[i][0]
                tmp['output'] = data[i][1]
                tmp['interface'] = data[i][2]
                tmp['datetime'] = str(data[i][3])
                newdata.append(tmp)
            t3 = time.time()
            check = General.get_average_data(newdata, 30, ["input", "output"])
            print("######################################## ", t2 - t1, t3 - t2, t3 - t1, len(newdata))
            return status_code_200('', check)











        # limit, page, offset, order, _from, _to = getPeriodTimeDefault(
        # 	parameters, TrafficResource.__table__.columns, TrafficResource
        # )
        # query = session.query(TrafficResource)
        # if 'search' in parameters and search != '':
        # 	search_values = parameters['search'].split(",")
        # 	for search_value in search_values:
        # 		query = query.filter(
        # 			or_(key.like('%'+ search_value +'%')\
        # 				for key in TrafficResource.__table__.columns)
        # 		)

        # if 'interface' in parameters:
        # 	try:
        # 		interface = parameters['interface']
        # 		interface = json.loads(interface)
        # 		query = query.filter(TrafficResource.interface.in_(interface))
        # 	except Exception as exp:
        # 		raise(exp)
        # 		pass

        # query = query.filter(TrafficResource.datetime.between(_from, _to))

        # total_count = query.count()
        # records = query.limit(1000).all()
        # _records = {}
        # for i in range(len(records)):
        # 	records[i] = General.standardizedData(records[i])
        # 	if records[i]['interface'] not in _records:
        # 		_records[records[i]['interface']] = []
        # 	_records[records[i]['interface']].append(records[i])
        # arr = []
        # for record in _records:
        # 	arr += General.get_average_data(_records[record], 50, ["input", "output"])
        # session.close()
        # return status_code_200('', arr)
        except Exception as exp:
            raise (exp)
            session.close()
            return status_code_500(exp)
        finally:
            session.close()

    def post(self):
        try:
            session = Session()
            data = request.json
            # return str(data)

            data = convert_none_to_string(data)
            # missingParam = checkMissingParam(aparam, data)
            # if missingParam != '':
            # 	return status_code_400("Missing :" + missingParam)

            current_time = datetime.datetime.now()

            traffic = TrafficResource(
                input=data['input'],
                output=data['output'],
                interface=data["interface"],
                datetime=current_time
            )

            session.add(traffic)

            try:
                session.commit()
            except Exception as exp:
                print(exp)
                session.rollback()
                return status_code_500("Check duplicated username")

            return status_code_200('', {'id': traffic.id})
        except Exception as exp:
            raise (exp)
            return status_code_500(exp)
        finally:
            session.close()


class TrafficResourceDownloadAPI(Resource):

    # @check_permission
    def get(self):
        try:
            session = Session()
            parameters = request.args
            limit, page, offset, order, _from, _to = getPeriodTimeDefault(
                parameters, TrafficResource.__table__.columns, TrafficResource
            )

            query = session.query(TrafficResource)
            if 'search' in parameters:
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    query = query.filter(
                        or_(key.like('%' + search_value + '%') for key in TrafficResource.__table__.columns)
                    )
            query = query.filter(TrafficResource.datetime.between(_from, _to)) \
                .order_by(order)
            total_count = query.count()
            records = query.all()
            for i in range(len(records)):
                records[i] = General.standardizedData(records[i])

            for i in range(len(records)):
                records[i] = {
                    "No": records[i]['id'],
                    "Date": records[i]['datetime'],
                    "Incoming Traffic": records[i]['input'],
                    "Outgoing Traffic": records[i]['output']
                }
            return excel.make_response_from_records(records, "csv", file_name="bvg_traffic_resource")
        except Exception as exp:
            return status_code_500(exp)
        finally:
            session.close()


class ServiceLogs(Resource):

    # @check_permission
    def get(self):
        try:
            session = Session()
            parameters = request.args

            query = session.query(ServiceLog)
            if 'search' in parameters:
                pass

            records = query.filter(ServiceLog.status == 1).all()

            for i in range(len(records)):
                records[i] = General.standardizedData(records[i], None, {"id": "id", "name": "name", "type": "type"})
            pptp_logs = []
            l2tp_logs = []
            opencon_logs = []
            openvpn_logs = []
            system_log = []
            for i in records:
                if i["type"] == "PPTP Logs":
                    pptp_logs.append(i)
                elif i["type"] == "L2TP Logs":
                    l2tp_logs.append(i)
                elif i["type"] == "OpenConnect Logs":
                    opencon_logs.append(i)
                elif i["type"] == "OpenVPN Logs":
                    openvpn_logs.append(i)
                else:
                    system_log.append(i)

            result = {
                "list_type": ["PPTP Logs", "L2TP Logs", "OpenConnect Logs", "OpenVPN Logs", "System Logs"],
                "list_file": {
                    "PPTP Logs": pptp_logs,
                    "L2TP Logs": l2tp_logs,
                    "OpenConnect Logs": opencon_logs,
                    "OpenVPN Logs": openvpn_logs,
                    "System Logs": system_log

                }
            }

            return status_code_200('', result)
        except Exception as exp:
            return status_code_500(exp)
        finally:
            session.close()

    # @check_permission
    def post(self):
        try:
            session = Session()
            parameters = request.args

            query = session.query(ServiceLog)
            if 'search' in parameters:
                pass

            records = query.all()

            for i in range(len(records)):
                records[i] = General.standardizedData(records[i], None, {"id": "id", "name": "name", "type": "type",
                                                                         "directory": "directory", "status": "status",
                                                                         "watched": "watched"})

            return status_code_200('', records)
        except Exception as exp:
            return status_code_500(exp)
        finally:
            session.close()


class UpdateWatched(Resource):

    # @check_permission
    def put(self, logfile_id):
        try:
            session = Session()
            data = request.json
            if data == None:
                return status_code_400("Missing data")
            if "watched" not in data:
                return status_code_500("Missing watched variable")

            session.query(ServiceLog).filter(ServiceLog.id == logfile_id).update({"watched": data["watched"]})
            try:
                session.commit()
            except Exception as exp:
                print(exp)
                session.rollback()
                return status_code_500("Error!")
            return status_code_200('', "")
        except Exception as exp:
            raise (exp)
            return status_code_500(exp)
        finally:
            session.close()


def getPeriodTimeDefault2(parameters):
    parameters = parameters.to_dict()
    if (('type' and 'time') or ('from' and 'to')) not in parameters:
        parameters['type'] = 'minutes'
        parameters['time'] = 1
    if ('type' and 'time') in parameters:
        time_to, time_from = get_time(parameters['type'], parameters['time'])

    elif ('from' and 'to') in parameters:
        time_from = parameters['from']
        time_to = parameters['to']
    else:
        time_to = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print (time_to,"to")
        time_from = datetime.datetime.fromtimestamp(0).strftime('%Y-%m-%d %H:%M:%S')

    return  time_from, time_to

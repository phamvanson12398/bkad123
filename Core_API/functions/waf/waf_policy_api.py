from sqlalchemy import or_

from models.models import ConnectToDB, WafPolicy, GroupWebsites, WafPolicyHaveGroupWebsites
from libraries.general import getDefault, standardizedData, check_null
from libraries.status_code import *

from flask import request
from flask_restful import Resource

Session = ConnectToDB()


class WafPolicyCollectionAPI(Resource):

    def get(self,profile_id):
        try:
            session = Session()
            parameters = request.args
            limit, page, offset, order = getDefault(
                parameters, WafPolicy.__table__.columns, WafPolicy
            )
            query = session.query(WafPolicy).filter(WafPolicy.profile == profile_id)
            if "search" in parameters and parameters['search'] != "":
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    query = query.filter(or_(key.like('%'+ search_value +'%')\
                        for key in WafPolicy.__table__.columns))
            total_count = query.count()
            records = query.order_by(order).offset(offset).limit(limit).all()
            for i in range(len(records)):
                print(records[i].status)
                group_websites = []
                for group_website in records[i].group_websites:
                    group_website = standardizedData(
                        group_website, None, {'id': 'id', 'name': 'name', 'description': 'description'}
                    )
                    group_websites.append(group_website)
                records[i] = standardizedData(records[i], ["group_websites"])
                records[i]['group_websites'] = group_websites
                records[i]['policy_enable'] = records[i]['policy_enable'].split(",")
            return status_code_200("", get_data_with_page(records, limit, page, total_count))
        except Exception as exp:
            raise (exp)
            return status_code_500("")
        finally:
            session.close()

    def post(self, profile_id):
        try:
            session = Session()
            parameters = request.args
            data = request.get_json()
            if "policy_enable" in data:
                data['policy_enable'] = ",".join(str(i) for i in data['policy_enable'])
            else:
                data['policy_enable'] = ""
            waf_policy = WafPolicy(
                name=data['name'],
                policy_enable=data['policy_enable'],
                profile=profile_id
            )
            for group_website_id in data['group_websites']:
                try:
                    group_website = session.query(GroupWebsites).filter_by(id=int(group_website_id)).one()
                except Exception as exp:
                    return status_code_400('Not found member!')
                waf_policy.group_websites.append(group_website)
            session.add(waf_policy)
            try:
                session.commit()
            except Exception as exp:
                print(exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("", "")
        except Exception as exp:
            raise (exp)
            return status_code_500("")
        finally:
            session.close()


class WafPolicyAPI(Resource):

    def get(self, profile_id, waf_policy_id):
        try:
            session = Session()
            parameters = request.args
            record = session.query(WafPolicy).filter(WafPolicy.profile == profile_id).filter_by(id=waf_policy_id).one()
            group_websites = []
            for group_website in record.group_websites:
                group_website = standardizedData(
                    group_website, None, {'id': 'id', 'name': 'name', 'description': 'description'}
                )
                group_websites.append(group_website)
            record = standardizedData(record, ["group_websites"])
            record['policy_enable'] = record['policy_enable'].split(",")
            record['group_websites'] = group_websites
            return status_code_200("", record)
        except Exception as exp:
            raise (exp)
            return status_code_500("")
        finally:
            session.close()

    def put(self, profile_id, waf_policy_id):
        try:
            session = Session()
            parameters = request.args
            data = request.json
            error = verify_input(data)
            if error != "" or error is False:
                return status_code_400("Request Data Error!")
            if check_null(data) is False:
                return status_code_400("Request Data Error!")
            if 'group_websites' in data:
                session.query(WafPolicyHaveGroupWebsites). \
                    filter(WafPolicyHaveGroupWebsites.waf_policy_id == waf_policy_id).delete()
                for group_websites in data['group_websites']:
                    link = WafPolicyHaveGroupWebsites(
                        group_website_id=group_websites,
                        waf_policy_id=waf_policy_id
                    )
                    session.add(link)
                try:
                    session.commit()
                except Exception as exp:
                    session.rollback()
                    return status_code_400('Request data error!')
                del data['group_websites']
            if "policy_enable" in data:
                data['policy_enable'] = ','.join(i for i in data['policy_enable'])
            print("Flag 2")
            print("data", data)
            session.query(WafPolicy).filter(WafPolicy.profile == profile_id). \
                filter(WafPolicy.id == waf_policy_id).update(data)
            try:
                session.commit()
            except Exception as exp:
                raise (exp)
                session.rollback()
                return status_code_500("")
            return status_code_200("Success!", "")
        except Exception as exp:
            raise (exp)
            return status_code_500("")
        finally:
            session.close()

    def delete(self, profile_id, waf_policy_id):
        try:
            session = Session()
            session.query(WafPolicyHaveGroupWebsites). \
                filter(WafPolicyHaveGroupWebsites.waf_policy_id == waf_policy_id).delete()
            session.query(WafPolicy). \
                filter(WafPolicy.profile == profile_id). \
                filter(WafPolicy.id == waf_policy_id).delete()
            try:
                session.commit()
                return status_code_200("Success!", "")
            except Exception as exp:
                raise (exp)
                session.rollback()
                return status_code_500("")
        except Exception as exp:
            raise (exp)
            return status_code_500("")
        finally:
            session.close()


def verify_input(data):
    try:
        str_error = ""
        return str_error
    except Exception as exp:
        print(exp)
        return False

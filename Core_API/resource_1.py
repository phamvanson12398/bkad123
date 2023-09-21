from flask import Flask
from flask_restful import Resource, Api

from functions.websites.websites_api import WebsitesCollectionAPI, WebsitesAPI
from functions.GroupWebsites.group_websites_api import GroupWebsitesCollectionAPI, GroupWebsitesAPI
from functions.ADProfile.ad_profile_api import ADProfileCollectionAPI, ADProfileAPI
from functions.LearningMode.learning_mode_api import LearningModeCollectionAPI, LearningModeAPI
from functions.ATAS.atas_api import ATASCollectionAPI, ATASAPI
from functions.network.network_api import NetworkCollectionAPI, NetworkAPI
from functions.group_network.group_network_api import GroupNetworkCollectionAPI, GroupNetworkAPI, NetworkGroupNetwork
from functions.ad_policy.ad_policy_api import ADPolicyCollectionAPI, ADPolicyAPI
from functions.network_interface.network_interface_api import InterfacesCollectionAPI, InterfacesAPI
from functions.network_nat.network_nat_api import NatCollectionAPI, NatAPI
# from functions.network_load_balancing.network_load_balancing_api import LoadBalancingCollectionAPI
# from functions.report_schedule.report_schedule_api import ReportScheduleCollectionAPI, ReportScheduleAPI
from functions.tcp_general.tcp_general_api import TcpGeneralCollectionAPI, TcpGeneralAPI
from functions.tcp_slowcnn.tcp_slowcnn_api import  TcpSlowConnectionCollectionAPI, TcpSlowConnectionAPI
from functions.service.service_api import ServiceCollectionAPI, ServiceAPI
from functions.group_service.group_service_api import GroupServiceCollectionAPI, GroupServiceAPI
from functions.tcp_threshold.tcp_protocol_threshold_api import TcpProtocolThresholdCollectionAPI, TcpProtocolThresholdAPI
from functions.tcp_threshold.tcp_address_threshold_api import TcpAddressThresholdCollectionAPI, TcpAddressThresholdAPI
from functions.tcp_threshold.tcp_other_threshold_api import TcpOtherThresholdCollectionAPI, TcpOtherThresholdAPI
from functions.http_threshold.http_slowcnn_api import  HttpSlowConnectionCollectionAPI, HttpSlowConnectionAPI
from functions.http_threshold.http_general_api import HttpGeneralCollectionAPI, HttpGeneralAPI
from functions.http_threshold.http_method_threshold_api import HttpMethodThresholdCollectionAPI, HttpMethodThresholdAPI
from functions.http_threshold.http_url_threshold_api import HttpUrlThresholdCollectionAPI, HttpUrlThresholdAPI
from functions.http_threshold.http_host_threshold_api import HttpHostThresholdCollectionAPI, HttpHostThresholdAPI
from functions.http_threshold.http_cookie_threshold_api import HttpCookieThresholdCollectionAPI, HttpCookieThresholdAPI
from functions.http_threshold.http_agent_threshold_api import HttpAgentThresholdCollectionAPI, HttpAgentThresholdAPI
from functions.ATAS.protocol_statistic_api import ATASProtocolDataStatisticCollectionAPI, ATASAddressDataStatisticCollectionAPI, ATASOthersDataStatisticCollectionAPI
from functions.data_statistic.protocol_statistic_api import ProtocolDataStatisticCollectionAPI, AddressDataStatisticCollectionAPI, OthersDataStatisticCollectionAPI
from functions.ATAS.http_statistic_api import ATASMethodDataStatisticCollectionAPI, ATASUrlDataStatisticCollectionAPI, ATASCookieDataStatisticCollectionAPI, ATASAgentDataStatisticCollectionAPI, ATASHostDataStatisticCollectionAPI
from functions.data_statistic.http_statistic_api import MethodDataStatisticCollectionAPI, UrlDataStatisticCollectionAPI, CookieDataStatisticCollectionAPI, AgentDataStatisticCollectionAPI, HostDataStatisticCollectionAPI
from functions.routes.routes_api import RoutesCollectionAPI, RoutesAPI
from functions.high_availability_mode.high_availability_mode_api import HA_Mode_API, HA_API
from functions.network_load_balancing.network_load_balancing_api import LoadBalancingCollectionAPI
from functions.report_schedule.report_schedule_api import ReportScheduleCollectionAPI, ReportScheduleAPI
from functions.report_schedule.emegency_api import EmegencyCollectionAPI, EmegencyScheduleAPI
from functions.system_users.system_users_api import UsersCollectionAPI, UserAPI
from functions.backup_and_restore.backup_and_restore_api import BackUpAPI, BackUpAPIs, BackUpPlanAPI, Restore
from functions.datetime.datetime_api import DateTimeAPI
from functions.access_control_list.access_control_list_api import AccessControlListCollectionAPI, AccessControlListAPI
from functions.firewall_access.firewall_access_api import FirewallAccessCollectionAPI, FirewallAccessAPI
from functions.operating_mode.operating_mode import Operating_modeAPI
from functions.ACSH.ACSH_api import ACSHCollectionAPI, ACSHAPI
from functions.static.statics import ImageData,BackupData
from functions.signature.signature_api import SignatureCollectionAPI, SignatureAPI
from functions.Abnormal.abnormal_api import AbnormalCollectionAPI, AbnormalAPI
from functions.other_feature.get_option_value_api import TcpOtherOptionsAPI
from functions.waf.policy_api import WafPolicyListCollectionAPI
from functions.waf.waf_policy_api import WafPolicyCollectionAPI, WafPolicyAPI
from functions.monitoring.monitoring_api import SystemResourceAPI, TrafficResourceAPI

from flask_cors import CORS
import logging, logging.config, yaml
logging.config.dictConfig(yaml.load(open('logging.conf')))
logfile    = logging.getLogger('file')
logconsole = logging.getLogger('console')
logfile.debug("Debug FILE")
logconsole.debug("Debug CONSOLE")




app = Flask(__name__)
api = Api(app)



CORS(app)

# Resource Websites
api.add_resource(WebsitesCollectionAPI, '/api/websites', methods = ['GET', 'POST'])
api.add_resource(WebsitesAPI, '/api/websites/<int:website_id>', methods = ['GET', 'PUT', 'DELETE'])

# Reosurce Group Website
api.add_resource(GroupWebsitesCollectionAPI, '/api/group_websites', methods = ['GET', 'POST'])
api.add_resource(GroupWebsitesAPI, '/api/group_websites/<int:group_website_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource AD Profile
api.add_resource(ADProfileCollectionAPI, '/api/ad_profile', methods = ['GET', 'POST'])
api.add_resource(ADProfileAPI, '/api/ad_profile/<int:profile_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource Learning Mode 
api.add_resource(LearningModeCollectionAPI, '/api/learning_mode', methods = ['GET', 'POST'])
api.add_resource(LearningModeAPI, '/api/learning_mode/<int:learning_mode_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource ATAS
api.add_resource(ATASCollectionAPI, '/api/atas', methods = ['GET', 'POST'])
api.add_resource(ATASAPI, '/api/atas/<int:atas_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resoure Network
api.add_resource(NetworkCollectionAPI, '/api/networks', methods = ['GET', 'POST'])
api.add_resource(NetworkAPI, '/api/networks/<int:network_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource Group Network
api.add_resource(GroupNetworkCollectionAPI, '/api/group_networks', methods = ['GET', 'POST'])
api.add_resource(GroupNetworkAPI, '/api/group_networks/<int:group_network_id>', methods = ['GET', 'PUT', 'DELETE'])
api.add_resource(NetworkGroupNetwork, '/api/net_and_gnet', methods = ['GET'])

# Resource AD Policy
api.add_resource(ADPolicyCollectionAPI, '/api/ad_policy', methods = ['GET', 'POST'])
api.add_resource(ADPolicyAPI, '/api/ad_policy/<int:ad_policy_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource Network Interface
api.add_resource(InterfacesCollectionAPI, '/api/interfaces', methods=['GET', 'POST'])
api.add_resource(InterfacesAPI, '/api/interfaces/<int:interface_id>', methods = ['GET', 'PUT', 'DELETE'])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

# Resource Nat 
api.add_resource(NatCollectionAPI, '/api/nat', methods=['GET', 'POST'])
api.add_resource(NatAPI, '/api/nat/<int:nat_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource Load Balancing 
# api.add_resource(LoadBalancingCollectionAPI, '/api/loadbalancing', methods=['GET', 'POST', 'PUT'])

# Resource report schedule 
# api.add_resource(ReportScheduleCollectionAPI, '/api/report', methods=['GET', 'POST'])
# api.add_resource(ReportScheduleAPI, '/api/report/<int:report_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource Services
api.add_resource(ServiceCollectionAPI, '/api/services', methods=['GET', 'POST'])
api.add_resource(ServiceAPI, '/api/services/<int:service_id>', methods=['GET', 'PUT', 'DELETE'])

# Group Service
api.add_resource(GroupServiceCollectionAPI, '/api/group_services', methods=['GET', 'POST'])
api.add_resource(GroupServiceAPI, '/api/group_services/<int:group_service_id>', methods=['GET', 'PUT', 'DELETE'])

# Resource Tcp General
api.add_resource(TcpGeneralCollectionAPI, '/api/profile/<int:profile_id>/tcp/general', methods=['GET'])
api.add_resource(TcpGeneralAPI, '/api/profile/<int:profile_id>/tcp/general/<int:tcp_general_id>', methods=['GET', 'PUT'])

# Resource Tcp SlowConnection
api.add_resource(TcpSlowConnectionCollectionAPI, '/api/profile/<int:profile_id>/tcp/slowcn', methods=['GET'])
api.add_resource(TcpSlowConnectionAPI, '/api/profile/<int:profile_id>/tcp/slowcn/<int:tcp_slowcn_id>', methods=['GET', 'PUT'])

# Tcp Protocol Threshold
api.add_resource(TcpProtocolThresholdCollectionAPI, '/api/profile/<int:profile_id>/tcp/protocol', methods=['GET', 'POST'])
api.add_resource(TcpProtocolThresholdAPI, '/api/profile/<int:profile_id>/tcp/protocol/<int:protocol_threshold_id>', methods=['GET', 'PUT', 'DELETE'])

# Tcp Address Threshold
api.add_resource(TcpAddressThresholdCollectionAPI, '/api/profile/<int:profile_id>/tcp/address', methods=['GET', 'POST'])
api.add_resource(TcpAddressThresholdAPI, '/api/profile/<int:profile_id>/tcp/address/<int:address_threshold_id>', methods=['GET', 'PUT', 'DELETE'])

# Tcp Other Threshold
api.add_resource(TcpOtherThresholdCollectionAPI, '/api/profile/<int:profile_id>/tcp/other', methods=['GET', 'POST'])
api.add_resource(TcpOtherThresholdAPI, '/api/profile/<int:profile_id>/tcp/other/<int:other_threshold_id>', methods=['GET', 'PUT', 'DELETE'])


# Resource HTTP SlowConnection
api.add_resource(HttpSlowConnectionCollectionAPI, '/api/profile/<int:profile_id>/http/slowcn', methods=['GET'])
api.add_resource(HttpSlowConnectionAPI, '/api/profile/<int:profile_id>/http/slowcn/<int:http_slowcnn_id>', methods=['GET', 'PUT'])


# Resource HTTP General
api.add_resource(HttpGeneralCollectionAPI, '/api/profile/<int:profile_id>/http/general', methods=['GET','POST'])
api.add_resource(HttpGeneralAPI, '/api/profile/<int:profile_id>/http/general/<int:http_general_id>', methods=['GET', 'PUT'])


# Http Method Threshold
api.add_resource(HttpMethodThresholdCollectionAPI, '/api/profile/<int:profile_id>/http/method', methods=['GET', 'POST'])
api.add_resource(HttpMethodThresholdAPI, '/api/profile/<int:profile_id>/http/method/<int:method_threshold_id>', methods=['GET', 'PUT', 'DELETE'])

# Http Url Threshold
api.add_resource(HttpUrlThresholdCollectionAPI, '/api/profile/<int:profile_id>/http/url', methods=['GET', 'POST'])
api.add_resource(HttpUrlThresholdAPI, '/api/profile/<int:profile_id>/http/url/<int:url_threshold_id>', methods=['GET', 'PUT', 'DELETE'])

# Http Host Threshold
api.add_resource(HttpHostThresholdCollectionAPI, '/api/profile/<int:profile_id>/http/host', methods=['GET', 'POST'])
api.add_resource(HttpHostThresholdAPI, '/api/profile/<int:profile_id>/http/host/<int:host_threshold_id>', methods=['GET', 'PUT', 'DELETE'])

# Http Cookie Threshold
api.add_resource(HttpCookieThresholdCollectionAPI, '/api/profile/<int:profile_id>/http/cookie', methods=['GET', 'POST'])
api.add_resource(HttpCookieThresholdAPI, '/api/profile/<int:profile_id>/http/cookie/<int:cookie_threshold_id>', methods=['GET', 'PUT'])

# Http Agent Threshold
api.add_resource(HttpAgentThresholdCollectionAPI, '/api/profile/<int:profile_id>/http/agent', methods=['GET', 'POST'])
api.add_resource(HttpAgentThresholdAPI, '/api/profile/<int:profile_id>/http/agent/<int:agent_threshold_id>', methods=['GET', 'PUT', 'DELETE'])

# Tcp Data Statistic
api.add_resource(ProtocolDataStatisticCollectionAPI, '/api/monitoring/protocol', methods=['GET'])
api.add_resource(ATASProtocolDataStatisticCollectionAPI, '/api/atas/statistic/protocol', methods=['GET'])
api.add_resource(ATASAddressDataStatisticCollectionAPI, '/api/atas/statistic/address', methods=['GET'])
api.add_resource(AddressDataStatisticCollectionAPI, '/api/monitoring/address', methods=['GET'])
api.add_resource(ATASOthersDataStatisticCollectionAPI, '/api/atas/statistic/other', methods=['GET'])
api.add_resource(OthersDataStatisticCollectionAPI, '/api/monitoring/other', methods=['GET'])

# Http Data Statistic
api.add_resource(MethodDataStatisticCollectionAPI, '/api/monitoring/methods', methods=['GET'])
api.add_resource(ATASMethodDataStatisticCollectionAPI, '/api/atas/statistic/methods', methods=['GET'])
api.add_resource(UrlDataStatisticCollectionAPI, '/api/monitoring/urls', methods=['GET'])
api.add_resource(ATASUrlDataStatisticCollectionAPI, '/api/atas/statistic/urls', methods=['GET'])
api.add_resource(CookieDataStatisticCollectionAPI, '/api/monitoring/cookies', methods=['GET'])
api.add_resource(ATASCookieDataStatisticCollectionAPI, '/api/atas/statistic/cookies', methods=['GET'])
api.add_resource(AgentDataStatisticCollectionAPI, '/api/monitoring/agents', methods=['GET'])
api.add_resource(ATASAgentDataStatisticCollectionAPI, '/api/atas/statistic/agents', methods=['GET'])
api.add_resource(HostDataStatisticCollectionAPI, '/api/monitoring/host', methods=['GET'])
api.add_resource(ATASHostDataStatisticCollectionAPI, '/api/atas/statistic/host', methods=['GET'])

# Routes 
api.add_resource(RoutesCollectionAPI, '/api/routes', methods=['GET', 'POST'])
api.add_resource(RoutesAPI, '/api/routes/<int:routes_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource HA
api.add_resource(HA_Mode_API, '/api/high-availability-mode', methods=['GET'])
api.add_resource(HA_API, '/api/high-availability', methods=['GET', 'PUT'])

# Resource Load Balancing 
api.add_resource(LoadBalancingCollectionAPI, '/api/loadbalancing', methods=['GET', 'POST', 'PUT'])

# Resource report schedule 
api.add_resource(ReportScheduleCollectionAPI, '/api/report', methods=['GET', 'POST'])
api.add_resource(ReportScheduleAPI, '/api/report/<int:report_id>', methods = ['GET', 'PUT', 'DELETE'])

# Emegency (report schedule)
api.add_resource(EmegencyCollectionAPI, '/api/emergency', methods=['GET', 'POST'])
api.add_resource(EmegencyScheduleAPI, '/api/emergency/<int:emegency_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource system users
api.add_resource(UsersCollectionAPI, '/api/users', methods=['GET', 'POST'])
api.add_resource(UserAPI, '/api/users/<int:user_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource backup backup plan 
api.add_resource(BackUpAPI, '/api/backup', methods=['GET', 'POST'])
api.add_resource(BackUpAPIs, '/api/backup/<int:backup_id>', methods=['GET','DELETE'])
api.add_resource(BackUpPlanAPI, '/api/backup/plan', methods = ['GET', 'POST'])
api.add_resource(Restore, '/api/restore', methods = ['POST'])
api.add_resource(BackupData, '/api/backup/<int:backup_id>/download', methods = ['GET'])

# Resource datetime
api.add_resource(DateTimeAPI, '/api/dashboard/system_time', methods=['GET', 'POST'])


# Resource access control list
api.add_resource(AccessControlListCollectionAPI, '/api/acl', methods=['GET', 'POST'])
api.add_resource(AccessControlListAPI, '/api/acl/<int:acl_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource firewall access
api.add_resource(FirewallAccessCollectionAPI, '/api/firewalls', methods=['GET', 'POST'])
api.add_resource(FirewallAccessAPI, '/api/firewalls/<int:firewall_policy_id>', methods = ['GET', 'PUT', 'DELETE'])

# Resource operating_mode
api.add_resource(Operating_modeAPI, '/api/operating_mode', methods=['GET', 'POST'])


# Resource auto checking server health
api.add_resource(ACSHCollectionAPI, '/api/diagnostic/acsh', methods=['GET', 'POST'])
api.add_resource(ACSHAPI, '/api/diagnostic/acsh/<int:acsh_id>', methods = ['GET', 'PUT', 'DELETE'])

#User avatar
api.add_resource(ImageData,'/api/static/image/<file_name>',methods=["GET"])

api.add_resource(SignatureCollectionAPI, '/api/profile/<int:profile_id>/signature', methods=['GET'])
api.add_resource(SignatureAPI, '/api/profile/<int:profile_id>/signature/<int:signature_id>', methods=['GET', 'PUT'])

api.add_resource(AbnormalCollectionAPI, '/api/abnormal', methods=['GET'])
api.add_resource(AbnormalAPI, '/api/abnormal/<abnormal_id>', methods=["GET", 'PUT'])

api.add_resource(TcpOtherOptionsAPI, '/api/optionvalues/other', methods=['GET'])

api.add_resource(WafPolicyListCollectionAPI, '/api/waf/policy_list', methods=['GET'])

api.add_resource(WafPolicyCollectionAPI, '/api/profile/<int:profile_id>/http/waf', methods=['GET', 'POST'])
api.add_resource(WafPolicyAPI, '/api/profile/<int:profile_id>/http/waf/<int:waf_policy_id>', methods=['GET', 'PUT', 'DELETE'])

#monitoring
api.add_resource(SystemResourceAPI, '/api/monitoring/system_resource', methods=['GET'])
api.add_resource(TrafficResourceAPI, '/api/monitoring/traffic_resource', methods=['GET'])

if __name__ == '__main__':
	try:
		logging.basicConfig(filename='error.log',level=logging.DEBUG)
		app.run(host='0.0.0.0', port=3001, debug=True)
	except Exception as exp:
		print (exp)

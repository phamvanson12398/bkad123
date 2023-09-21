from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *
from sqlalchemy import *

Base = declarative_base()


# khoi tao ket noi vao co so du lieu
def ConnectToDB():
	engine = create_engine('mysql+mysqldb://bkad:123654As!@localhost/bkad?charset=utf8',pool_size=50, max_overflow=0)
	Session = sessionmaker(bind=engine)
	return Session


# Model cho bang Website
class Websites(Base):
	__tablename__ = 'websites'

	id = Column(Integer, primary_key=True)
	domain = Column(String)
	ip_address = Column(String)
	port = Column(Integer)
	listen_port = Column(Integer)
	ssl = Column(Integer)
	cache = Column(Integer)
	key = Column(String)
	cert = Column(String)
	status = Column(Integer)

	group_websites = relationship('GroupWebsites', secondary = 'group_websites_have_websites')


# Model cho bang Group Website
class GroupWebsites(Base):
	__tablename__ = 'group_websites'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)

	websites = relationship('Websites', secondary='group_websites_have_websites')


# Model cho bang phu lien ket hai bang Website va Group Website
class GroupWebsitesHaveWebsites(Base):
	__tablename__ = 'group_websites_have_websites'

	website_id = Column(Integer, ForeignKey('websites.id'), primary_key=True)
	group_website_id = Column(Integer, ForeignKey('group_websites.id'), primary_key=True)


class ADProfile(Base):
	__tablename__ = 'ad_profile'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	mode = Column(String)
	description = Column(String)

	atas = relationship('ATAS', uselist=False, back_populates="ad_profile")
	waf_policy = relationship('WafPolicy', uselist=False, back_populates="ad_profile")
	ad_policy = relationship('ADPolicy', uselist=False, back_populates="ad_profile")
	signature = relationship('Signature', uselist=False, back_populates="profile")
	abnormal = relationship('Abnormal', uselist=False, back_populates="profile")
	tcp_general = relationship('TcpGeneral', uselist=False, back_populates="ad_profile")
	tcp_slowcnn = relationship('TcpSlowConnection', uselist=False, back_populates="ad_profile")
	tcp_threshold = relationship('TcpThreshold', uselist=False, back_populates="ad_profile")
	http_threshold = relationship('HttpThreshold', uselist=False, back_populates="ad_profile")
	http_general = relationship('HttpGeneral', uselist=False, back_populates="ad_profile")
	http_slowcnn = relationship('HttpSlowConnection', uselist=False, back_populates="ad_profile")


class LearningMode(Base):
	__tablename__ = 'learning_mode'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	learning_time = Column(Integer)
	iteration = Column(Integer)
	learning_type = Column(String)

	atas = relationship('ATAS', uselist=False, back_populates="learn_mode")


class ATAS(Base):
	__tablename__ = 'atas'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	learning_mode = Column(Integer, ForeignKey('learning_mode.id'))
	start_time = Column(String)
	start_date = Column(String)
	end_date = Column(String)
	apply = Column(Integer)
	status = Column(Integer)
	progress = Column(String)
	profile = Column(Integer, ForeignKey('ad_profile.id'))

	ad_profile = relationship("ADProfile", back_populates="atas")
	learn_mode = relationship("LearningMode", back_populates="atas")


class Network(Base):
	__tablename__ = 'network'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	ip_address = Column(String)
	netmask = Column(String)
	description = Column(String)

	group_network = relationship('GroupNetwork', secondary = 'group_network_have_network')
	ad_policy = relationship('ADPolicy', secondary = 'ad_policy_have_networks')
	# firewallsource = relationship('FireWallAccess', secondary = 'firewall_access_source')
	# firewalldestination = relationship('FireWallAccess', secondary = 'firewall_access_destination')
	
class Service(Base):
	__tablename__ = 'service'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	port = Column(String)
	protocol = Column(String)
	description = Column(String)

	group_service = relationship('GroupService', secondary='group_service_have_services')
	firewallservice = relationship('FireWallAccess', secondary='firewall_access_service')

class GroupService(Base):
	__tablename__ = 'group_service'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)

	service = relationship('Service', secondary='group_service_have_services')
	firewallgroupservice = relationship('FireWallAccess', secondary='firewall_access_group_service')

class GroupServiceHaveServices(Base):
	__tablename__ = 'group_service_have_services'

	service_id = Column(Integer, ForeignKey('service.id'),primary_key=True)
	group_service_id = Column(Integer, ForeignKey('group_service.id'), primary_key=True)


class GroupNetwork(Base):
	__tablename__ = 'group_network'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)

	network = relationship('Network', secondary = 'group_network_have_network')
	ad_policy = relationship('ADPolicy', secondary = 'ad_policy_have_group_networks')
	firewallgroupsource = relationship('FireWallAccess', secondary = 'firewall_access_group_source')
	firewallgroupdestination = relationship('FireWallAccess', secondary = 'firewall_access_group_destination')

class GroupNetworkHaveNetwork(Base):
	__tablename__ = 'group_network_have_network'

	group_network_id = Column(Integer, ForeignKey('group_network.id'), primary_key=True)
	network_id = Column(Integer, ForeignKey('network.id'), primary_key=True)


class ADPolicy(Base):
	__tablename__ = 'ad_policy'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	profile = Column(Integer, ForeignKey('ad_profile.id'))
	description = Column(String)
	status = Column(Integer)

	ad_profile = relationship("ADProfile", back_populates="ad_policy")
	network = relationship('Network', secondary = 'ad_policy_have_networks')
	group_network = relationship('GroupNetwork', secondary = 'ad_policy_have_group_networks')


class ADPolicyHaveNetwork(Base):
	__tablename__ = 'ad_policy_have_networks'

	policy_id = Column(Integer, ForeignKey('ad_policy.id'), primary_key=True)
	network_id = Column(Integer, ForeignKey('network.id'), primary_key=True)

class ADPolicyHaveGroupNetwork(Base):
	__tablename__ = 'ad_policy_have_group_networks'

	policy_id = Column(Integer, ForeignKey('ad_policy.id'), primary_key=True)
	group_network_id = Column(Integer, ForeignKey('group_network.id'), primary_key=True)


class NetworkInterface(Base):
	__tablename__ = 'network_interface'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	ip_address = Column(String)
	netmask = Column(String)
	gateway = Column(String)
	status = Column(Integer)
	type = Column(String)
	addressing_mode = Column(String)
	ispname = Column(String)
	username = Column(String)
	password = Column(String)
	mtu = Column(String)
	fixed_ip = Column(String)
	clone_mac = Column(String)
	created_at = Column(String)
	updated_at = Column(String)

	# group_nat = relationship('NetworkNat', secondary = 'group_nat_have_interface')
	# group_load_balancing = relationship('NetworkLoadBalancing', secondary = 'group_load_balancing_have_interface')
	network_nat = relationship('NetworkNat', uselist=True, back_populates="network_interface")
	firewall_interface = relationship("FireWallAccess", secondary="firewall_access_interface")


class NetworkNat(Base):
	__tablename__ = 'network_nat'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	protocol = Column(String)
	type = Column(String)
	ip_address = Column(String)
	service = Column(Integer)
	ip_map = Column(String)
	port_map = Column(Integer)
	status = Column(Integer)
	interface = Column(Integer, ForeignKey('network_interface.id'))

	network_interface = relationship("NetworkInterface", back_populates="network_nat")
	
	# interface = relationship('NetworkInterface', secondary = 'group_nat_have_interface')

# class GroupNatHaveInterface(Base):
	
# 	__tablename__ = 'group_nat_have_interface'
# 	interface_id = Column(Integer, ForeignKey('network_interface.id') ,primary_key=True)
# 	nat_id = Column(Integer, ForeignKey('network_nat.id'),primary_key=True)
		

class NetworkLoadBalancing(Base):
	__tablename__ = 'network_load_balancing'

	id = Column(Integer, primary_key=True)
	status = Column(Integer)
	command = Column(String)
	server = Column(String)
	timeout = Column(Integer)
	threshold = Column(Integer)

	interface = Column(String)

# class GroupLoadBalancingHaveInterface(Base):
# 	__tablename__ = 'group_load_balancing_have_interface'

# 	interface_id = Column(Integer, ForeignKey('network_interface.id'), primary_key=True)
# 	load_balancing_id = Column(Integer, ForeignKey('network_load_balancing.id'), primary_key=True)


class ReportSchedule(Base):
	__tablename__ = 'report_schedule'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	frequency = Column(String)
	specific_day = Column(String)
	start_time = Column(String)
	type = Column(String)
	email = Column(String)
	status = Column(Integer)


class Signature(Base):
	__tablename__ = 'signature'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	type = Column(String)
	description = Column(String)
	content = Column(String)
	status = Column(Integer)
	ad_profile = Column(Integer, ForeignKey('ad_profile.id'))

	profile = relationship("ADProfile", back_populates="signature")


class Abnormal(Base):
	__tablename__ = 'abnormal'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	status = Column(Integer)
	ad_profile = Column(Integer, ForeignKey('ad_profile.id'))

	profile = relationship("ADProfile", back_populates="abnormal")


class TcpGeneral(Base):
	__tablename__ = 'tcp_general'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	data = Column(String)
	status = Column(Integer)
	input_type = Column(String)
	input_id = Column(String)
	member_name = Column(String)
	member_value = Column(String)
	profile = Column(Integer, ForeignKey('ad_profile.id'))

	ad_profile = relationship("ADProfile", back_populates="tcp_general")


class HttpGeneral(Base):
	__tablename__ = 'http_general'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	data = Column(String)
	status = Column(Integer)
	input_type = Column(String)
	input_id = Column(String)
	member_name = Column(String)
	member_value = Column(String)
	profile = Column(Integer, ForeignKey('ad_profile.id'))

	ad_profile = relationship("ADProfile", back_populates="http_general")



class TcpGeneralDef(Base):
	__tablename__ = 'tcp_general_def'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	data = Column(String)
	status = Column(Integer)
	input_type = Column(String)
	input_id = Column(String)
	member_name = Column(String)
	member_value = Column(String)


class TcpSlowConnection(Base):
	__tablename__ = 'tcp_slowcnn'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	data = Column(String)
	status = Column(Integer)
	input_type = Column(String)
	input_id = Column(String)
	member_name = Column(String)
	member_value = Column(String)
	profile = Column(Integer, ForeignKey('ad_profile.id'))

	ad_profile = relationship("ADProfile", back_populates="tcp_slowcnn")


class HttpSlowConnection(Base):
	__tablename__ = 'http_slowcnn'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	data = Column(String)
	status = Column(Integer)
	input_type = Column(String)
	input_id = Column(String)
	member_name = Column(String)
	member_value = Column(String)
	profile = Column(Integer, ForeignKey('ad_profile.id'))

	ad_profile = relationship("ADProfile", back_populates="http_slowcnn")


class TcpSlowConnectionDef(Base):
	__tablename__ = 'tcp_slowcnn_def'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	data = Column(String)
	status = Column(Integer)
	input_type = Column(String)
	input_id = Column(String)
	member_name = Column(String)
	member_value = Column(String)


class TcpOtherOptions(Base):
	__tablename__ = 'tcp_other_options'

	id = Column(Integer, primary_key=True)
	option = Column(String)
	value = Column(String)

	# tcp_threshold1 = relationship('TcpThreshold', uselist=False, back_populates="other")


class TcpThreshold(Base):
	__tablename__ = 'tcp_threshold'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	packet_in = Column(Integer)
	packet_out = Column(Integer)
	bandwidth_in = Column(Integer)
	bandwidth_out = Column(Integer)
	percent = Column(String)
	description = Column(String)
	prevention = Column(String)
	status = Column(Integer)
	type = Column(String)
	profile = Column(Integer, ForeignKey('ad_profile.id'))
	other_id = Column(Integer, ForeignKey('tcp_other_options.id'))

	# other = Column("TcpOtherOptions", back_populates="tcp_threshold1")
	ad_profile = relationship("ADProfile", back_populates="tcp_threshold")
	service = relationship('Service', secondary = 'tcp_threshold_have_services')
	group_service = relationship('GroupService', secondary = 'tcp_threshold_have_groupservices')
	network = relationship('Network', secondary = 'tcp_threshold_have_networks')
	group_network = relationship('GroupNetwork', secondary = 'tcp_threshold_have_groupnetworks')

class TcpThresholdHaveServices(Base):
	__tablename__ = 'tcp_threshold_have_services'

	tcp_threshold_id = Column(Integer, ForeignKey('tcp_threshold.id'), primary_key=True)
	service_id = Column(Integer, ForeignKey('service.id'), primary_key=True)


class TcpThresholdHaveGroupServices(Base):
	__tablename__ = 'tcp_threshold_have_groupservices'

	tcp_threshold_id = Column(Integer, ForeignKey('tcp_threshold.id'), primary_key=True)
	group_service_id = Column(Integer, ForeignKey('group_service.id'), primary_key=True)


class TcpThresholdHaveNetworks(Base):
	__tablename__ = 'tcp_threshold_have_networks'

	tcp_threshold_id = Column(Integer, ForeignKey('tcp_threshold.id'), primary_key=True)
	network_id = Column(Integer, ForeignKey('network.id'), primary_key=True)


class TcpThresholdHaveGroupNetworks(Base):
	__tablename__ = 'tcp_threshold_have_groupnetworks'

	tcp_threshold_id = Column(Integer, ForeignKey('tcp_threshold.id'), primary_key=True)
	group_network_id = Column(Integer, ForeignKey('group_network.id'), primary_key=True)


class HttpThreshold(Base):
	__tablename__ = 'http_threshold'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	packet_in = Column(Integer)
	packet_out = Column(Integer)
	bandwidth_in = Column(Integer)
	bandwidth_out = Column(Integer)
	percent = Column(String)
	description = Column(String)
	prevention = Column(String)
	status = Column(Integer)
	type = Column(String)
	profile = Column(Integer, ForeignKey('ad_profile.id'))

	ad_profile = relationship("ADProfile", back_populates="http_threshold")
	http_threshold_value = relationship('HttpThresholdValue', uselist=True, back_populates="http_threshold")


class HttpThresholdValue(Base):
	__tablename__ = 'http_threshold_value'

	id = Column(Integer, primary_key=True)
	http_threshold_id = Column(Integer, ForeignKey('http_threshold.id'))
	value = Column(String)

	http_threshold = relationship("HttpThreshold", back_populates="http_threshold_value")


class AtasTcpThreshold(Base):
	__tablename__ = 'atas_tcp_threshold'

	id = Column(Integer, primary_key=True)
	tcp_threshold_id = Column(Integer, ForeignKey('tcp_threshold.id'))

	# tcp_threshold = relationship("TcpThreshold", back_populates="atas_tcp_thresholds")


class AtasHttpThreshold(Base):
	__tablename__ = 'atas_http_threshold'

	id = Column(Integer, primary_key=True)
	http_threshold_id = Column(Integer, ForeignKey('http_threshold.id'))

	# http_threshold = relationship("HttpThreshold", back_populates="atas_http_threshold")


class Routes(Base):
	__tablename__ = 'routes'
	id = Column(Integer, primary_key=True)
	created_at = Column(String)
	description = Column(String)
	destination = Column(String)
	gateway = Column(String)
	metric = Column(Integer)
	name = Column(String)
	netmask = Column(String)
	status = Column(Integer)
	updated_at = Column(String)

class Config_HA(Base):
	__tablename__ = 'config_ha'
	id = Column(Integer, primary_key=True)
	device_priority = Column(Integer)
	group_name = Column(String)
	group_password = Column(String)
	heartbeat_interfaces = Column(String)
	heartbeat_netmask = Column(String)
	heartbeat_network = Column(String)
	operation_mode = Column(String)
	high_availability_status = Column(Integer)

class Virtual_Interface(Base):
	__tablename__='virtual_interface'
	interface_name = Column(String, primary_key=True)
	is_enable = Column(Integer)
	virtual_ip_address = Column(String)
	priority = Column(Integer)

# class ReportSchedule(Base):
# 	__tablename__ = 'report_schedule'
# 	id = Column(Integer, primary_key=True)
# 	name = Column(String)
# 	frequency = Column(String)
# 	specific_day = Column(String)
# 	start_time = Column(String)
# 	type = Column(String)
# 	email = Column(String)

class Emegency(Base):
	__tablename__ = 'emegency'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	number_of_event = Column(Integer)
	time_limited = Column(Integer)
	report_email = Column(String)
	status = Column(Integer)

class SystemUsers(Base):
	__tablename__ = 'system_users'

	id = Column(Integer, primary_key=True)
	username = Column(String)
	name = Column(String)
	avatar = Column(String)
	password = Column(String)
	status = Column(Integer)

class BackUp(Base):
	__tablename__ = 'backup'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	datetime = Column(String)
	password = Column(String)


class BackUpPlan(Base):
	__tablename__ = 'backup_plan'
	id = Column(Integer, primary_key=True)
	status = Column(Integer)
	frequency = Column(String)
	specific_day = Column(String)
	start_time = Column(String)
	end_date = Column(String)
	start_date = Column(String)


class DateTime(Base):
	__tablename__ = 'datetime'
	id = Column(Integer, primary_key=True)
	sync_time = Column(Integer)
	system_time = Column(String)
	time_zone = Column(String)
	server = Column(String)


class AccessControlList(Base):
	__tablename__ = 'access_control_list'

	id = Column(Integer, primary_key=True)
	address = Column(String)
	type = Column(String)
	description = Column(String)
	status = Column(Integer)


class FireWallAccess(Base):
	__tablename__ = 'firewall_access'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	position = Column(Integer)
	action = Column(String)
	status = Column(Integer)
	created_at = Column(String)
	edited_at = Column(String)
	# interface = Column(Integer, ForeignKey('network_interface.id'))


	firewall_access_source = relationship("Network", secondary="firewall_access_source")
	firewall_access_group_source = relationship(
		'GroupNetwork', secondary='firewall_access_group_source'
	)
	firewall_access_destination = relationship("Network", secondary="firewall_access_destination")
	firewall_access_group_destination = relationship(
		'GroupNetwork', secondary='firewall_access_group_destination'
	)
	firewall_access_service = relationship("Service", secondary="firewall_access_service")
	firewall_access_group_service = relationship(
		'GroupService', secondary='firewall_access_group_service'
	)
	firewall_interface = relationship("NetworkInterface", secondary="firewall_access_interface")


class FireWallAccessInterface(Base):
	__tablename__ = 'firewall_access_interface'
	firewall_id = Column(Integer, ForeignKey('firewall_access.id'), primary_key=True)
	interface_id = Column(Integer, ForeignKey('network_interface.id'), primary_key=True)


class FireWallAccessSource(Base):
	__tablename__ = 'firewall_access_source'

	firewall_id = Column(Integer, ForeignKey('firewall_access.id'), primary_key=True)
	network_id = Column(Integer, ForeignKey('network.id') , primary_key=True)


class FireWallAccessGroupSource(Base):
	__tablename__ = 'firewall_access_group_source'
	firewall_id = Column(Integer, ForeignKey('firewall_access.id'), primary_key=True)
	gr_network_id = Column(Integer, ForeignKey('group_network.id'), primary_key=True)


class FireWallAccessDestinaton(Base):
	__tablename__ = 'firewall_access_destination'
	
	firewall_id = Column(Integer, ForeignKey('firewall_access.id'), primary_key=True)
	network_id = Column(Integer, ForeignKey('network.id'), primary_key=True)


class FireWallAccessGroupDestinaton(Base):
	__tablename__ = 'firewall_access_group_destination'
	firewall_id = Column(Integer, ForeignKey('firewall_access.id'), primary_key=True)
	gr_network_id = Column(Integer, ForeignKey('group_network.id'), primary_key=True)


class FireWallAccessService(Base):
	__tablename__ = 'firewall_access_service'
	firewall_id = Column(Integer, ForeignKey('firewall_access.id'), primary_key=True)
	service_id = Column(Integer, ForeignKey('service.id'), primary_key=True)


class FireWallAccessGroupService(Base):
	__tablename__ = 'firewall_access_group_service'
	firewall_id = Column(Integer, ForeignKey('firewall_access.id'), primary_key=True)
	gr_service_id = Column(Integer, ForeignKey('group_service.id'), primary_key=True)


class Operating_mode(Base):
	__tablename__ = 'operating_mode'
	id = Column(Integer, primary_key=True)
	mode = Column(String)


class ACSH(Base):
	__tablename__ = 'acsh'

	id = Column(Integer, primary_key=True)
	address = Column(String)
	domain = Column(String)
	service_status = Column(String)
	status = Column(Integer)
	port = Column(Integer)
	description = Column(String)


class WafPolicyList(Base):
	__tablename__ = 'waf_policy_list'

	id = Column(Integer, primary_key=True)
	policy_name = Column(String)


class WafPolicy(Base):
	__tablename__ = 'waf_policy'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	policy_enable = Column(String)
	status = Column(Integer)
	profile = Column(Integer, ForeignKey('ad_profile.id'))

	ad_profile = relationship("ADProfile", back_populates="waf_policy")
	group_websites = relationship('GroupWebsites', secondary='waf_policy_have_group_website')


class WafPolicyHaveGroupWebsites(Base):
	__tablename__ = 'waf_policy_have_group_website'

	waf_policy_id = Column(Integer, ForeignKey('waf_policy.id'), primary_key=True)
	group_website_id = Column(Integer, ForeignKey('group_websites.id'), primary_key=True)
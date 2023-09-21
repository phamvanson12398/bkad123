import iptc

from models.models import ConnectToDB, NetworkNat, NetworkInterface

class NetworkNatCore():

	def __init__(self):
		pass

	def add_nat_rule(self):
		try:
			Session = ConnectToDB()
			session = Session()
			chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "PREROUTING")
			chain.flush()
			chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "POSTROUTING")
			chain.flush()
			records = session.query(NetworkNat).all()
			for data in records:
				print ("Data = ", data.__dict__)
				interface = data.network_interface.name
				data = data.__dict__
				if data['status'] == 1:
					data['protocol'] = data['protocol'].split(",")
					for protocol in data['protocol']:
						rule = iptc.Rule()
						match = iptc.Match(rule, protocol.lower())
						match.dport = str(data['service'])
						rule.add_match(match)
						match = iptc.Match(rule, "state")
						match.state = "RELATED,ESTABLISHED"
						rule.add_match(match)
						rule.protocol = protocol
						rule.src = data['ip_address']
						target = iptc.Target(rule, data['type'])
						if data['type'] == "DNAT":
							chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "PREROUTING")
							rule.in_interface = interface
							target.to_destination = f"{data['ip_map']}:{data['port_map']}"
						else:
							chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "POSTROUTING")
							rule.out_interface = interface
							target.to_source = f"{data['ip_map']}:{data['port_map']}"
						rule.target = target
						chain.insert_rule(rule)
			return True
		except Exception as exp:
			raise (exp)
			return False
		finally:
			session.close()
# from infi.clickhouse_orm.database import Database
# from infi.clickhouse_orm.models import Model
# from infi.clickhouse_orm.fields import *
# from infi.clickhouse_orm.engines import MergeTree
from clickhouse_driver import Client

def ConnectToDB():
    # db = Database('bkad', db_url='http://192.168.200.4:8123', password='123')
    client = Client(
        host='192.168.200.4',
        database='bkad',
        password='123'
    )
    return client

# class TcpDataStatistic(Model):

#     created_at = DateTimeField()
#     created_date = DateField()
#     policy_id = Int32Field()
#     packet_in = Float64Field()
#     packet_out = Float64Field()
#     bandwidth_in = Float64Field()
#     bandwidth_out = Float64Field()
#     percent = Float64Field()

def CHConnect():
	return Client(host='192.168.200.4',port=9000, password='123', database='bvg')
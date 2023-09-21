import random
import string

from clickhouse_driver import Client

def randomString():
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(32))

def randomNum():
	return random.random()


if __name__ == '__main__':
	client = Client(
		"localhost",
		password="123",
		database="test"
		)

	data = []
	print ("Init Data...")
	for i in range(10000000):
		data.append({
			'id': i,
			'pac_in': randomNum(),
			'pac_out': randomNum(),
			'b_in': randomNum(),
			'b_out': randomNum(),
			'percent': randomNum()
		})
		print (f"Append {i} record!")
	print ("Complete Init Data!!!")

	block = []
	print ("Insert Data to Database...")
	for i in range(len(data)):
		block.append(data[i])
		if i % 1000 == 0 and i > 0:
			print ("Inserting Block Data to Database...")
			_str = "(0, 0, 0, 0, 0, 0)"
			for j in block:
				_str += "," + f"({j['id']}, {j['pac_in']}, {j['pac_out']}, {j['b_in']}, {j['b_out']}, {j['percent']})"
				query = f"INSERT INTO protocols (protocol_id, packet_in, packet_out, bandwidth_in, bandwidth_out, percent) VALUES {_str}"
				client.execute(query)
			block = []
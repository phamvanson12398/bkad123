import datetime
import time

def getDefault(parameters, metadata, obj):
	if ('orderBy' or 'orderType') not in parameters:
		order = obj.id.asc()
	else:
		try:
			if parameters['orderType'] == 'desc':
				order = metadata[parameters['orderBy']].desc()
			else:
				order = metadata[parameters['orderBy']].asc()
		except:
			order = obj.id.asc()
	if 'limit' not in parameters:
		limit = 10
	else:
		try:
			limit = int(parameters['limit'])
		except:
			limit = 10
	if 'page' not in parameters:
		page = 1
	else:
		try:
			page = int(parameters['page'])
		except:
			page = 1
	offset = (page - 1) * limit

	return limit, page, offset, order

def standardizedData(obj, del_param=None, param=None):
	data = {}
	try:
		obj = obj.__dict__
	except:
		return None
	try:
		if '_sa_instance_state' in obj:
			del obj["_sa_instance_state"]
		obj["created_at"] = datetime_to_str(obj["created_at"])
		obj["updated_at"] = datetime_to_str(obj["updated_at"])
	except:
		pass
	if del_param != None:
		for d in del_param:
			try:
				del obj[d]
			except:
				pass
	if param != None:
		for p in param:
			data[p] = obj[param[p]]
		return data

	return obj

def readfile(dir):
	f = open(dir,"r")
	data = f.read()
	f.close()
	return data

def check_null(data):
	for p in data:
		if p != 'description':
			if data[p] == "":
				return False

def convert_none_to_string(data, exp=[], param={}):
	try:
		data_temp = data.copy()
		for key in data:
			if data[key] is None and key not in exp:
				data[key] = ""
		for p in param:
			print (p)
			if p not in data:
				data_temp[p] = param[p]
		print (data)
		return data_temp
	except Exception as exp:
		pass

def get_time(type, _time):
	current_time = datetime.datetime.now()
	try:
		_time = float(_time)
		from_time = time.mktime(current_time.timetuple())
		if type == 'minutes':
			to_time = from_time - _time * 60
		if type == 'hours':
			to_time = from_time - _time * 3600
		if type == 'days':
			to_time = from_time - _time * 86400
		if type == 'weeks':
			to_time = from_time - _time * 604800

		to_time = datetime.datetime.fromtimestamp(to_time).strftime('%Y-%m-%d %H:%M:%S')
		current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
	except:
		return current_time, datetime.datetime.fromtimestamp(0).strftime('%Y-%m-%d %H:%M:%S')
	return current_time, to_time

def datetime_to_str(input_datetime):
	if input_datetime:
		return input_datetime.strftime('%Y-%m-%d %H:%M:%S')
	return None

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
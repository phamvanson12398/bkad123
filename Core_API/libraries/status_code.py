from flask import Flask, jsonify

# app = Flask(__name__)

def status_code_200(message, data):
	result = {'status': 1, 'message': str(message), 'data': data}
	resp = jsonify(result)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return result


# @app.errorhandler(400)
def status_code_400(message):
	result = {'status': 0, 'message': str(message)}
	resp = jsonify(result)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.status_code = 200
	return resp

# @app.errorhandler(500)
def status_code_500(message):
	result = {'status': 0, 'message': str(message)}
	resp = jsonify(result)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.status_code = 200
	return resp

def get_data_with_page(data, page_limit, current_page, total):
	result = {'data':'','paging':{'total_count': total}}
	result['data'] = data
	total_page = ''
	if int(result['paging']['total_count'])%int(page_limit) == 0:
		total_page = int(result['paging']['total_count'])//int(page_limit)
	else:
		total_page = (int(result['paging']['total_count'])//int(page_limit)) + 1

	if current_page < int(total_page):
		result['paging']['records_in_page'] = page_limit
	else:
		result['paging']['records_in_page'] =  int(result['paging']['total_count']) - (int(current_page) - 1) * page_limit

	result['paging']['total_page'] = total_page
	result['paging']['current_page'] = int(current_page)

	return result
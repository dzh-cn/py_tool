import os

from flask import Flask, request, render_template, json

# uri = 'http://127.0.0.1:8081/'
uri = 'http://172.24.6.100/'

app = Flask(__name__)

# boss_front
log_dir = '/export/log/%s/%s_detail.log'
home_dir = '/home/wy/www/%s/logs/catalina.out'


@app.route('/log/<system>.html', methods=['GET', 'POST'])
def log_home_html(system):
	return log_home(system)


@app.route('/log/<system>', methods=['GET', 'POST'])
def log_home(system):
	return render_template('log.html', offset=os.path.getsize(get_log_file_path(system)), system=system)


@app.route('/log/<system>.json', methods=['GET', 'POST'])
def read_log(system):
	print("%s ..." % system)
	filePath = get_log_file_path(system)
	offset = request.args.get('offset')
	if offset is None or int(offset) < 1:
		offset = os.path.getsize(filePath)

	result = {'offset': os.path.getsize(filePath)}
	with open(file=filePath, encoding='utf8') as f:
		f.seek(int(offset))
		result['line'] = f.readlines()

	return json.dumps(result)


def get_log_file_path(system):
	log = str(log_dir % (system, system))
	if os.path.exists(log):
		return log
	home_logs = str(home_dir % system)
	if os.path.exists(home_logs):
		return home_logs
	raise RuntimeError('系统找不到日志', log, home_logs)


@app.errorhandler(404)
def not_found(e):
	return str("<b style='font-size:200px;'>404</b><p>%s</p>" % e)


@app.errorhandler(500)
def not_found(e):
	return str("<b style='font-size:200px;'>500</b><p>%s</p>" % e)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8571)

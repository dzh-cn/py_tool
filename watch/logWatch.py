import os

from flask import Flask, request, render_template, json

# uri = 'http://127.0.0.1:8081/'
uri = 'http://172.24.6.100/'

app = Flask(__name__)

# boss_front
dir = '/export/log/%s/%s_detail.log'


@app.route('/<system>/log.html', methods=['GET', 'POST'])
def home(system):
	return render_template('log.html', offset=os.path.getsize(str(dir % (system, system))), system=system)


@app.route('/<system>/watch.json', methods=['GET', 'POST'])
def read_log(system):
	print("%s ..." % system)
	filePath = str(dir % (system, system))
	offset = request.args.get('offset')
	if offset is None or int(offset) < 1:
		offset = os.path.getsize(filePath)

	result = {'offset': os.path.getsize(filePath)}
	with open(file=filePath, encoding='utf8') as f:
		f.seek(int(offset))
		result['line'] = f.readlines()

	return json.dumps(result)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8571)

import os
from zipfile import ZipFile

from flask import Flask, request, render_template

# uri = 'http://127.0.0.1:8081/'
uri = 'http://172.24.6.100/'

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')


@app.route('/upload', methods=['GET'])
def upload_form():
	user = request.args.get('user')
	return render_template('upload.html', user=user)


@app.route('/upload', methods=['POST'])
def upload():
	try:
		user = request.form['user']
		directory = request.form['directory']
		if not len(request.files) or not directory or not user:
			message = '以下都不能为空！'
		else:
			cover = request.form['cover']
			result = extractall_to_relatively_path(request.files['file'], directory, cover=cover)
			message = uri + user + '/' + directory
			if result != 1:
				message = result

	except BaseException as e:
		print(e)
		message = e.__str__()
		pass
	return render_template('upload.html', message=message, user=user, directory=directory)


def extractall_to_absolute_path(file, path, *, cover=0):
	if os.path.exists(path) and cover == '0':
		print('path of [', path, '] is exists')
		return '文件已存在，可选择覆盖'

	if cover:
		print('cover not finish')

	with ZipFile(file, 'r') as zip_file:
		zip_file.extractall(path)

	print('All files zipped successfully!')
	return 1


def extractall_to_relatively_path(file, path, **param):
	return extractall_to_absolute_path(file, 'E:/export/data/nginx_prototype_html/' + path, **param)


if __name__ == '__main__':
	app.run(host='0.0.0.0')

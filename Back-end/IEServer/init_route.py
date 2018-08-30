#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:def_html_route
   Author:jasonhaven
   date:18-8-15
-------------------------------------------------
   Change Activity:18-8-15:
-------------------------------------------------
"""

from log import Logger
import mimetypes
import os
from flask import Flask, make_response, render_template, send_from_directory, request, flash, jsonify, url_for,redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)


from views.init_main import init_main
app.register_blueprint(init_main,url_prefix='/BITIE/main')

from views.init_page import init_page
app.register_blueprint(init_page,url_prefix='/BITIE')

from views.init_system import init_system
app.register_blueprint(init_system,url_prefix='/BITIE/system')



'''
系统服务管理：日志，请求装饰器监听,登录，注册
'''

logger = Logger(isclean=True).get_logger()


@app.before_request
def before_request():
	ip = request.remote_addr
	url = request.url
	logger.info('ip = {} , url = {}.'.format(ip, url))
	extension = url.rsplit('.', 1)[1].lower()
	filter_resource = set(['png.', 'jpg.', 'js.', 'css.'])
	if extension not in filter_resource:
		logger.info('ip = {} , url = {}.'.format(ip, url))


@app.errorhandler(404)
def page_not_found(error):
	return redirect(url_for('init_system.page_not_found'))


@app.errorhandler(500)
def server_interval(error):
	return redirect(url_for('init_system.server_interval'))



'''
文件上传下载
'''

basepath = os.path.dirname(__file__)  # 当前文件所在路径
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
upload_path = os.path.join(basepath, UPLOAD_FOLDER)

DOWNLOAD_FOLDER = 'download'


@app.route('/BITIE/download/<category>/<filename>', methods=['GET'])
def download(category,filename):
	app.logger.debug('download_file...')
	directory=os.path.join(basepath,DOWNLOAD_FOLDER,category)
	file_path=os.path.join(directory,filename)
	if os.path.exists(file_path) and os.path.isfile(file_path):
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		mime_type = mimetypes.guess_type(filename)[0]
		response.headers['Content-Type'] = mime_type
		response.headers["Content-Disposition"] = "attachment; filename={};".format(filename.encode().decode('latin-1'))
		return response
	return redirect(url_for('init_system.page_not_found'))


# 用于判断文件后缀
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config['SECRET_KEY'] = '123456'


@app.route('/BITIE/upload', methods=['POST', 'GET'])
def upload():
	'''
	上传文件
	:return:
	data:dict
		status:True/False
		text:content of file
		desc:description of status
	'''
	app.logger.debug('upload_file...')

	data = {}
	data['status'] = False
	data['desc'] = ''
	data['text'] = ''

	if request.method == 'POST':
		if 'myfile' not in request.files:
			flash('No file part')
			data['desc'] = '请求访问错误！'
			return jsonify(data)

	file = request.files['myfile']

	if file.filename == '':
		flash('No selected file')
		data['desc'] = '请求文件不存在！'
		return jsonify(data)

	if file and allowed_file(file.filename):
		# 上传到固定的文件
		filename = secure_filename("tmp.txt")
		file.save(os.path.join(upload_path, filename))
		with open(os.path.join(upload_path, filename), 'r', encoding='utf-8') as f:
			text = f.read()
		data['status'] = True
		data['text'] = text
		return jsonify(data)
	data['desc'] = "文件类型不支持!"
	return jsonify(data)


'''
业务处理－信息抽取基础
'''

'''
信息抽取基础－关键字提取
'''
from keyword_extract import tfidf4zh, tfidf4en, textrank4zh, textrank4en


@app.route("/BITIE/keyword_extract", methods=['POST'])
def keyword_extract():
	app.logger.debug('keyword_extract...')

	data = {}
	data['status'] = False
	data['result'] = []

	text = request.form.get('text', 'hello,world')
	show_num = int(request.form.get('show_num', 5))
	alogrithm = request.form.get('alogrithm', 'tfidf')
	language = request.form.get('language', 'chinese')
	input_type = int(request.form.get('input_type', 0))

	app.logger.debug("{},{},{},{}".format(show_num, alogrithm, input_type, language))

	if language == 'chinese':
		if alogrithm == 'tfidf':  # OK
			if input_type == 0:  # textarea input
				data['result'], data['status'] = tfidf4zh(text, show_num)
			elif input_type == 1:  # file input
				text = open(os.path.join(UPLOAD_FOLDER, 'tmp.txt'), 'r').read()
				data['result'], data['status'] = tfidf4zh(text, show_num)
		elif alogrithm == 'textrank':  # OK
			if input_type == 0:  # textarea input
				data['result'], data['status'] = textrank4zh(text, show_num)
			elif input_type == 1:  # file input
				text = open(os.path.join(UPLOAD_FOLDER, 'tmp.txt'), 'r').read()
				data['result'], data['status'] = textrank4zh(text, show_num)
		elif alogrithm == 'lda':
			if input_type == 0:  # textarea input
				data['result'], data['status'] = tfidf4zh(text, show_num)
			elif input_type == 1:  # file input
				text = open(os.path.join(UPLOAD_FOLDER, 'tmp.txt'), 'r').read()
				data['result'], data['status'] = tfidf4zh(text, show_num)
	elif language == 'english':
		if alogrithm == 'tfidf':  # OK
			if input_type == 0:  # textarea input
				data['result'], data['status'] = tfidf4en(text, show_num)
			elif input_type == 1:  # file input
				text = open(os.path.join(UPLOAD_FOLDER, 'tmp.txt'), 'r').read()
				data['result'], data['status'] = tfidf4en(text, show_num)
		elif alogrithm == 'textrank':  # OK
			if input_type == 0:  # textarea input
				data['result'], data['status'] = textrank4en(text, show_num)
			elif input_type == 1:  # file input
				text = open(os.path.join(UPLOAD_FOLDER, 'tmp.txt'), 'r').read()
				data['result'], data['status'] = textrank4en(text, show_num)

	return jsonify(data)


'''
信息抽取基础－命名实体识别
'''
from ner import stanford_ner


@app.route("/BITIE/naming_entity_recognize", methods=['POST'])
def naming_entity_recognize():
	app.logger.debug('naming_entity_recognize...')

	data = {}
	data['status'] = False
	data['result'] = []
	data['analysis'] = []

	text = request.form.get('text', 'hello,world')
	# show_num = int(request.form.get('show_num', 5))
	alogrithm = request.form.get('alogrithm', 'tfidf')
	language = request.form.get('language', 'chinese')
	input_type = int(request.form.get('input_type', 0))

	app.logger.debug("{},{},{}".format(alogrithm, input_type, language))

	if alogrithm == 'stanford':
		if input_type == 0:  # textarea input
			data['result'], data['analysis'], data['status'] = stanford_ner(text, language)
		elif input_type == 1:  # file input
			text = open(os.path.join(UPLOAD_FOLDER, 'tmp.txt'), 'r').read()
			data['result'], data['analysis'], data['status'] = stanford_ner(text, language)
	elif alogrithm == 'crf':
		pass
	elif alogrithm == 'lstmcrf':
		pass
	elif alogrithm == 'bilstmcrf':
		pass

	return jsonify(data)


'''
信息抽取基础－词向量
'''
from word_embedding import similarity, most_similar


@app.route("/BITIE/word_embedding/similarity",methods=['POST'])
def word_similarity():
	app.logger.debug('similarity...')
	data = {}
	data['result'] = []
	data['status'] = False

	word1 = request.form.get('word1', '你')
	word2 = request.form.get('word2', '我')

	data['result'], data['status'] = similarity(word1, word2)
	return jsonify(data)


@app.route("/BITIE/word_embedding/most_similar",methods=['POST'])
def word_most_similar():
	app.logger.debug('most_similar...')
	data = {}
	data['result'] = []
	data['status'] = False

	word = request.form.get('word', '你')
	show_num = int(request.form.get('show_num', 5))

	data['result'], data['status'] = most_similar(word,topn=show_num)
	return jsonify(data)

'''
业务处理－科技情报挖掘
'''
from tag_generating.tag_auto_generating import process  as tag_process

@app.route("/BITIE/tag_auto_generating",methods=["POST"])
def tag_auto_generating():
	app.logger.debug('tag_auto_generating...')
	data = {}
	data['result'] = []
	data['status'] = False

	title = request.form.get('title', 'hello,world')
	text = request.form.get('text', 'hello,world')
	input_type = int(request.form.get('input_type', 0))

	if input_type == 0:  # textarea input
		data['result'],  data['status'] = tag_process(title,text)
	elif input_type == 1:  # file input
		text = open(os.path.join(UPLOAD_FOLDER, 'tmp.txt'), 'r').read()
		data['result'], data['status'] = tag_process(title,text)

	return jsonify(data)

'''
业务处理－实体扩展
'''
from entity_extend.entity_extend import process as entity_process
@app.route("/BITIE/entity_extend",methods=["POST"])
def entity_extend():
	app.logger.debug('entity_extend...')
	data = {}
	data['result'] = []
	data['status'] = False

	words = request.form.get('words', 'hello;world')
	app.logger.debug(words)

	data['result'],data['status']=entity_process(words.split())

	return jsonify(data)

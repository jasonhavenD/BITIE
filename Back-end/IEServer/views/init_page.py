#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:init_page
   Author:jasonhaven
   date:18-8-28
-------------------------------------------------
   Change Activity:18-8-28:
-------------------------------------------------
"""

from flask import  render_template,Blueprint

init_page=Blueprint('init_page',__name__)
'''
左侧栏目方法定义
'''


@init_page.route('/word_embedding.html')
def word_embedding():
	'''
	文本分类
	:return:
	'''
	return render_template('pages/word_embedding.html')


@init_page.route('/text_classification.html')
def text_classification():
	'''
	文本分类
	:return:
	'''
	return render_template('pages/text_classification.html')


@init_page.route('/keyword.html')
def keyword():
	'''
	关键字提取
	:return:
	'''
	return render_template('pages/keyword.html')


@init_page.route('/ner.html')
def ner():
	'''
	命名实体识别
	:return:
	'''
	return render_template('pages/ner.html')


@init_page.route('/re.html')
def re():
	'''
	实体关系抽取
	:return:
	'''
	return render_template('pages/re.html')


@init_page.route('/topic_detection.html')
def topic_detection():
	'''
	事件抽取
	:return:
	'''
	return render_template('pages/topic_detection.html')




@init_page.route('/tag_auto_generating.html')
def tag_auto_generating():
	'''
	标签自动生成
	:return:
	'''
	return render_template('pages/tag_auto_generating.html')

tag_auto_generating


@init_page.route('/dataset.html')
def dataset():
	'''
	常用数据集下载
	:return:
	'''
	return render_template('pages/dataset.html')


@init_page.route('/meeting.html')
def meeting():
	'''
	常用meeting下载
	:return:
	'''
	return render_template('pages/meeting.html')


@init_page.route('/paper.html')
def paper():
	'''
	常用paper下载
	:return:
	'''
	return render_template('pages/paper.html')


@init_page.route('/')
@init_page.route('/index')
@init_page.route('/index.html')
def index():
	'''
	首页
	:return:
	'''
	return render_template('index.html')  # 使用模板会有动画失效的问题


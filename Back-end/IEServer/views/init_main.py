#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:main
   Author:jasonhaven
   date:18-8-28
-------------------------------------------------
   Change Activity:18-8-28:
-------------------------------------------------
"""

from flask import  render_template,Blueprint

init_main=Blueprint('init_main',__name__)

'''
首页的右侧内部页面定义
'''

@init_main.route('/main.html')
def main():
	return render_template('main/main.html')


@init_main.route('/main_word_embedding.html')
def main_word_embedding():
	return render_template('main/main_word_embedding.html')


@init_main.route('/main_keyword.html')
def main_keyword():
	return render_template('main/main_keyword.html')


@init_main.route('/main_ner.html')
def main_ner():
	return render_template('main/main_ner.html')


@init_main.route('/main_re.html')
def main_re():
	return render_template('main/main_re.html')


@init_main.route('/main_topic.html')
def main_topic():
	return render_template('main/main_topic.html')


@init_main.route('/main_text.html')
def main_text():
	return render_template('main/main_text.html')

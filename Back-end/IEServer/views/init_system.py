#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:init_system
   Author:jasonhaven
   date:18-8-30
-------------------------------------------------
   Change Activity:18-8-30:
-------------------------------------------------
"""

from flask import  render_template,Blueprint

init_system=Blueprint('init_system',__name__)


@init_system.route('/404.html')
def page_not_found():
	return render_template('system/404.html'),404


@init_system.route('/500.html')
def server_interval():
	return render_template('system/500.html'),500



@init_system.route('/login.html')
def login():
	return render_template('system/login.html')



@init_system.route('/register.html')
def regisiter():
	return render_template('system/register.html')


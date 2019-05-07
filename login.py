#!/usr/bin/python3

import sys
import os
import urllib

import cgi
from http.cookies import SimpleCookie

import lib.consts as cnst
import lib.session as session
from lib.main import web
from lib.main import QString
from lib.layout1 import Layout
from lib.layout1 import layout1
from lib.log import Log
from lib.user import User

@web
@layout1
def main():
	redirect_path = '/'
	if 'redirect' in QString.params.keys():
		redirect_path = '/' + urllib.parse.unquote(QString.params['redirect'].value)

	# Get username from cookie (which will be saved when you login)
	username = ''
	if 'HTTP_COOKIE' in os.environ:
		cookies = SimpleCookie(os.environ['HTTP_COOKIE'])
		if 'last_user' in cookies:
			username = cookies['last_user'].value
		# Log user out if they try to access login page while logged in for whatever weird reason
		if 'session' in cookies:
			session_cookie = cookies['session']
			session.logout(session_cookie)
			Layout.pg.add_cookie(session_cookie)

	Layout.pg.add_script('input.js')
	Layout.pg.add_binding('username', username)
	Layout.pg.add_binding('redirect_path', redirect_path)
	Layout.pg.display_file('login.html')

#!/usr/bin/python3

import os

import cgi
from http.cookies import SimpleCookie

import lib.session as session
from lib.main import web
from lib.layout1 import Layout
from lib.layout1 import layout1
from lib.log import Log

@web
@layout1
def main():
	if 'HTTP_COOKIE' in os.environ:
		cookies = SimpleCookie(os.environ['HTTP_COOKIE'])
		# Log user out if they try to access register page while logged in for whatever weird reason
		if 'session' in cookies:
			session_cookie = cookies['session']
			session.logout(session_cookie)
			Layout.pg.add_cookie(session_cookie)

	Layout.pg.add_script('input.js')
	Layout.pg.display_file('register.html')

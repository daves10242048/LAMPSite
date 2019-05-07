#!/usr/bin/python3

import cgi

import lib.site.login as login
import lib.util.security as security
from lib.main import web
from lib.main import QString
from lib.layout1 import Layout
from lib.layout1 import layout1
from lib.log import Log

def success_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Verification email has been resent. Please check your inbox.')
	Layout.pg.display_file('redirect_message.html')

def error_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Error: An unexpected error has occurred.')
	Layout.pg.display_file('redirect_message.html')

def not_logged_in_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Error: You must be logged in to perform this action.')
	Layout.pg.display_file('redirect_message.html')

def already_verified_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Error: Your email address is already verified.')
	Layout.pg.display_file('redirect_message.html')

@web
@layout1
def main():
	user = login.fetch_logged_in_user()
	if user is None:
		not_logged_in_msg()
		return

	if user.verified:
		already_verified_msg()
		return

	try:
		security.send_verification_email(user, user.email)
		success_msg()
	except Exception as e:
		error_msg()
		Log.log_error(str(e))

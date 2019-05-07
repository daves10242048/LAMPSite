#!/usr/bin/python3

from datetime import datetime

import cgi
import lib.site.login as login
import lib.util.security as security
import lib.sqlwrapper as sqlwrapper
from lib.main import web
from lib.main import QString
from lib.layout1 import Layout
from lib.layout1 import layout1
from lib.log import Log

def success_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Congratulations, your account is now verified.')
	Layout.pg.display_file('redirect_message.html')

def wrong_email_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Error: The email address in your profile does not match with the email address being verified.')
	Layout.pg.display_file('redirect_message.html')

def error_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Error: An unexpected error has occurred. Your account cannot be verified at this time.')
	Layout.pg.display_file('redirect_message.html')

def not_logged_in_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Error: You must be logged in to verify your account.')
	Layout.pg.display_file('redirect_message.html')

def invalid_msg():
	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', 'Error: Verification code has expired or is invalid, or you are logged in as the wrong user.')
	Layout.pg.display_file('redirect_message.html')

def is_base64_string(string):
	return True if all((c >= 'a' and c <= 'z') or (c >= 'A' or c <= 'Z') or (c >= '0' or c <= '9') or c == '-' or c == '_' for c in string) else False

def is_valid_code(code):
	return True if len(code) == 43 and is_base64_string(code) else False

@web
@layout1
def main():
	if 'error' in QString.params.keys() and QString.params['error'].value == 'true':
		error_msg()
		return

	user = login.fetch_logged_in_user()
	if user is None:
		not_logged_in_msg()
		return

	if 'code' not in QString.params.keys() or not is_valid_code(QString.params['code'].value):
		invalid_msg()
		return

	code = QString.params['code'].value

	try:
		conn = sqlwrapper.connect('dbname')
		rows = conn.select_filter_equal('verification_codes', ('email', 'expiration_date'), ('code', 'user_id'), (code, user.id))

		if len(rows) == 0:
			invalid_msg()
			return

		(email, expiration_date) = rows[0]
		if user.email != email:
			wrong_email_msg()
			return

		if datetime.now() > expiration_date:
			invalid_msg()
			return

		security.verify_account(user.id)
		success_msg()

	except Exception as e:
		error_msg()
		Log.log_error(str(e))

	finally:
		conn.close()

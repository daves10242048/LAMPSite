#!/usr/bin/python3

import lib.site.login as login
import lib.site.display as display
from lib.main import web
from lib.layout1 import Layout
from lib.layout1 import layout1
from lib.log import Log

@web
@layout1
def main():
	user = login.fetch_logged_in_user()

	msg = ''
	if user is None:
		username = 'please log in'
	else:
		username = '<font class="{0}">{1}</font>'.format('username', display.username_html(user))
		if user.email is not None and not user.verified:
			msg = '<b>Note</b>: your account is not yet verified. Please click on the link in the confirmation email to verify your account.' \
			    + '<br/>If you did not receive a confirmation email or it has expired, <a class="userlink" href="/resend.py">click here.</a>' \
				+ '<br/>(Verification email may take a few minutes to send. Please check your spam folder if you do not see it in your inbox.)'

	Layout.pg.add_binding('username', username)
	Layout.pg.add_binding('messages', msg)
	Layout.pg.display_file('index.html')
#!/usr/bin/python3

import os
import urllib

import cgi
from html import escape

import lib.consts as cnst
import lib.util.htmlutil as htmlutil
import lib.site.login as login
import lib.site.display as display
from lib.main import web
from lib.main import QString
from lib.layout1 import Layout
from lib.layout1 import layout1
from lib.log import Log
from lib.user import User
from lib.role import Role

@web
@layout1
def main():
	this_user = login.fetch_logged_in_user()
	profile_userid = None

	if this_user is not None:
		userid = this_user.id

		profile_userid = userid
		if 'id' in QString.params.keys():
			try:
				profile_userid = int(QString.params['id'].value)
			except:
				profile_userid = -1

	table_contents = ''
	if profile_userid is not None:
		profile_user = User.load_user(profile_userid)
		show_hidden = False
		if profile_userid == userid or (this_user is not None and Role.SPY in this_user.get_full_role_titles()):
			show_hidden = True

		if profile_user is not None and (profile_user.public or show_hidden):
			table_contents += htmlutil.create_table_row(['User ID', escape(str(profile_userid))], 'highlight')
			table_contents += htmlutil.create_table_row(
				[
					'Username', '<font class="{0}">{1}</font>'.format('username', display.username_html(profile_user))
				],
				'highlight'
			)
			if show_hidden or profile_user.public_email:
				email = profile_user.email if profile_user.email is not None else ''
				verified_html = ''
				if profile_user.email is not None:
					if profile_userid == userid:
						if profile_user.verified:
							verified_html = '<span title="{0}"><img src="{1}" alt="{2}" style="position:relative; top:2px; left: 3px;"/></span>'.format('Verified Email', '/img/verified.png', 'Verified')
						else:
							verified_html = '<span title="{0}"><img src="{1}" alt="{2}" style="position:relative; top:2px; left: 3px;"/></span>'.format('Your email is unverified.', '/img/unverified.png', 'Unverified')
				if profile_user.public_email:
					table_contents += htmlutil.create_table_row(['Email', escape(email) + verified_html], 'highlight')
				else:
					table_contents += htmlutil.create_table_row(['<i>Email</i>', '<i>{0}</i>'.format(escape(email)) + verified_html], 'highlight')
			table_contents += htmlutil.create_table_row(['Roles', ', '.join(profile_user.get_base_role_titles(show_hidden=show_hidden, formatted=True))], 'highlight')

			Layout.pg.add_binding('user_name', escape(profile_user.name))
			Layout.pg.add_binding('table_contents', table_contents)
			Layout.pg.display_file('profile.html')
		else:
			Layout.pg.add_binding('redirect_url', '/profile.py')
			Layout.pg.add_binding('message', 'The specified user does not exist. Redirecting to your profile...')
			Layout.pg.display_file('redirect_message.html')
	else:
		login_url = cnst.Path.HOST + '/login.py?redirect=' + urllib.parse.quote(os.environ['SCRIPT_NAME'][1:], safe='')
		print("Content-Type: text/html")
		print('Location: ' + login_url)
		print()
#!/usr/bin/python3

import os
import urllib

import cgi

import lib.consts as cnst
import lib.util.htmlutil as htmlutil
import lib.util.dateutil as dateutil
import lib.site.display as display
import lib.site.login as login
import lib.sqlwrapper as sqlwrapper
from lib.main import web
from lib.main import QString
from lib.layout1 import Layout
from lib.layout1 import layout1
from lib.log import Log
from lib.user import User
from lib.role import Role

def fetch_user_list(page_length, page_num, order_by, sort_order, user_id, show_hidden):
	sort_column = 'user_name'
	if order_by == 'date':
		sort_column = 'register_time'

	order = 'asc'
	if sort_order == 'desc':
		order = sort_order

	try:
		conn = sqlwrapper.connect('dbname')
		c = conn.cursor()
		if show_hidden:
			c.execute(
				"select user_id " + 
				"from users " + 
				"order by " + sort_column + " " + order
			)
		else:
			c.execute(
				"select user_id " + 
				"from users " + 
				"where public != 0 or user_id = %s " +
				"order by " + sort_column + " " + order,
				(user_id,)
			)
		rows = c.fetchall()
		user_count = len(rows)
		start_index = (page_num - 1) * page_length
		return (
			rows[min(start_index, len(rows) - 1) : min(start_index + page_length, len(rows))],
			(user_count + page_length - 1) // page_length
		)

	finally:
		conn.close()


def get_params():
	page_length = 30
	page_num = 1
	order_by = 'username'
	sort_order = 'asc'

	if 'count' in QString.params.keys():
		try:
			page_length = int(QString.params['count'].value)
		except:
			pass

	if 'page' in QString.params.keys():
		try:
			page_num = int(QString.params['page'].value)
		except:
			pass

	if 'sort' in QString.params.keys():
		order_by = QString.params['sort'].value

	if 'order' in QString.params.keys():
		sort_order = QString.params['order'].value

	return page_length, page_num, order_by, sort_order


@web
@layout1
def main():
	this_user = login.fetch_logged_in_user()

	if this_user is not None:
		user_id = this_user.id
		is_spy = Role.SPY in this_user.get_full_role_titles()

		page_length, page_num, order_by, sort_order = get_params()

		page_num = max(page_num, 1)
		page_length = max(min(page_length, 100), 1)

		table_contents = ''
		user_list, page_count = fetch_user_list(page_length, page_num, order_by, sort_order, user_id, is_spy)

		page_list_html = display.generate_page_list(os.environ['SCRIPT_NAME'][1:], page_count, page_num, page_length, order_by, sort_order)
		page_list_table = htmlutil.create_table_row(page_list_html)

		for other_user_row in user_list:
			other_user_id = other_user_row[0]
			other_user = User.load_user(other_user_id)

			table_contents += htmlutil.create_table_row(
				[
					other_user_id,
					htmlutil.link_str('profile.py?id={0}'.format(other_user_id), display.username_html(other_user), 'userlink'),
					'<p>{0}</p>'.format(dateutil.date_string(other_user.register_time) + '<span style="float:right">{0}</span>'.format(dateutil.time_string(other_user.register_time))),
				],
				'highlight'
			)

		username_arrow = ''
		if order_by == 'username':
			username_arrow = '⯆' if sort_order == 'asc' else '⯅'

		date_arrow = ''
		if order_by == 'date':
			date_arrow = '⯆' if sort_order == 'asc' else '⯅'

		Layout.pg.bindings = { 
			'username_selected': 'selected' if order_by == 'username' else '',
			'date_selected': 'selected' if order_by == 'date' else '',
			'asc_selected': 'selected' if sort_order == 'asc' else '',
			'desc_selected': 'selected' if sort_order == 'desc' else '',
			'username_arrow': username_arrow,
			'date_arrow': date_arrow,
			'page_size': page_length,
			'page_table': page_list_table,
			'table_contents': table_contents
		}
		Layout.pg.add_script('page_users.js')
		Layout.pg.display_file('users.html')
	else:
		login_url = cnst.Path.HOST + '/login.py?redirect=' + urllib.parse.quote(os.environ['SCRIPT_NAME'][1:], safe='')
		print("Content-Type: text/html")
		print('Location: ' + login_url)
		print()

#!/usr/bin/python3

from lib.main import web
from lib.main import QString
from lib.layout1 import Layout
from lib.layout1 import layout1
from lib.log import Log

@web
@layout1
def main():
	message = 'Successfully logged out. Redirecting to the home page...'

	if 'error' in QString.params.keys():
		error_code = QString.params['error'].value
		if error_code == '1':
			message = 'You are already logged out.'
		elif error_code == '2':
			message = 'Error: Invalid token.'
		elif error_code == '0':
			message = 'Error: An unexpected error has occurred.'

	Layout.pg.add_binding('redirect_url', '/')
	Layout.pg.add_binding('message', message)
	Layout.pg.display_file('redirect_message.html')
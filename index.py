#!/home/yetiwerks/python/bin/python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import os
import time
import pages
import apps
import sys
today = time.strftime("%m/%d/%Y")
user = os.environ['REMOTE_USER']
site = os.environ['HTTP_HOST']
u_id, s_id = apps.get_creds(user, site)

form = cgi.FieldStorage()

func = cgi.escape(form.getvalue('f','gl'))
filt = cgi.escape(form.getvalue('fl','all'))
srt = cgi.escape(form.getvalue('s','asc'))
ky = cgi.escape(form.getvalue('k','hits'))
name = cgi.escape(form.getvalue('name','Name'))
link = cgi.escape(form.getvalue('link','http://links.taojoannes.com'))
l_id = cgi.escape(form.getvalue('li','1'))
c_id = cgi.escape(form.getvalue('c','1'))

title = 'Links 0.1'

def debug_block():
	cgi.print_form(form)
	cgi.print_directory()
	cgi.print_environ()

try:
	if func == 'gl':
		title, content = apps.get_links(u_id, s_id)
	elif func == 'al':
		title, content = apps.add_link(u_id, s_id, c_id, name, link)
	elif func == 'el':
		title, content = apps.edit_link(l_id)
	elif func == 'sl':
		title, content = apps.save_link(l_id, u_id, s_id, c_id, name, link)
	elif func == 'dl':
		title, content = apps.delete_link(l_id, u_id, s_id)
	elif func == 'gc':
		title, content = apps.get_categories()
	elif func == 'ac':
		title, content = apps.add_category(name)
	elif func == 'ec':
		title, content = apps.edit_category(c_id)
	elif func == 'sc':
		title, content = apps.save_category(c_id, name)
	elif func == 'dc':
		title, content = apps.delete_category(c_id)
	elif func == 'go':
		title, content = apps.go(l_id)
	else:
		raise
except Exception, e:
	title = 'Error'
	pages.head(title)
	debug_block()
	pages.foot()
	raise

pages.head(title)
print content
pages.foot()

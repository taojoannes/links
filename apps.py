import MySQLdb as mdb
import os
con = mdb.connect('localhost', 'links','links','links')
cur = con.cursor()

def get_uid(user):
	cur.execute('''
SELECT id
FROM users 
WHERE name = %s
''', (user,))
	val = cur.fetchone()
	return val[0]

def add_uid(user):
	cur.execute('''
INSERT
INTO users
(name)
VALUES (%s)
''', (user,))
	con.commit()
	cur.execute('''
SELECT
LAST_INSERT_ID()
''')
	val = cur.fetchone()
	return val[0]

def get_sid(site):
	cur.execute('''
SELECT id
FROM sites 
WHERE name = %s
''', (site,))
	val = cur.fetchone()
	return val[0]

def add_sid(site):
	cur.execute('''
INSERT
INTO sites
(name)
VALUES (%s)
''', (site,))
	con.commit()
	cur.execute('''
SELECT
LAST_INSERT_ID()
''')
	val = cur.fetchone()
	return val[0]

def get_uname(u_id):
	cur.execute('''
SELECT name
FROM users
WHERE id = %s
''', (u_id,))
	val = cur.fetchone()
	return val[0]

def get_site(s_id):
	cur.execute('''
SELECT name
FROM sites
WHERE id = %s
''', (s_id,))
	val = cur.fetchone()
	return val[0]

def get_cname(c_id):
	cur.execute('''
SELECT name
FROM categories
WHERE id = %s
''', (c_id,))
	val = cur.fetchone()
	return val[0]

def get_creds(user, site):
	try:
		u_id = get_uid(user)
	except Exception, e:
		u_id = add_uid(user)
	try:
		s_id = get_sid(site)
	except Exception, e:
		s_id = add_sid(site)
	return (u_id, s_id)


def get_links(u_id, s_id):
	cur.execute('''
SELECT * 
FROM links
WHERE u_id = %s
AND s_id = %s
''', (u_id, s_id))
	links = cur.fetchall()
	title = '''%s's links''' % get_uname(u_id)
	content = '''
<div id="accordion">
	
	<h3>Add Link</h3>
	<div>
		<form name="add_link">
		<input type="hidden" name="f" value="al">
		<select name="c">
		%s
		</select><br>
		<input type="text" name="name" placeholder="link name"><br>
		<input type="text" name="link" placeholder="link URL">
		<input type="submit" style="display:none"/>
		</form>
	</div>
''' % (get_categories(0))
	link_dict = {}
	for l_id, c_id, name, link, u_id, hits, s_id in links:
		try:
			c_list = link_dict[c_id]
			c_list.append((l_id,name,link,hits),)
		except KeyError:
			link_dict[c_id] = [(l_id,name,link,hits)]
	for c_id, link_list in link_dict.iteritems():
		content = '''%s
	<h3>%s</h3>
		<div>
''' % (content, get_cname(c_id))
		for id, name, link, hits in link_list:
			content = '''%s
	<div class="menu_row">
		<a href="?f=go&li=%s" title="(%s) %s">
		<div class="menu_item" onclick=>
		%s
		</div>
		</a>
		<div class="edit_item" onClick="javascript:location.href='/?f=dl&li=%s'">
		<img src="/images/icons/essential-ui/png/cross106.png" width=25px height=25px>
		</div>
		<div class="edit_item" onClick="javascript:location.href='/?f=el&li=%s'">
		<img src="/images/icons/essential-ui/png/settings60.png" width=25px height=25px>
		</div>
	</div>
		''' % (content, id, hits, link, name, id, id)
		content = '''%s
		</div>''' % content
			
	content = '''%s
	<h3>Categories</h3>
	<div>
		<form name="add_category">
		<input type="hidden" name="f" value="ac">
		<input type="text" name="name" placeholder="category">
		<input type="submit" style="display:none"/>
		</form>
		<hr>
		%s
	</div>
''' % (content, list_categories())
	return (title, content)
		
def add_link(u_id, s_id, c_id, name, link):
	cur.execute('''
INSERT INTO links
(c_id, name, link, u_id, s_id)
VALUES (%s, %s, %s, %s, %s)
''', (c_id, name, link, u_id, s_id))
	con.commit()
	title = "link added"
	content = '''<META http-equiv="refresh" content="0;URL=%s">''' % os.environ['HTTP_REFERER']
	return (title, content)
	
def edit_link(l_id):
	cur.execute('''
SELECT name, link, c_id
FROM links
WHERE id = %s
''', (l_id,))
	name, link, c_id = cur.fetchone()
	title = "Editing %s" % name
	content = '''
<form name="edit_link" action="/" method="post">
<input type="hidden" name="f" value="sl">
<input type="hidden" name="li" value="%s">
<select name="c">
%s
</select><br>
<input type="text" name="name" value="%s"><br>
<input type="text" name="link" value="%s"><br>
<input type="submit" value="Save">
</form>
''' % (l_id, get_categories(c_id), name, link)
	return (title, content)

def save_link(l_id, u_id, s_id, c_id, name, link):
	cur.execute('''
UPDATE links
SET 
c_id = %s,
name = %s,
link = %s
WHERE id = %s
AND u_id = %s
AND s_id = %s
''', (c_id, name, link, l_id, u_id, s_id))
	con.commit()
	title = "link %s updated" % name
	content = '''<META http-equiv="refresh" content="0;URL=/">'''
	return (title, content)
	
def delete_link(l_id, u_id, s_id):
	cur.execute('''
DELETE FROM links
WHERE id = %s
AND u_id = %s
AND s_id = %s
''', (l_id, u_id, s_id))
	con.commit()
	title = 'link deleted'
	content = '''<META http-equiv="refresh" content="0;URL=%s">''' % os.environ['HTTP_REFERER']
	return (title, content)

def get_categories(c_id):
	cur.execute('''
SELECT id, name
FROM categories
ORDER BY name ASC
''')
	val = ''
	results = cur.fetchall()
	for id, name in results:
		if id == c_id:
			val = '''%s
<option SELECTED value="%s">%s</option>''' % (val, id, name)
		else:
			val = '''%s
<option value="%s">%s</option>''' % (val, id, name)
	return val

def list_categories():
	cur.execute('''
SELECT id, name
FROM categories
ORDER BY name ASC
''')
	val = ''
	results = cur.fetchall()
	for id, name in results:
		val = '''%s
%s 
<a href="?f=ec&c=%s">[e]</a>	
<a href="?f=dc&c=%s">[d]</a><br>	
''' % (val, name, id, id)
	return val
		
def add_category(name):
	cur.execute('''
INSERT INTO categories
(name) 
VALUES (%s)
''', (name,))
	con.commit()
	title = "category added"
	content = '''<META http-equiv="refresh" content="0;URL=%s">''' % os.environ['HTTP_REFERER']
	return (title, content)
def edit_category(c_id):
	name = get_cname(c_id)
	title = 'Edit Category %s' % name
	content = '''
<form action="/" method="post">
<input type="hidden" name="f" value="sc">
<input type="hidden" name="c" value="%s">
<input type="text" name="name" value="%s">
<input type="submit" value="Save">
</form>
''' % (c_id, name)
	return (title, content)

def save_category(c_id, name):
	cur.execute('''
UPDATE categories
SET
name = %s
WHERE id = %s
''', (name, c_id))
	con.commit()
	title = "Updated %s" % name
	content = '''<META http-equiv="refresh" content="0;URL=/">''' 
	return (title, content)
def delete_category(c_id):
	cur.execute('''
DELETE FROM categories
WHERE id = %s
''' % (c_id,))
	con.commit()
	title = "Deleted"
	content = '''<META http-equiv="refresh" content="0;URL=/">''' 
	return (title, content)
def go(l_id):
	cur.execute('''
SELECT link, hits, name
FROM links
WHERE id = %s
''', (l_id,))
	link, hits, name = cur.fetchone()
	hits += 1
	cur.execute('''
UPDATE links
SET hits = %s
WHERE id = %s
''', (hits, l_id))
	con.commit()
	title = name
	content = '''<META http-equiv="refresh" content="0;URL=%s">''' % link
	return (title, content)

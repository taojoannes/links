Links 

This is just a very simple and unsophisticated link management system. 

It works great loaded in a Firefox sidebar.

Features:

* links are private, only displayed to the user they belong to
* click counting to track most used

Setup:

You need a mysql database and user with write access.

Edit apps.py, change the mdb.connect statement to reflect your database and user.

	 con = mdb.connect('localhost', 'user','pass','database')

Links uses simple .htaccess controls, a sample .htaccess file is included in the archive.

You will need to change the  AuthUserFile line to point to a valid .htpasswd file

	AuthUserFile /home/yetiwerks/auth/passwd

To create a .htpasswd file:
	htpasswd -c <file> <user>

To add a user:
	htpasswd <file> <user>


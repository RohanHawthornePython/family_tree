import sqlite3, os
from flask import g

def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()    

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(os.path.join('/home/pi/webapp/flaskr.db'))
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def check_user(user):
	# check if user already exists
	db = get_db()
	cur = db.cursor()
	cur.execute("SELECT password FROM user WHERE username=?", [user])
	passwd = cur.fetchone()
	if passwd:
		return passwd[0]
	else:
		return None

def add_user(username,password):
	# add a new user
	db = get_db()
	db.execute("insert into user (username, password) values (?, ?)", [username, password])
	db.commit()
	
def add_person(fullname,gender,dob):
	# add a new user
	db = get_db()
	cur = db.cursor()
	cur.execute("insert into person (fullname, gender, dob) values (?, ?, ?)", [fullname, gender, dob])
	db.commit()
	return cur.lastrowid

def add_marriage(root, spouse, relationship):
	print ("adding marriage between " + root + " and " + spouse)

def add_child(root, child):
	print ("adding child " + child + " to " + root)
	
import os, model, tree
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, escape, Markup

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY=b'?$Vx`j?C?GG>\n\xec]/'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.teardown_appcontext
def close_db(error):
	model.close_db(error)
	
def init_db():
	db = model.get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()
	
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', name=escape(session['username']), magic_html=Markup(tree.get_tree()))
    return render_template('splash.html')
    
@app.route('/register', methods=['GET','POST'])
def register():
	error = None
	if request.method == 'POST':
		if model.check_user(escape(request.form['username'])):
			error = 'Username already exists'
		else:
			session['username'] = request.form['username']
			model.add_user(escape(request.form['username']), request.form['password'])
			flash('You were registered')
			return redirect(url_for('index'))
	return render_template('register.html', error=error, registering=True)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		test_password = model.check_user(escape(request.form['username']))
		if not test_password or test_password != request.form['password']:
			error = 'Invalid username/password combination'
		else:
			session['username'] = request.form['username']
			flash('Welcome back %s' % escape(request.form['username']))
			return redirect(url_for('index'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/addperson', methods=['GET','POST'])
def addperson():
	error = None
	gender = request.values.get("gender") 
	if request.method == 'GET' and gender:
		return render_template('addperson.html', gender=gender)
	elif request.method == 'POST':
		currid = request.values.get('current_person')
		newid = model.add_person(request.form['fullname'],request.form['gender'],request.form['dob'])
		relationship = request.values.get('relationship')
		if relationship and relationship == 'bride' or relationship == 'groom':
			model.add_marriage(currid, newid, relationship)
		elif relationship and relationship == 'child':
			model.add_child(currid, newid)
		flash('Person added')
		return redirect(url_for('index'))
	else:
		return render_template('addperson.html')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'skey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'logindb'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	display = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM logintable WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			display = 'Logged in successfully...'
			return render_template('profile.html', display = display)
		else:
			display = 'Incorrect information please check you password and username'
	return render_template('login.html', display = display)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	display = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM logintable WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			display = 'Account already exists !'
		else:
			cursor.execute('INSERT INTO logintable VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			display = 'You have successfully registered !'
	elif request.method == 'POST':
		display = 'Please fill out the form !'
	return render_template('register.html', display = display)

@app.route("/table")
def table():
	cursor=mysql.get_db().cursor()
	query="CREATE TABLE IF NOT EXISTS logintable(id INT NOT NULL AUTO_INCREMENT,username VARCHAR(50) NOT NULL,password VARCHAR(100) NOT NULL ,email VARCHAR(50) NOT NULL,PRIMARY KEY(id)"
	cursor.execute(query)
	return "succesfull"


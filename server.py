#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

from flask_login import LoginManager, logout_user
import os
from sqlalchemy import *

from models import Account
from models.User import User
from models.Account import Account
from pprint import pprint
from flask_login import login_user, login_required, current_user
from flask import Flask, request, render_template, g, redirect, Response, jsonify, flash

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = "secret"
login_manager = LoginManager()
login_manager.init_app(app)

# XXX: The Database URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = "pd2720"
DB_PASSWORD = "QtRW!xRN84KZ"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_SERVER + "/proj1part2"

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

# Here we create a test table and insert some values in it
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

with open('migrations/initial.sql', 'r') as file:
    data = file.read()

engine.execute(data)

res = engine.execute("SELECT * FROM Users where id = 1;")

user = User.from_row(res.fetchone())


@app.before_request
def before_request():
    """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback;
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
    """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

    # DEBUG: this is debugging code to see what request looks like
    pprint(request)

    if current_user is not None and current_user.is_authenticated:
        return redirect('/accounts')
    else:
        return redirect('/login')
    #
    # example of a database query
    #
    cursor = g.conn.execute("SELECT name FROM test")
    names = []
    for result in cursor:
        names.append(result['name'])  # can also be accessed using result[0]
    cursor.close()

    #
    # Flask uses Jinja templates, which is an extension to HTML where you can
    # pass data to a template and dynamically generate HTML based on the data
    # (you can think of it as simple PHP)
    # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
    #
    # You can see an example template in templates/index.html
    #
    # context are the variables that are passed to the template.
    # for example, "data" key in the context variable defined below will be
    # accessible as a variable in index.html:
    #
    #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
    #     <div>{{data}}</div>
    #
    #     # creates a <div> tag for each element in data
    #     # will print:
    #     #
    #     #   <div>grace hopper</div>
    #     #   <div>alan turing</div>
    #     #   <div>ada lovelace</div>
    #     #
    #     {% for n in data %}
    #     <div>{{n}}</div>
    #     {% endfor %}
    #
    context = dict(data=names)

    #
    # render_template looks in the templates/ folder for files.
    # for example, the below file reads template/index.html
    #
    return render_template("index.html", **context)


# ACCOUNTS ENTITY

@app.route('/accounts', methods=['GET'])
@login_required
def accounts_page():
    account_rows = engine.execute("SELECT * FROM Accounts where uid=%s LIMIT 20;", current_user.id).fetchall()
    accounts = [Account.from_row(row).__dict__ for row in account_rows]
    return render_template("accounts/list.html", accounts=accounts)



@login_manager.user_loader
def load_user(user_id):

    result = engine.execute('SELECT * FROM Users where id=' + str(user_id))
    if result is None:
        return None
    else:
        return User.from_row(result.fetchone())


@app.post('/login')
def login():
    info = request.form.to_dict()
    email = info.get('email', 'guest')
    password = info.get('password', '')
    result = engine.execute("SELECT * FROM Users where email=%s and password=%s", (email, password))
    if result.rowcount > 0:
        user = User.from_row(result.fetchone())
        login_user(user)
        pprint(current_user)
        flash("You were successfully logged in")
        return redirect('/accounts')
    else:
        flash("Username or Password Error", 'error')
        return redirect('/login')
        # return jsonify({"status": 401,
        #                 "reason": "Username or Password Error"})


@app.get('/login')
def get_login_page():
    return render_template("auth/login.html", **{})


@app.post('/register')
def register():
    info = request.form.to_dict()
    email = info['email']
    result = engine.execute("SELECT * FROM Users where email=%s;", email)
    if result.rowcount > 0:
        flash("This email is taken")
        return redirect('/register')
    else:
        password = info['password']
        name = info['name']
        user_row = g.conn.execute(text("INSERT INTO Users(name, email, password) VALUES(:name,:email,:pwd) RETURNING id"), {'name':name, 'email':email, 'pwd':password}).fetchone()
        result = g.conn.execute("SELECT * FROM Users where id=%s", user_row.id)
        user = User.from_row(result.fetchone())
        login_user(user)
        flash("You were successfully logged in")
        return redirect('/accounts')

@app.get('/register')
def get_register_page():
    return render_template("auth/register.html", **{})

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()

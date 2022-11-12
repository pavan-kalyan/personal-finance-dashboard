#!/usr/bin/env python3
import datetime

from flask_login import LoginManager, logout_user
import os
from sqlalchemy import *

# from models import Account, Transaction
from models.Organization import Organization
from models.User import User
from models.Account import Account
from models.Contact import Contact
from models.Category import Category
from models.Transaction import Transaction
from models.Tag import Tag
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
        import traceback
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

#TODO: VALIDATION
# ACCOUNTS ENTITY
@app.get('/accounts')
@login_required
def accounts_page():
    page_num = request.args.get('page')
    if page_num is None or int(page_num) < 0:
        page_num = 0
    else:
        page_num = int(page_num)

    account_rows = g.conn.execute(
        text(
            "SELECT A.*, O.name as org_name FROM Accounts A join Organizations O on A.org_id = O.id where uid=:uid LIMIT 20 OFFSET :page_num ;"),
        uid=current_user.id, page_num=page_num * 20).fetchall()
    accounts = [Account.from_row(row).__dict__ for row in account_rows]
    return render_template("accounts/list.html", accounts=accounts, page_num=page_num)


@app.get('/accounts/<id>/edit')
@login_required
def account_edit_page(id):
    org_rows = g.conn.execute("SELECT * FROM Organizations;").fetchall()
    account_row = g.conn.execute(
        "SELECT A.*,O.name as org_name FROM Accounts A join Organizations O on A.org_id = O.id WHERE A.uid=%s AND A.id=%s",
        (current_user.id, id)).fetchone()
    if account_row is None:
        flash('Did not find account or it does not exist')
        return redirect('/accounts')
    account = Account.from_row(account_row)
    organizations = [Organization.from_row(row).__dict__ for row in org_rows]
    return render_template("accounts/edit.html", organizations=organizations, account=account)


@app.post('/accounts/<id>/edit')
@login_required
def edit_account(id):
    info = request.form.to_dict()
    org_id = info['organization']
    name = info['name']
    type = info['type']
    balance = info['balance']
    account_number = info['account_number']
    uid = current_user.id
    g.conn.execute(text(
        "UPDATE Accounts SET name=:name, org_id =:org_id, type=:type, balance=:balance, account_number=:a_num WHERE uid=:uid AND id=:id"),
        id=id, uid=uid, balance=balance, a_num=account_number, name=name, org_id=org_id, type=type)
    return redirect('/accounts')


@app.get('/accounts/create')
@login_required
def account_creation_page():
    org_rows = g.conn.execute("SELECT * FROM Organizations;").fetchall()
    organizations = [Organization.from_row(row).__dict__ for row in org_rows]
    return render_template("accounts/create.html", organizations=organizations)


@app.post('/accounts')
@login_required
def accounts():
    if request.method == "POST":
        info = request.form.to_dict()
        org_id = info['organization']
        name = info['name']
        type = info['type']
        balance = info['balance']
        account_number = info['account_number']
        uid = current_user.id
        account_row = g.conn.execute(
            text(
                "INSERT INTO Accounts (type, name, balance, account_number, org_id, uid) VALUES (:type, :name, :balance, :a_num, :org_id, :uid) RETURNING ID"),
            type=type, name=name, balance=balance, a_num=account_number, org_id=org_id, uid=uid).fetchone()
        flash('Account has been added')
        return redirect('/accounts')

    return redirect('/accounts')


@app.route('/accounts/<id>/delete/', methods=['GET'])
@login_required
def delete_account(id):
    del_res = g.conn.execute("DELETE FROM Accounts where uid=%s AND id=%s", (current_user.id, id))
    if del_res.rowcount < 1:
        flash('Failed to delete account. May not exist or you don\'t have the right permissions')
    return redirect('/accounts')


# TRANSACTIONS ENTITY
@app.route('/transactions', methods=['GET'])
@login_required
def transactions_page():
    page_num = request.args.get('page')
    if page_num is None or int(page_num) < 0:
        page_num = 0
    else:
        page_num = int(page_num)

    trans_rows = engine.execute(text("""
    SELECT T.*, A.name as account_name, A.account_number, C.name as contact, Cat.name as category
    FROM Transactions T JOIN Accounts A ON T.account_id=A.id FULL JOIN Contacts C ON T.contact_id=C.id FULL JOIN Categories Cat ON T.category_id=Cat.id
   where A.uid=:uid LIMIT 20 OFFSET :page_num;
    """), uid=current_user.id, page_num=page_num * 20).fetchall()

    transactions = [Transaction.from_row(row).__dict__ for row in trans_rows]
    return render_template("transactions/list.html", transactions=transactions, page_num=page_num)


@app.get('/transactions/<id>/edit')
@login_required
def transaction_edit_page(id):
    contact_rows = g.conn.execute("SELECT * FROM Contacts where uid=%s", current_user.id).fetchall()
    account_rows = g.conn.execute(
        "SELECT A.*, O.name as org_name FROM Accounts A join Organizations O on A.org_id = O.id where uid=%s",
        current_user.id).fetchall()
    category_rows = g.conn.execute("SELECT * FROM Categories where uid=%s", current_user.id).fetchall()

    transaction_row = g.conn.execute("""
        SELECT T.*, A.name as account_name, A.account_number, C.name as contact, Cat.name as category
        FROM Transactions T JOIN Accounts A ON T.account_id=A.id FULL JOIN Contacts C ON T.contact_id=C.id FULL JOIN Categories Cat ON T.category_id=Cat.id
        WHERE A.uid=%s AND T.id=%s
    """, (current_user.id, id)).fetchone()
    if transaction_row is None:
        flash('Did not find transaction or it does not exist')
        return redirect('/transactions')

    transaction = Transaction.from_row(transaction_row)
    contacts = [Contact.from_row(row).__dict__ for row in contact_rows]
    accounts = [Account.from_row(row).__dict__ for row in account_rows]
    categories = [Category.from_row(row).__dict__ for row in category_rows]

    return render_template("transactions/edit.html", contacts=contacts, accounts=accounts, categories=categories,
                           transaction=transaction)


@app.post('/transactions/<id>/edit')
@login_required
def edit_transaction(id):
    info = request.form.to_dict()
    date = info['date']
    amount = info['amount']
    acc_id = info['account']
    contact_id = info['contact'] if info['contact'] != "" else None
    category_id = info['category'] if info['category'] != "" else None
    memo = info['memo']
    g.conn.execute(text(
        "UPDATE Transactions SET date=:date, amount=:amount, account_id=:acc_id, contact_id=:contact_id, category_id=:category_id, memo=:memo WHERE id=:id"),
        date=date, id=id, amount=amount, acc_id=acc_id, contact_id=contact_id, category_id=category_id, memo=memo)
    return redirect('/transactions')


@app.get('/transactions/create')
@login_required
def transaction_creation_page():
    contact_rows = g.conn.execute("SELECT * FROM Contacts where uid=%s", current_user.id).fetchall()
    account_rows = g.conn.execute(
        "SELECT A.*, O.name as org_name FROM Accounts A join Organizations O on A.org_id = O.id where uid=%s",
        current_user.id).fetchall()
    category_rows = g.conn.execute("SELECT * FROM Categories where uid=%s", current_user.id).fetchall()

    contacts = [Contact.from_row(row).__dict__ for row in contact_rows]
    accounts = [Account.from_row(row).__dict__ for row in account_rows]
    categories = [Category.from_row(row).__dict__ for row in category_rows]
    return render_template("transactions/create.html", contacts=contacts, accounts=accounts, categories=categories, date=datetime.date.today())


@app.post('/transactions')
@login_required
def transactions():
    if request.method == "POST":
        info = request.form.to_dict()
        date = info['date']
        amount = info['amount']
        acc_id = info['account']
        contact_id = info['contact'] if info['contact'] != "" else None
        category_id = info['category'] if info['category'] != "" else None
        memo = info['memo']
        transaction_row = g.conn.execute(
            text(
                "INSERT INTO Transactions (date, amount, account_id, contact_id, category_id, memo) VALUES (:date, :amount, :acc_id, :contact_id, :category_id, :memo) RETURNING ID"),
            date=date, amount=amount, acc_id=acc_id, contact_id=contact_id, category_id=category_id,
            memo=memo).fetchone()
        flash('Transaction has been added')
        return redirect('/transactions')

    return redirect('/transactions')


@app.route('/transactions/<id>/delete/', methods=['GET'])
@login_required
def delete_transaction(id):
    del_res = g.conn.execute("DELETE FROM Transactions where id=%s", id)
    if del_res.rowcount < 1:
        flash('Failed to delete transaction. May not exist or you don\'t have the right permissions')
    return redirect('/transactions')


# CATEGORIES ENTITY
@app.route('/categories', methods=['GET'])
@login_required
def categories_page():
    page_num = request.args.get('page')
    if page_num is None or int(page_num) < 0:
        page_num = 0
    else:
        page_num = int(page_num)

    cat_rows = engine.execute(text("SELECT * FROM Categories where uid=:uid LIMIT 20 OFFSET :page_num;"),
                              uid=current_user.id, page_num=page_num * 20).fetchall()

    categories = [Category.from_row(row).__dict__ for row in cat_rows]
    return render_template("categories/list.html", categories=categories, page_num=page_num)


@app.get('/categories/<id>/edit')
@login_required
def category_edit_page(id):
    category_row = g.conn.execute("""
        SELECT *
        FROM Categories
        WHERE uid=%s AND id=%s
    """, (current_user.id, id)).fetchone()
    if category_row is None:
        flash('Did not find category or it does not exist')
        return redirect('/categories')

    category = Category.from_row(category_row)

    return render_template("categories/edit.html", category=category)


@app.post('/categories/<id>/edit')
@login_required
def edit_category(id):
    info = request.form.to_dict()
    name = info['name']
    group = info['group']
    g.conn.execute(text(
        "UPDATE Categories SET name=:name, group=:group WHERE id=:id"),
        name=name, group=group, id=id)
    return redirect('/categories')


@app.get('/categories/create')
@login_required
def category_creation_page():
    return render_template("categories/create.html")


@app.post('/categories')
@login_required
def categories():
    if request.method == "POST":
        info = request.form.to_dict()
        name = info['name']
        group = info['group']
        category_row = g.conn.execute(
            text(
                "INSERT INTO Categories (uid, name, \"group\") VALUES (:uid, :name, :group) RETURNING ID"),
            name=name, group=group, uid=current_user.id).fetchone()
        flash('Category has been added')
        return redirect('/categories')

    return redirect('/categories')


@app.route('/categories/<id>/delete/', methods=['GET'])
@login_required
def delete_category(id):
    del_res = g.conn.execute("DELETE FROM Categories where id=%s", id)
    if del_res.rowcount < 1:
        flash('Failed to delete category. May not exist or you don\'t have the right permissions')
    return redirect('/categories')


# TAGS ENTITY
@app.route('/tags', methods=['GET'])
@login_required
def tags_page():
    page_num = request.args.get('page')
    if page_num is None or int(page_num) < 0:
        page_num = 0
    else:
        page_num = int(page_num)

    tag_rows = engine.execute(text("SELECT * FROM Tags where uid=:uid LIMIT 20 OFFSET :page_num;"),
                              uid=current_user.id, page_num=page_num * 20).fetchall()

    tags = [Tag.from_row(row).__dict__ for row in tag_rows]
    return render_template("tags/list.html", tags=tags, page_num=page_num)


@app.get('/tags/<id>/edit')
@login_required
def tag_edit_page(id):
    tag_row = g.conn.execute("""
        SELECT *
        FROM Tags
        WHERE uid=%s AND id=%s
    """, (current_user.id, id)).fetchone()
    if tag_row is None:
        flash('Did not find tag or it does not exist')
        return redirect('/tags')

    tag = Tag.from_row(tag_row)

    return render_template("tags/edit.html", tag=tag)


@app.post('/tags/<id>/edit')
@login_required
def edit_tag(id):
    info = request.form.to_dict()
    name = info['name']
    g.conn.execute(text(
        "UPDATE Tags SET name=:name WHERE id=:id"),
        name=name,  id=id)
    return redirect('/tags')


@app.get('/tags/create')
@login_required
def tag_creation_page():
    return render_template("tags/create.html")


@app.post('/tags')
@login_required
def tags():
    if request.method == "POST":
        info = request.form.to_dict()
        name = info['name']
        tag_row = g.conn.execute(
            text(
                "INSERT INTO Tags (uid, name) VALUES (:uid, :name) RETURNING ID"),
            name=name, uid=current_user.id).fetchone()
        flash('Tag has been added')
        return redirect('/tags')

    return redirect('/tags')


@app.route('/tags/<id>/delete/', methods=['GET'])
@login_required
def delete_tag(id):
    del_res = g.conn.execute("DELETE FROM Tags where id=%s", id)
    if del_res.rowcount < 1:
        flash('Failed to delete Tag. May not exist or you don\'t have the right permissions')
    return redirect('/tags')

@login_manager.user_loader
def load_user(user_id):
    result = g.conn.execute('SELECT * FROM Users where id=' + str(user_id))
    if result is None:
        return None
    else:
        return User.from_row(result.fetchone())


@app.post('/login')
def login():
    info = request.form.to_dict()
    email = info.get('email', 'guest')
    password = info.get('password', '')
    result = g.conn.execute("SELECT * FROM Users where email=%s and password=%s", (email, password))
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
    result = g.conn.execute("SELECT * FROM Users where email=%s;", email)
    if result.rowcount > 0:
        flash("This email is taken")
        return redirect('/register')
    else:
        password = info['password']
        name = info['name']
        user_row = g.conn.execute(
            text("INSERT INTO Users(name, email, password) VALUES(:name,:email,:pwd) RETURNING id"),
            {'name': name, 'email': email, 'pwd': password}).fetchone()
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

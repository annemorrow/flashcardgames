# views.py


import sqlite3
from functools import wraps

from flask import Flask, flash, redirect, render_template, \
    request, session, url_for, g
    

# config

app = Flask(__name__)
app.config.from_object('_config')


# helper functions

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def get_list_names(username):
    g.db = connect_db()
    cur = g.db.execute('''select list_name from users inner join lists on 
                users.user_id=lists.user_id where username is "{}"'''.format(username))
    list_names = [str(row[0]) for row in cur.fetchall()]
    g.db.close()
    return list_names

def get_questions(username, list_name):
    g.db = connect_db()
    cur = g.db.execute('''select question, answer from 
              users inner join lists on users.user_id=lists.user_id 
              inner join questions on lists.list_id=questions.list_id
              where username="{}" and list_name="{}"'''.format(username, list_name))
    q = []
    for row in cur:
        item = {}
        item["question"] = str(row[0])
        item["answer"] = str(row[1])
        q.append(item)
    g.db.close()
    return q

# route handlers

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
                or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('questions'))
    return render_template('login.html')

@app.route('/questions/')
@login_required
def questions():
    question_lists = get_list_names("admin")
    full_question_set = {}
    for list_name in question_lists:
        full_question_set[list_name] = get_questions("admin", list_name)
    return render_template(
        'questions.html',
        full_question_set=full_question_set
    )

# Add new list
@app.route('/add_list/', methods=['POST'])
@login_required
def new_list():
    g.db = connect_db()
    cur = g.db.execute('select user_id from users where username is "admin"')
    user_id = 0
    for row in cur:
        user_id = str(row[0])
    list_name = request.form['list_name']
    if not list_name:
        flash("Your list needs a name")
        return redirect(url_for('questions'))
    else:
        g.db.execute('insert into lists (user_id, list_name) values (?, ?)', [user_id, request.form['list_name']])
        g.db.commit()
        g.db.close()
        flash('New list was successfully added.  Thanks.')
        return redirect(url_for('questions'))
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

def get_questions(list_id):
    g.db = connect_db()
    cur = g.db.execute('''select question_id, question, answer from questions where
                         list_id is "{}"'''.format(list_id))
    q = []
    for row in cur:
        item = {}
        item["question_id"] = str(row[0])
        item["question"] = str(row[1])
        item["answer"] = str(row[2])
        q.append(item)
    g.db.close()
    return q

def get_user_questions(user_id):
    # [{list_id:, list_name: , questions: [{question_id: question: answer:}, ]}, {list_id:, list_name: , questions: []}]
    g.db = connect_db()
    user_questions = []
    cur = g.db.execute('''select list_id, list_name from lists inner join users on
              users.user_id=lists.user_id where users.user_id is "{}"'''.format(user_id))
    for row in cur:
        item = {}
        item["list_id"] = str(row[0])
        item["list_name"] = str(row[1])
        user_questions.append(item)
    for item in user_questions:
        question_list = []
        cur = g.db.execute('''select question_id, question, answer from questions 
                          where list_id is "{}"'''.format(item["list_id"]))
        for row in cur:
            question = {}
            question["question_id"] = str(row[0])
            question["question"] = str(row[1])
            question["answer"] = str(row[2])
            question_list.append(question)
        item["questions"] = question_list
    g.db.close()
    return user_questions
        

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
    full_question_set = get_user_questions(1)
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
        g.db.execute('insert into lists (user_id, list_name) values (?, ?)', [user_id, list_name])
        g.db.commit()
        g.db.close()
        flash('New list was successfully added.  Thanks.')
        return redirect(url_for('questions'))

# Add new question
@app.route('/add_question/', methods=['POST'])
@login_required
def new_question():
    g.db = connect_db()
    list_id = request.form["list_id"]
    question = request.form["question"]
    answer = request.form["answer"]
    g.db.execute('insert into questions (list_id, question, answer) values (?, ?, ?)', [list_id, question, answer])
    g.db.commit()
    g.db.close()
    return redirect(url_for('questions'))
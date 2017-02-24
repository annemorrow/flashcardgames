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
    g.db = connect_db()
    cur = g.db.execute(
        '''select list_name from lists where user_id is 
        (select user_id from users where username is "admin")'''
    )
    question_lists = [
        row[0] for row in cur.fetchall()
    ]
    cur = g.db.execute(
        ''' select list_id, question, answer from questions'''
    )
    questions = [[row[0], str(row[1]), str(row[2])] for row in cur.fetchall()]
    for question in questions:
        cur = g.db.execute('select list_name from lists where list_id is ' + str(question[0]))
        question[0] = str(cur.fetchall()[0][0])
    g.db.close()
    return render_template(
        'questions.html',
        question_lists=question_lists,
        questions=questions
    )
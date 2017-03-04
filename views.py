# views.py



from functools import wraps
from flask import Flask, flash, redirect, render_template, \
    request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
    

# config

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Subject


# helper functions

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
    subjects = db.session.query(Subject)
    return render_template(
        'questions.html',
        subjects = subjects
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

# Delete question
@app.route('/delete/<int:question_id>/')
@login_required
def delete_question(question_id):
    g.db = connect_db()
    g.db.execute('delete from questions where question_id='+str(question_id))
    g.db.commit()
    g.db.close()
    flash('The question was deleted')
    return redirect(url_for('questions'))
# views.py



from functools import wraps
from flask import Flask, flash, redirect, render_template, \
    request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
    

# config

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Subject, Short_Answer_Question
from forms import AddSubjectForm

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
    short_answer_questions = db.session.query(Short_Answer_Question)
    form = AddSubjectForm()
    return render_template(
        'questions.html',
        subjects = subjects,
        short_answer_questions = short_answer_questions,
        form=form
    )

# Add new list
@app.route('/add_subject/', methods=['POST'])
@login_required
def new_subject():
    form = AddSubjectForm()
    flash("new subject function")
    if form.validate_on_submit():
        subject_name = form.name.data
        db.session.add(Subject(subject_name))
        db.session.commit()
        flash('New subject was successfully added.  Thanks.')
    else:
        flash(form.errors)
    return redirect(url_for('questions'))

# Add new question
@app.route('/add_question/', methods=['POST'])
@login_required
def new_question():
    subject_id = request.form["subject_id"]
    question = request.form["question"]
    answer = request.form["answer"]
    subject = db.session.query(Subject).filter_by(id=subject_id)[0]
    db.session.add(Short_Answer_Question(subject, question, answer))
    db.session.commit()
    return redirect(url_for('questions'))

# Delete question
@app.route('/delete/<int:question_id>/')
@login_required
def delete_question(question_id):
    db.session.query(Short_Answer_Question).filter_by(id = question_id).delete()
    db.session.commit()
    flash('The question was deleted')
    return redirect(url_for('questions'))
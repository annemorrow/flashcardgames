# models.py


from views import db

class Short_Answer_Question(db.Model):

    __tablename__ = 'short_answer_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject',
        backref=db.backref('short_answer_questions', lazy='dynamic'))
        
    def __init__(self, subject, question, answer=None):
        self.question = question
        self.answer = answer
        self.subject = subject
    
    def __repr__(self):
        return 'SAQuestion %r>' % self.question[:10]


class Subject(db.Model):

    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Subject %r>' % self.name
# models.py


from views import db


class Subject(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Subject %r>' % self.name
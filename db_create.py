from views import db
from models import Subject

# create the database and the db table
db.create_all()

# insert data
db.session.add(Subject("Math"))
db.session.add(Subject("English"))

# commit the changes
db.session.commit()
from views import db
from models import Subject, Short_Answer_Question

# create the database and the db table
db.create_all()



db.session.commit()
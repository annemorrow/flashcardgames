from views import db
from models import Subject, Short_Answer_Question

# create the database and the db table
db.create_all()

# insert data
#math = Subject("Math")
#english = Subject("English")
#db.session.add(math)
#db.session.add(english)

#db.session.add(Short_Answer_Question(math, "2 X 4", "8"))
#db.session.add(Short_Answer_Question(math, "9 X 20"))

# commit the changes
db.session.commit()
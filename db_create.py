# project/db_create.py


import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    
    # create the tables
    c.execute("""CREATE TABLE users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL)""")
    
    c.execute("""CREATE TABLE lists(list_id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL, list_name TEXT NOT NULL)""")
    
    c.execute("""CREATE TABLE questions(question_id INTEGER PRIMARY KEY AUTOINCREMENT,
             list_id INTEGER NOT NULL, question TEXT NOT NULL, answer TEXT)""")
    
    # insert dummy users into the tables
    c.execute("""INSERT INTO users (username) VALUES("testuser1")""")
    c.execute("""INSERT INTO users (username) VALUES("testuser2")""")
    c.execute("""INSERT INTO users (username) VALUES("testuser3")""")
    
    c.execute("""insert into lists (user_id, list_name) values(1, "science")""")
    c.execute("""insert into lists (user_id, list_name) values(1, "math")""")
    c.execute("""insert into lists (user_id, list_name) values(1, "history")""")
    
    c.execute("""insert into lists (user_id, list_name) values(2, "science")""")
    c.execute("""insert into lists (user_id, list_name) values(2, "technology")""")
    c.execute("""insert into lists (user_id, list_name) values(2, "family")""")
    
    c.execute("""insert into lists (user_id, list_name) values(3, "farming")""")
    
    c.execute("""insert into questions(list_id, question, answer) values(2, "3 x 4", "12")""")
    c.execute("""insert into questions(list_id, question, answer) values(2, "3 x 8", "24")""")
    c.execute("""insert into questions(list_id, question, answer) values(2, "3 x 15", "45")""")
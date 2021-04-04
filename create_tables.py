import sqlite3


co = sqlite3.connect("users.db")
c = co.cursor()

c.execute("CREATE TABLE jokes (jokes    TEXTFIELD, points INT, pk INT UNIQUE)")
c.execute("CREATE TABLE users (username TEXTFIELD, points INT               )")

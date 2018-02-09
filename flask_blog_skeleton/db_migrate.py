from app.backend import db
from instance.config import DATABASE_PATH

import sqlite3


with sqlite3.connect(DATABASE_PATH) as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()

    # temporary change the name of table
    c.execute("""ALTER TABLE users RENAME TO old_users""")

    # recreate a new table with updated schema
    db.create_all()

    # retrieve data from old table
    c.execute("""SELECT * FROM old_users ORDER BY id ASC""")

    # save all rows as a list of tuples
    data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'users') for row in c.fetchall()]

    # insert data to the new table
    c.executemany("""INSERT INTO users (id, first_name, last_name, username, email, password, registered_on, admin) VALUES (?, ?, ?, ?, ?, ?, ?)""", data)

    # delete old table
    c.execute("DROP TABLE old_users")

from app.backend import db
from instance.config import DATABASE_PATH

import sqlite3


with sqlite3.connect(DATABASE_PATH) as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()

    # temporary change the name of table
    c.execute("""ALTER TABLE posts RENAME TO old_posts""")

    # recreate a new table with updated schema
    db.create_all()

    # retrieve data from old table
    c.execute("""SELECT id, title, body, posted_date, last_edit_date, status, user_id FROM old_posts ORDER BY id ASC""")

    # save all rows as a list of tuples
    data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 'posts') for row in c.fetchall()]

    # insert data to the new table
    c.executemany("""INSERT INTO posts (id, title, body, posted_date, last_edit_date, status, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)""", data)

    # delete old table
    c.execute("DROP TABLE old_posts")

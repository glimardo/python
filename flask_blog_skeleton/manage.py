import os

from flask import Flask
from flask_script import Manager, prompt_bool

from app.backend import create_app
from app.backend import db

from app.backend.models import User, Post

from instance import config

from instance.config import DATABASE_PATH

import sqlite3


config_name = "development"
# config_name = "production"
# config_name = "testing"

app = create_app(config_name)
manager = Manager(app)


@manager.command
def initdb():
    '''
    Initialize the database
    '''
    db.create_all()
    print("Initialized the database")


@manager.command
def dropdb():
    '''
    Drop the database
    '''
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()
        print("Dropped the database")


@manager.command
def create_test_user():
    '''
    Create test user
    '''
    db.session.add(User(first_name='Test man', last_name='Last name test', username='test', email='test@test.test', password='test1234'))
    db.session.commit()


@manager.command
def create_admin():
    '''
    Create admin test user
    '''
    db.session.add(User(first_name='admin', last_name='admin', username='admin01', email='admin@admin.admin', password='admin123', admin=True))
    db.session.commit()


@manager.command
def try_update():
    new_account = User.query.filter_by(username='ironman').first()
    new_account.username = 'start'
    db.session.commit()


@manager.command
def db_migrate_post():
    '''
    Db migrate posts
    '''
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
        data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'posts') for row in c.fetchall()]
        
        # insert data to the new table
        c.executemany("""INSERT INTO posts (id, title, body, posted_date, last_edit_date, status, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)""", data)
        
        # delete old table
        c.execute("DROP TABLE old_posts")


if __name__ == "__main__":
    manager.run()

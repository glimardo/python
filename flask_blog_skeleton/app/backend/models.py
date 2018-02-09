import datetime

from flask import current_app
from . import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def __init__(self, first_name, last_name, username, email, password, admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password, 10).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False, unique=True)
    body = db.Column(db.String(9000), nullable=False)
    topic = db.Column(db.String(1000), nullable=False)
    tag = db.Column(db.String(1000), nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    last_edit_date = db.Column(db.DateTime)
    status = db.Column(db.String(5))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body, topic, tag, posted_date, last_edit_date, status, user_id):
        self.title = title
        self.body = body
        self.topic = topic
        self.tag = tag
        self.posted_date = posted_date
        self.last_edit_date = datetime.datetime.now()
        self.status = status
        self.user_id = user_id

    def url(self):
        return '/post/' + str(self.id)

    def preview(self, nlines=10):
        return '\n'.join(self.body.split('\n')[:nlines])

    def __repr__(self):
        return 'title {0}'.format(self.title)


from flask import render_template, Blueprint, redirect, request, url_for

from app.backend import db
from app.backend.models import Post, User

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def homepage():
    
    page = request.args.get('page', 1, type=int)
    POSTS_PER_PAGE = 3

    #all_posted = User.query.join(Post, User.id == Post.user_id).add_columns(Post.id, Post.title, Post.body, Post.last_edit_date, Post.tag, Post.topic, Post.status, User.username).filter(Post.status == 'Post').order_by(Post.last_edit_date.desc()).paginate(1, 3, False).items

    # all_posted = User.query.join(Post, User.id == Post.user_id).add_columns(Post.id, Post.title, Post.body, Post.last_edit_date, Post.tag, Post.topic, Post.status, User.username).filter(Post.status == 'Post').order_by(Post.last_edit_date.desc()).all()

    all_posted = User.query.join(Post, User.id == Post.user_id).add_columns(Post.id, Post.title, Post.body, Post.last_edit_date, Post.tag, Post.topic, Post.status, User.username).filter(Post.status == 'Post').order_by(Post.last_edit_date.desc()).paginate(page, POSTS_PER_PAGE, False)

    next_url = url_for('home.homepage', page=all_posted.next_num)

    if all_posted.has_next:
        True
    else: 
        None

    prev_url = url_for('home.homepage', page=all_posted.prev_num)

    if all_posted.has_prev:
        True
    else:
        None
    
    return render_template("home/index.html", all_posted=all_posted.items, next_url=next_url, prev_url=prev_url)


@home_blueprint.route('/about')
def about():
    return render_template("home/about.html")

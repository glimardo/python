from flask import render_template, Blueprint, url_for, redirect, flash, request, abort, session

from flask_login import login_required, current_user

from app.backend import db
from app.backend.models import Post, User

topic_blueprint = Blueprint('topics', __name__)


@topic_blueprint.route('/topic/<string:topic>', methods=['GET', 'POST'])
#@login_required
def show_topic(topic):
    find_posts_topic = User.query.join(Post, User.id == Post.user_id).add_columns(Post.id, Post.title, Post.body, Post.last_edit_date, Post.tag, Post.topic, Post.status, User.username).filter(User.id == Post.user_id).filter(Post.status == 'Post', Post.topic == topic).order_by(Post.last_edit_date).all()

    return render_template('topic/posts_topic.html', find_posts_topic=find_posts_topic, topic=topic)

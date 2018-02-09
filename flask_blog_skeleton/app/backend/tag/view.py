from flask import render_template, Blueprint, url_for, redirect, flash, request, abort, session

from flask_login import login_required, current_user

from app.backend import db
from app.backend.models import Post, User

tag_blueprint = Blueprint('tag', __name__)


@tag_blueprint.route('/tag/<string:tag>', methods=['GET', 'POST'])
#@login_required
def show_tag(tag):
    tag_filter = "%" + tag + "%"
    print(tag_filter)
    find_posts_tag = User.query.join(Post, User.id == Post.user_id).add_columns(Post.id, Post.title, Post.body, Post.last_edit_date, Post.tag, Post.topic, Post.status, User.username).filter(Post.status == 'Post', Post. tag.like(tag_filter)).order_by(Post.last_edit_date).all()
    return render_template('tag/posts_tag.html', find_posts_tag=find_posts_tag, tag=tag)

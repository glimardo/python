import datetime
from flask import render_template, Blueprint, url_for, redirect, flash, request, abort, session

from flask_login import login_required, current_user

from app.backend import db
from app.backend.models import Post, User


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin/posts/', methods=['GET', 'POST'])
@login_required
def admin_posts():
    all_posts = Post.query.all()
    all_published_posts = Post.query.filter(Post.status == 'Post').order_by(Post.last_edit_date).all()
    all_draft_posts = Post.query.filter(Post.status == 'Draft').order_by(Post.last_edit_date).all()

    if current_user.admin:
        return render_template('admin/all_posts.html', all_posts=all_posts, all_published_posts=all_published_posts, all_draft_posts=all_draft_posts)
    else:
        flash('You can\'t view this page!', 'danger')
        return redirect(url_for('home.homepage'))


@admin_blueprint.route('/admin/users', methods=['GET', 'POST'])
@login_required
def admin_users():
    all_users = User.query.all()
    all_users_not_admin = User.query.filter(User.admin == 0).all()
    all_admins = User.query.filter(User.admin == 1).all()
    all_users_post = db.session.query(User, Post).filter(User.id == Post.user_id).all()

    if current_user.admin:
        return render_template('admin/all_users.html', all_users=all_users, all_admins=all_admins, all_users_not_admin=all_users_not_admin, all_users_post=all_users_post)
    else:
        flash('You can\'t view this page!', 'danger')
        return redirect(url_for('home.homepage'))


@admin_blueprint.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():

    if current_user.admin:
        return render_template('admin/dashboard.html')
    else:
        flash('You can\'t view this page!', 'danger')
        return redirect(url_for('home.homepage'))

import datetime
from flask import render_template, Blueprint, url_for, redirect, flash, request, abort, session

from flask_login import login_required, current_user

from functools import wraps

from app.backend import db
from app.backend.models import Post
from .forms import AddPostForm

post_blueprint = Blueprint('blog_posts', __name__)


@post_blueprint.route('/post/add/', methods=['GET', 'POST'])
@login_required
def new_post():
    error = None
    form = AddPostForm(request.form)
    if request.method == 'POST':

        if form.validate_on_submit():
            new_post = Post(
                            form.post_title.data,
                            form.post_body.data,
                            form.post_topic.data,
                            form.post_tag.data,
                            datetime.datetime.utcnow(),
                            datetime.datetime.utcnow(),
                            form.post_status.data,
                            session['user_id']
                            )
            db.session.add(new_post)
            db.session.commit()
            flash('You have successfully added a post!', 'success')
    
        return render_template('post/add.html', form=form, error=error)

    return render_template('post/add.html', form=form, error=error)


@post_blueprint.route('/post/all')
def show_all_posts():
    posts = Post.query.all()
    return render_template('post/posts.html', posts=posts)


@post_blueprint.route('/post/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post/post.html', post=post)


@post_blueprint.route('/post/all/<int:user_id>')
@login_required
def show_all_user_posts(user_id):
    posts = Post.query.filter(Post.user_id == user_id).order_by(Post.last_edit_date).all()
    posts_published = Post.query.filter(Post.user_id == user_id, Post.status == 'Post').order_by(Post.last_edit_date).all()
    posts_draft = Post.query.filter(Post.user_id == user_id, Post.status == 'Draft').order_by(Post.last_edit_date).all()

    return render_template('post/user_posts.html', posts=posts, posts_published=posts_published, posts_draft=posts_draft)


@post_blueprint.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    
    if current_user.id == post.user_id or current_user.admin == True:
        db.session.delete(post)
        db.session.commit()
        flash('The post was deleted. Why not add a new one?', 'success')
        return redirect(url_for('blog_posts.new_post'))
    else:
        flash('You can only delete post that belong to you!', 'danger')
        return redirect(url_for('blog_posts.show_all_user_posts',  user_id=current_user.id))


@post_blueprint.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):

    post = Post.query.get_or_404(id)
    form = AddPostForm(obj=post)

    if current_user.id == post.user_id or current_user.admin == True:
    
        if form.validate_on_submit():
            post.title = form.post_title.data
            post.body = form.post_body.data
            post.topic = form.post_topic.data
            post.tag = form.post_tag.data
            post.status = form.post_status.data
            post.last_edit_date = datetime.datetime.utcnow()

            db.session.add(post)
            db.session.commit()
            flash('You have successfully updated a post!', 'success')

            return redirect(url_for('blog_posts.show_post', id=id))

        form.post_title.data = post.title
        form.post_body.data = post.body
        form.post_topic.data = post.topic
        form.post_tag.data = post.tag
        form.post_status.data = post.status
        return render_template('post/edit.html', id=id, form=form)
    
    else:
        flash('You can only edit post that belong to you!', 'danger')
        return redirect(url_for('blog_posts.show_all_user_posts',  user_id=current_user.id))  


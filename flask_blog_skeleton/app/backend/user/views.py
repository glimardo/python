from flask import render_template, Blueprint, url_for, redirect, flash, request, abort, session, current_app
from flask_login import login_required, login_user, logout_user, current_user
from functools import wraps
from sqlalchemy.exc import IntegrityError

from app.backend import db, bcrypt
from app.backend.models import User
from .forms import LoginForm, RegistrationForm

import datetime

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    error = None
    form = RegistrationForm(request.form)

    if request.method == 'POST':

        if form.validate_on_submit():
            user = User(
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        username=form.last_name.data,
                        email=form.email.data,
                        password=form.password.data
                       )
            try:
                db.session.add(user)
                db.session.commit()
                flash('You have successfully registered! You may now login', 'success')

                return redirect(url_for('user.login'))
            except IntegrityError:
                error = 'That username and/or email already exist.'
                return render_template('user/register.html', form=form, error=error)

        else:
            print("Sono entrato nell'else e quindi Failed!")
    else:
        print('login form error: someone use a \'GET\' method instead \'POST\'')

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm(request.form)

    if request.method == 'POST':

        if form.validate_on_submit():
        # check whether user exists in the database and whether
        # the password entered matches the password in the database

            user = User.query.filter_by(username=form.username.data).first()
          
            if user and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                current_app.logger. debug('User login: ' + str(current_user.username) + " at " + datetime.datetime.utcnow().strftime('%d-%m-%y %H:%M'))
                flash('You are logged in. Welcome ' + str(user.username) + '!', 'success')
                print(str(user.username) + "has logged in!")
                #return render_template("home/index.html")
                if request.args.get("next") is None:
                    return redirect(url_for('home.homepage'))
                else:
                    return redirect(request.args.get("next"))
            else:
                flash('Invalid username or password', 'danger')
                print('Invalid username or password')
                return render_template('user/login.html', form=form)
    
    else:
        print('login form error: someone use a \'GET\' method instead \'POST\'')

    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    current_app.logger.debug('User logout: ' + str(current_user.username) + " at " + datetime.datetime.utcnow().strftime('%d-%m-%y %H:%M'))
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('home.homepage'))


@user_blueprint.route('/user/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def show_user_profile(id):
    
    user = User.query.get_or_404(id)
    form = RegistrationForm(obj=user)

    if current_user.id == user.id or current_user.admin == True:

        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.username = form.username.data
            
            try:
                db.session.add(user)
                db.session.commit()

                flash('You have successfully updated your profile!', 'success')
            except IntegrityError as e:
                current_app.logger. debug(e)
            
            #return render_template('user/user_profile.html', user=user, form=form)   
            return redirect(url_for('home.homepage')) 

        elif request.method == 'GET':
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.username.data = user.username

        return render_template('user/user_profile.html', id=id, form=form)
        
    else:
        flash('You cant\'t view this profle. Bye!', 'danger')
        return redirect(url_for('home.homepage'))

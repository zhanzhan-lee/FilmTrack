# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_login import login_required, current_user
from app.models import User
from app import db
from app.forms import LoginForm, RegisterForm


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.intro'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'warning')
        else:
            hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_user = User(
                username=form.username.data,
                password=hashed_pw
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Flask-Login to logout
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))




@auth.route('/profile')
@login_required
def profile():
    return render_template('_modals/profile.html', user=current_user)

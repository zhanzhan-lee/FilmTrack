
# app/routes.py
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

# View function for the home page
def home():
    return render_template('index.html', title="Home Page", message="Welcome to the Home Page!")

# View function for the about page
def about():
    return render_template('about.html', title="About Us", message="Learn more about us here.")

# View function for the contact page
def contact():
    return render_template('contact.html', title="Contact Us", message="Get in touch with us.")


# View function for login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['username'] = user.username # Store username in session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    return render_template('login.html', title="Login")

# View function for register
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'warning')
        else:
            hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title="Register")

# View function for logout
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
  
# View function for the stats page
def stats():
    return render_template('stats.html', title="Stats", message="Visualise your shooting habits.")


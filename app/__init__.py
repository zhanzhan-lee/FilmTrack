# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initializing a SQLAlchemy Instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuring the Flask Application
    app.config['SECRET_KEY'] = 'dev'  # temporary
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)



    # Importing routes (view functions) 

    from .routes import home, about, contact, login, register, logout, stats, share
    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/about', 'about', about)
    app.add_url_rule('/contact', 'contact', contact)
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/stats', 'stats', stats)
    app.add_url_rule('/share', 'share', share)


    
    with app.app_context():
        db.create_all()

   
    return app

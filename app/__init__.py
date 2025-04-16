# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuring the Flask Application
    app.config['SECRET_KEY'] = 'dev'  # temporary


    # Importing routes (view functions) 
    from .routes import home, about, contact, stats
    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/about', 'about', about)
    app.add_url_rule('/contact', 'contact', contact)
    app.add_url_rule('/stats', 'stats', stats)

    return app

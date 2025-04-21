from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', title="Home Page", message="Welcome to the Home Page!")

@main.route('/about')
def about():
    return render_template('about.html', title="About Us", message="Learn more about us here.")

@main.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us", message="Get in touch with us.")


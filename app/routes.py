# app/routes.py
from flask import render_template

# View function for the home page
def home():
    return render_template('index.html', title="Home Page", message="Welcome to the Home Page!")

# View function for the about page
def about():
    return render_template('about.html', title="About Us", message="Learn more about us here.")

# View function for the contact page
def contact():
    return render_template('contact.html', title="Contact Us", message="Get in touch with us.")

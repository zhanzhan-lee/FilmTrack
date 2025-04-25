from flask import Blueprint, render_template

share = Blueprint('share', __name__)

@share.route('/share')
def share_page():
    return render_template('share.html', title="Share", message="Share.")

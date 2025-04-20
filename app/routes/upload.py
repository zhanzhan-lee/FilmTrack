from flask import Blueprint, render_template

upload = Blueprint('upload', __name__)

@upload.route('/upload')
def upload_view():
    return render_template('upload.html', title="Upload", message="Upload your shooting.")

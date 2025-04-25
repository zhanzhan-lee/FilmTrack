from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from app import db
from app.forms import CameraForm
from app.models import Camera

upload = Blueprint('upload', __name__)

@upload.route('/upload_camera', methods=['GET', 'POST'])
@login_required
def upload_camera():
    form = CameraForm()
    if request.method == 'GET':
        return render_template('upload_camera.html', form=form)

    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            folder = os.path.join('static/uploads/cameras')
            os.makedirs(folder, exist_ok=True)
            form.image.data.save(os.path.join(folder, filename))

        camera = Camera(
            name=form.name.data,
            brand=form.brand.data,
            type=form.type.data,
            format=form.format.data,
            is_public=form.is_public.data,
            image_path=filename,
            user_id=current_user.id
        )
        db.session.add(camera)
        db.session.commit()
        return jsonify({'message': 'Camera uploaded successfully'})

    return jsonify({'message': 'Form validation failed'}), 400

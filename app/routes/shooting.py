# app/routes/shooting.py

from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from app.models import Roll, Film, Photo, Camera, Lens
from app.forms import RollForm
from app import db
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


shooting = Blueprint('shooting', __name__)

# --------------------------------------------
# 页面渲染：shooting 页面（初始加载）
# Page rendering: shooting page (initial load)
# --------------------------------------------
@shooting.route('/shooting')
@login_required
def shooting_page():
    # 后续这里可以 preload 但我们预计 AJAX 加载即可
    # We can preload it later, but we expect AJAX loading to be enough.
    return render_template(
        'shooting.html',
        roll_form=RollForm()  # 提供 modal 表单(Provide modal form)
    )

# --------------------------------------------
# 数据接口：返回当前用户所有 Roll（AJAX）
# Data interface: Return all Rolls of the current user (AJAX)
# --------------------------------------------
@shooting.route('/shooting/data/rolls')
@login_required
def get_roll_data():
    rolls = Roll.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': roll.id,
            'roll_name': roll.roll_name,
            'film_id': roll.film_id,
            'film_name': f"{roll.film.brand} {roll.film.name}" if roll.film else None,
            'film_image': roll.film.image_path if roll.film else None,  # 
            'start_date': roll.start_date.strftime('%Y-%m-%d') if roll.start_date else None,
            'end_date': roll.end_date.strftime('%Y-%m-%d') if roll.end_date else None,
            'status': roll.status,
            'notes': roll.notes or ''
        }
        for roll in rolls
    ])


# -----------------------------
# 上传新 Roll（POST）
# Upload a new Roll (POST)
# -----------------------------
@shooting.route('/shooting/upload_roll', methods=['POST'])
@login_required
def upload_roll():
    form = RollForm()
    form.film_id.choices = [(f.id, f"{f.brand} {f.name}") for f in Film.query.filter_by(user_id=current_user.id)]
    
    if form.validate_on_submit():
        new_roll = Roll(
            user_id=current_user.id,
            film_id=form.film_id.data,
            roll_name=form.roll_name.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status='in use',
            notes=form.notes.data
        )
        db.session.add(new_roll)
        db.session.commit()
        return jsonify({'message': 'success'}), 200

    return jsonify({'message': 'form invalid', 'errors': form.errors}), 400


# -----------------------------
# 编辑 Roll（POST）
# Edit Roll (POST)
# -----------------------------
@shooting.route('/shooting/edit_roll/<int:id>', methods=['POST'])
@login_required
def edit_roll(id):
    roll = Roll.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = RollForm()
    form.film_id.choices = [(f.id, f"{f.brand} {f.name}") for f in Film.query.filter_by(user_id=current_user.id)]

    if form.validate_on_submit():
        roll.film_id = form.film_id.data
        roll.roll_name = form.roll_name.data
        roll.start_date = form.start_date.data
        roll.end_date = form.end_date.data
        roll.status = form.status.data
        roll.notes = form.notes.data
        db.session.commit()
        return jsonify({'message': 'updated'}), 200

    return jsonify({'message': 'form invalid', 'errors': form.errors}), 400


# -----------------------------
# 删除 Roll（DELETE）
# Delete Roll (DELETE)
# -----------------------------
@shooting.route('/shooting/delete_roll/<int:id>', methods=['DELETE'])
@login_required
def delete_roll(id):
    roll = Roll.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(roll)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200


# -----------------------------
# 完成拍摄（POST）
# finish shooting (POST)
# -----------------------------


@shooting.route('/shooting/finish_roll/<int:roll_id>', methods=['POST'])
@login_required
def finish_roll(roll_id):
    roll = Roll.query.get_or_404(roll_id)
    if roll.user_id != current_user.id:
        return jsonify({'success': False}), 403

    from datetime import datetime
    roll.status = 'finished'
    end_date_str = request.form.get('end_date')
    if end_date_str:
        roll.end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        roll.end_date = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'success': True,
        'roll': {
            'id': roll.id,
            'roll_name': roll.roll_name,
            'film_name': f"{roll.film.brand} {roll.film.name}" if roll.film else '',
            'film_image': roll.film.image_path if roll.film else '',
            'start_date': roll.start_date.strftime('%Y-%m-%d') if roll.start_date else '',
            'end_date': roll.end_date.strftime('%Y-%m-%d') if roll.end_date else '',
            'status': roll.status
        }
    })


# -----------------------------
# Frame upload（POST）
# ------------------------------

@shooting.route('/shooting/data/photos')
@login_required
def get_photos():
    roll_id = request.args.get('roll_id', type=int)
    if not roll_id:
        return jsonify([])

    photos = Photo.query.filter_by(roll_id=roll_id, user_id=current_user.id).order_by(Photo.id).all()
    return jsonify([
        {
            'id': p.id,
            'image_path': p.image_path,
            'frame_number': p.frame_number,
            'shot_date': p.shot_date.strftime('%Y-%m-%d') if p.shot_date else '',
            'shutter_speed': p.shutter_speed,
            'aperture': p.aperture,
            'iso': p.iso,
            'location': p.location,
            'camera_id': p.camera_id,
            'lens_id': p.lens_id
        }
        for p in photos
    ])


@shooting.route('/shooting/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    image = request.files.get('image')
    if not image:
        return jsonify({'success': False, 'error': 'No image'}), 400

    filename = secure_filename(image.filename)
    save_dir = os.path.join(current_app.root_path, 'static/uploads/photos')
    os.makedirs(save_dir, exist_ok=True)
    image.save(os.path.join(save_dir, filename))

    # 解析字段
    roll_id = request.form.get('roll_id', type=int)
    if not roll_id:
        return jsonify({'success': False, 'error': 'Missing roll ID'}), 400

    #  自动查出 film_id
    roll = Roll.query.filter_by(id=roll_id, user_id=current_user.id).first()
    if not roll:
        return jsonify({'success': False, 'error': 'Invalid roll ID'}), 400
    film_id = roll.film_id  # ✅ 从 roll 中提取 film_id
    shot_date = request.form.get('shot_date')
    shutter_speed = request.form.get('shutter_speed')
    aperture = request.form.get('aperture')
    iso = request.form.get('iso')
    frame_number = request.form.get('frame_number')
    location = request.form.get('location')
    camera_id = request.form.get('camera_id', type=int)
    lens_id = request.form.get('lens_id', type=int)
    


    # date format check
    try:
        shot_date = datetime.strptime(shot_date, '%Y-%m-%d') if shot_date else None
    except ValueError:
        shot_date = None

    photo = Photo(
        user_id=current_user.id,
        image_path=filename,
        roll_id=roll_id,
        shot_date=shot_date,
        shutter_speed=shutter_speed,
        aperture=aperture,
        iso=iso,
        frame_number=frame_number,
        location=location,
        camera_id=camera_id,
        lens_id=lens_id,
        film_id=film_id
    )

    db.session.add(photo)
    db.session.commit()

    return jsonify({'success': True})


@shooting.route('/gear/data/cameras')
@login_required
def get_cameras():
    cameras = Camera.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': cam.id,
        'brand': cam.brand,
        'model': cam.model
    } for cam in cameras])

@shooting.route('/gear/data/lenses')
@login_required
def get_lenses():
    lenses = Lens.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': lens.id,
        'brand': lens.brand,
        'model': lens.model
    } for lens in lenses])


# edit photo
@shooting.route('/shooting/edit_photo/<int:id>', methods=['POST'])
@login_required
def edit_photo(id):
    photo = Photo.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    photo.shutter_speed = request.form.get('shutter_speed')
    photo.aperture = request.form.get('aperture')
    photo.iso = request.form.get('iso')
    photo.frame_number = request.form.get('frame_number')
    photo.location = request.form.get('location')

    photo.camera_id = request.form.get('camera_id', type=int)
    photo.lens_id = request.form.get('lens_id', type=int)

    shot_date = request.form.get('shot_date')
    if shot_date:
        try:
            photo.shot_date = datetime.strptime(shot_date, '%Y-%m-%d')
        except ValueError:
            pass

    db.session.commit()
    return jsonify({'success': True})

# delete photo
@shooting.route('/shooting/delete_photo/<int:id>', methods=['POST'])
@login_required
def delete_photo(id):
    photo = Photo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(photo)
    db.session.commit()
    return jsonify({'success': True})

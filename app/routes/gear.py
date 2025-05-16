# app/routes/gear.py
from flask import Blueprint, render_template
from flask import current_app
from flask_login import login_required, current_user
from app.models import Camera, Lens, Film
from app.forms import CameraForm, LensForm, FilmForm
from flask import jsonify
from flask import request
from werkzeug.utils import secure_filename
import os
from app import db
from sqlalchemy.exc import IntegrityError






gear = Blueprint('gear', __name__)

@gear.route('/gear')
@login_required
def gear_page():
    cameras = Camera.query.filter_by(user_id=current_user.id).all()
    lenses = Lens.query.filter_by(user_id=current_user.id).all()
    films = Film.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'gear.html', 
        cameras=cameras, 
        lenses=lenses,
        films=films,
        camera_form=CameraForm(),
        lens_form=LensForm(),
        film_form=FilmForm()
    )




@gear.route('/gear/data/cameras')
@login_required
def get_camera_data():
    cameras = Camera.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': cam.id,
            'name': cam.name,
            'brand': cam.brand,
            'type': cam.type,
            'format': cam.format,
            'image': cam.image_path 
        }
        for cam in cameras
    ])


@gear.route('/gear/data/lenses')
@login_required
def get_lens_data():
    lenses = Lens.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': lens.id,
            'name': lens.name,
            'brand': lens.brand,
            'mount_type': lens.mount_type,
            'image': lens.image_path 
        }
        for lens in lenses
    ])


@gear.route('/gear/data/films')
@login_required
def get_film_data():
    films = Film.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': film.id,
            'name': film.name,
            'brand': film.brand,
            'iso': film.iso,
            'format': film.format,
            'image': film.image_path
        }
        for film in films
    ])


# _____________________________________________________________________
# ADD NEW GEAR

@gear.route('/gear/upload_camera', methods=['POST'])
@login_required
def upload_camera():
    form = CameraForm()
    if form.validate_on_submit():
        
        image_file = form.image.data
        image_path = None
        if image_file:
            filename = secure_filename(image_file.filename)
            save_folder = os.path.join(current_app.static_folder, 'uploads', 'cameras')
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, filename)
            image_file.save(save_path)
            image_path = f'{filename}'  

     
        new_camera = Camera(
            name=form.name.data,
            brand=form.brand.data,
            type=form.type.data,
            format=form.format.data,
            image_path=image_path,
            is_public=form.is_public.data,
            user_id=current_user.id
        )
        db.session.add(new_camera)
        db.session.commit()

        return jsonify({'message': 'success'}), 200

    return jsonify({'message': 'form invalid'}), 400


@gear.route('/gear/upload_lens', methods=['POST'])
@login_required
def upload_lens():
    form = LensForm()
    if form.validate_on_submit():
        image_file = form.image.data
        image_path = None
        if image_file:
            filename = secure_filename(image_file.filename)
            save_folder = os.path.join(current_app.static_folder, 'uploads', 'lenses')
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, filename)
            image_file.save(save_path)
            image_path = f'{filename}'

        new_lens = Lens(
            name=form.name.data,
            brand=form.brand.data,
            mount_type=form.mount_type.data,
            image_path=image_path,
            is_public=form.is_public.data,
            user_id=current_user.id
        )
        db.session.add(new_lens)
        db.session.commit()
        return jsonify({'message': 'success'}), 200

    return jsonify({'message': 'form invalid'}), 400

@gear.route('/gear/upload_film', methods=['POST'])
@login_required
def upload_film():
    form = FilmForm()
    if form.validate_on_submit():
        image_file = form.image.data
        image_path = None
        if image_file:
            filename = secure_filename(image_file.filename)
            save_folder = os.path.join(current_app.static_folder, 'uploads', 'films')
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, filename)
            image_file.save(save_path)
            image_path = f'{filename}'

        new_film = Film(
            name=form.name.data,
            brand=form.brand.data,
            iso=form.iso.data,
            format=form.format.data,
            image_path=image_path,
            is_public=form.is_public.data,
            user_id=current_user.id
        )
        db.session.add(new_film)
        db.session.commit()
        return jsonify({'message': 'success'}), 200

    return jsonify({'message': 'form invalid'}), 400

# _____________________________________________________________________
# EDIT GEAR
#________
# Camera
@gear.route('/gear/edit_camera/<int:id>', methods=['POST'])
@login_required
def edit_camera(id):
    camera = Camera.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = CameraForm()

    # print(" Received form data:", form.data)
    # print(" Form errors:", form.errors)

    if form.validate_on_submit():
        camera.name = form.name.data
        camera.brand = form.brand.data
        camera.type = form.type.data
        camera.format = form.format.data
        camera.is_public = form.is_public.data

        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            folder = os.path.join(current_app.static_folder, 'uploads', 'cameras')
            os.makedirs(folder, exist_ok=True)
            save_path = os.path.join(folder, filename)
            image_file.save(save_path)
            camera.image_path = f'{filename}'

        db.session.commit()
        return jsonify({'message': 'updated'}), 200

    return jsonify({'message': 'form invalid'}), 400

@gear.route('/gear/delete_camera/<int:id>', methods=['DELETE'])
@login_required
def delete_camera(id):
    camera = Camera.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    try:
        db.session.delete(camera)
        db.session.commit()
        return jsonify({'message': 'deleted'}), 200

    except IntegrityError:
        db.session.rollback()  # Roll back the transaction to prevent the session from being locked
        return jsonify({
            'message': '❗ Unable to delete: This camera is linked to one or more photos.'
        }), 400
    

#________
# Lens
@gear.route('/gear/edit_lens/<int:id>', methods=['POST'])
@login_required
def edit_lens(id):
    lens = Lens.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = LensForm()

    if form.validate_on_submit():
        lens.name = form.name.data
        lens.brand = form.brand.data
        lens.mount_type = form.mount_type.data
        lens.is_public = form.is_public.data

        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            folder = os.path.join(current_app.static_folder, 'uploads', 'lenses')
            os.makedirs(folder, exist_ok=True)
            image_file.save(os.path.join(folder, filename))
            lens.image_path = f'{filename}'

        db.session.commit()
        return jsonify({'message': 'updated'}), 200

    return jsonify({'message': 'form invalid'}), 400


@gear.route('/gear/delete_lens/<int:id>', methods=['DELETE'])
@login_required
def delete_lens(id):
    lens = Lens.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    try:
        db.session.delete(lens)
        db.session.commit()
        return jsonify({'message': 'deleted'}), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': '❗ This lens is still associated with photos.'}), 400

#________
# Film
@gear.route('/gear/edit_film/<int:id>', methods=['POST'])
@login_required
def edit_film(id):
    film = Film.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = FilmForm()

    if form.validate_on_submit():
        film.name = form.name.data
        film.brand = form.brand.data
        film.iso = form.iso.data
        film.format = form.format.data
        film.is_public = form.is_public.data

        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            folder = os.path.join(current_app.static_folder, 'uploads', 'films')
            os.makedirs(folder, exist_ok=True)
            image_file.save(os.path.join(folder, filename))
            film.image_path = f'{filename}'

        db.session.commit()
        return jsonify({'message': 'updated'}), 200

    return jsonify({'message': 'form invalid'}), 400


@gear.route('/gear/delete_film/<int:id>', methods=['DELETE'])
@login_required
def delete_film(id):
    film = Film.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    try:
        db.session.delete(film)
        db.session.commit()
        return jsonify({'message': 'deleted'}), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': '❗ This film is still associated with photos.'}), 400

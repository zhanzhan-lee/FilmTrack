# app/routes/gear.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Camera, Lens, Film
from app.forms import CameraForm, LensForm, FilmForm
from flask import jsonify

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
            'name': lens.name,
            'brand': lens.brand,
            'mount_type': lens.mount_type,
            'image': lens.image_path  # 注意：不要添加 fallback 路径
        }
        for lens in lenses
    ])


@gear.route('/gear/data/films')
@login_required
def get_film_data():
    films = Film.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'name': film.name,
            'brand': film.brand,
            'iso': film.iso,
            'format': film.format,
            'image': film.image_path
        }
        for film in films
    ])

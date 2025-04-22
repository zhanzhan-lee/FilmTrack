# app/routes/gear.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Camera, Lens, Film

gear = Blueprint('gear', __name__)

@gear.route('/gear')
@login_required
def gear_page():
    cameras = Camera.query.filter_by(user_id=current_user.id).all()
    lenses = Lens.query.filter_by(user_id=current_user.id).all()
    films = Film.query.filter_by(user_id=current_user.id).all()
    return render_template('gear.html', cameras=cameras, lenses=lenses, films=films)

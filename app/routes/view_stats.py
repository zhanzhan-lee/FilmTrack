from flask import Blueprint, render_template, jsonify
from app.models import Share, User, Photo, Film, Camera, Lens
from flask_login import current_user, login_required
from sqlalchemy import func

view_stats = Blueprint('view_stats', __name__)

@view_stats.route('/view_stats')
@login_required
def view_stats_page():
    # Get all shares where the current user is the recipient
    shares = Share.query.filter_by(to_user_id=current_user.id).all()
    print(shares)
    return render_template('view-stats.html', shares=shares)

@view_stats.route('/api/shared_stats/<int:share_id>')
@login_required
def get_shared_stats(share_id):
    share = Share.query.get_or_404(share_id)
    
    # Verify the current user is the recipient
    if share.to_user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = {}
    
    # Exposure data (existing)
    if share.share_exposure:
        exposures = Photo.query.filter_by(user_id=share.from_user_id)\
            .with_entities(Photo.shutter_speed, func.count(Photo.id))\
            .group_by(Photo.shutter_speed).all()
        data['exposure'] = {
            'labels': [exp[0] for exp in exposures],
            'values': [exp[1] for exp in exposures]
        }

    # Aperture data (existing)
    if share.share_aperture:
        apertures = Photo.query.filter_by(user_id=share.from_user_id)\
            .with_entities(Photo.aperture, func.count(Photo.id))\
            .group_by(Photo.aperture).all()
        data['aperture'] = {
            'labels': [ap[0] for ap in apertures],
            'values': [ap[1] for ap in apertures]
        }

    # Favorite Film data
    if share.share_favorite_film:
        films = Photo.query\
            .filter_by(user_id=share.from_user_id)\
            .join(Film)\
            .with_entities(
                Film.name,
                Film.brand,
                func.count(Photo.id).label('count')
            )\
            .group_by(Film.name, Film.brand)\
            .order_by(func.count(Photo.id).desc())\
            .limit(5)\
            .all()
        data['favorite_film'] = {
            'labels': [f"{film[1]} {film[0]}" for film in films],
            'values': [film[2] for film in films]
        }

    # Gear preference data
    if share.share_gear:
        # Camera usage
        cameras = Photo.query\
            .filter_by(user_id=share.from_user_id)\
            .join(Camera)\
            .with_entities(
                Camera.name,
                func.count(Photo.id).label('count')
            )\
            .group_by(Camera.name)\
            .order_by(func.count(Photo.id).desc())\
            .all()
        data['cameras'] = {
            'labels': [cam[0] for cam in cameras],
            'values': [cam[1] for cam in cameras]
        }

        # Lens usage
        lenses = Photo.query\
            .filter_by(user_id=share.from_user_id)\
            .join(Lens)\
            .with_entities(
                Lens.name,
                func.count(Photo.id).label('count')
            )\
            .group_by(Lens.name)\
            .order_by(func.count(Photo.id).desc())\
            .all()
        data['lenses'] = {
            'labels': [lens[0] for lens in lenses],
            'values': [lens[1] for lens in lenses]
        }

    # Shoot time data
    if share.share_shoot_time:
        # Monthly trend using SQLite's strftime
        monthly = Photo.query\
            .filter_by(user_id=share.from_user_id)\
            .with_entities(
                func.strftime('%Y-%m', Photo.shot_date).label('month'),
                func.count(Photo.id)
            )\
            .group_by('month')\
            .order_by('month')\
            .all()
        data['monthly_trend'] = {
            'labels': [m[0] for m in monthly],
            'values': [m[1] for m in monthly]
        }

        # Time of day using SQLite's strftime
        hourly = Photo.query\
            .filter_by(user_id=share.from_user_id)\
            .with_entities(
                func.strftime('%H', Photo.shot_date).label('hour'),
                func.count(Photo.id)
            )\
            .group_by('hour')\
            .order_by('hour')\
            .all()
        data['time_of_day'] = {
            'labels': [f"{h[0]}:00" for h in hourly],
            'values': [h[1] for h in hourly]
        }

    return jsonify(data)

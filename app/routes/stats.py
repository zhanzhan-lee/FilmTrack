from flask import Blueprint, render_template, request, jsonify
from app.models import *
from sqlalchemy import func, extract
from flask_login import current_user, login_required
from datetime import datetime, timedelta

stats = Blueprint('stats', __name__)

@stats.route('/stats')
def stats_page():
    return render_template('stats.html', title="Stats", message="Visualise your shooting habits.")

@stats.route('/api/monthly-trend', methods=['GET'])
def get_monthly_trend():
    today = datetime.today()
    six_months_ago = today - timedelta(days=6 * 30)

    results = (
        Photo.query
        .with_entities(
            extract('month', Photo.shot_date).label('month'),
            func.count(Photo.id).label('photo_count')
        )
        .filter(Photo.shot_date >= six_months_ago)
        .filter(Photo.shot_date <= today)             # Filter for the last 6 months
        .filter(Photo.user_id == current_user.id)              # Filter by the current user's ID
        .group_by(extract('month', Photo.shot_date))           # Group by month
        .order_by(extract('month', Photo.shot_date))           # Order by month
        .all()
    )
    
    labels = []
    data = []

    # Map month numbers to month names
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    # Populate labels and data
    for month, photo_count in results:
        labels.append(month_names[month])  # Convert month number to name
        data.append(photo_count)

    # Fill in missing months with 0 photos
    for i in range(6):
        month = (today.month - i - 1) % 12 + 1  # Calculate the month number
        if month_names[month] not in labels:
            labels.insert(0, month_names[month])
            data.insert(0, 0)

    # Prepare the response
    monthly_data = {
        "labels": labels[-6:],  # Ensure only the last 6 months are included
        "data": data[-6:]       # Ensure only the last 6 months are included
    }

    return jsonify(monthly_data)

@stats.route('/api/aperture-distribution', methods=['GET'])
def get_aperture_distribution():
    # Query the database for the top 5 apertures used by the current user
    results = (
        Photo.query
        .with_entities(Photo.aperture, func.count(Photo.id).label('aperture_count'))
        .filter(Photo.user_id == current_user.id)  # Filter by the current user's ID
        .group_by(Photo.aperture)
        .order_by(func.count(Photo.id).desc())  # Order by count in descending order
        .limit(5)  # Limit to the top 5 apertures
        .all()
    )

    # Prepare the labels and data for the response
    labels = [result[0] for result in results]  # Aperture values
    data = [result[1] for result in results]   # Counts

    # Return the data as JSON
    return jsonify({"labels": labels, "data": data})

@stats.route('/api/shutter-speed-distribution', methods=['GET'])
def get_shutter_speed_distribution():
    # Query the database for the top 5 shutter speeds used by the current user
    results = (
        Photo.query
        .with_entities(Photo.shutter_speed, func.count(Photo.id).label('shutter_speed_count'))
        .filter(Photo.user_id == current_user.id)
        .group_by(Photo.shutter_speed)
        .order_by(func.count(Photo.id).desc())
        .limit(5)
        .all()
    )

    # Prepare the labels and data for the response
    labels = [result[0] for result in results]
    data = [result[1] for result in results]

    # Return the data as JSON
    return jsonify({"labels": labels, "data": data, "total": sum(data)})

@stats.route('/api/cameras-chart-preference', methods=['GET'])
def get_camera_preference():
    # Query the database for the top 3 most-used cameras by the current user
    results = (
        Photo.query
        .with_entities(Photo.camera_id, func.count(Photo.id).label('camera_count'))
        .filter(Photo.user_id == current_user.id)  # Filter by the current user's ID
        .group_by(Photo.camera_id)
        .order_by(func.count(Photo.id).desc())  # Order by count in descending order
        .limit(3)  # Limit to the top 3 cameras
        .all()
    )

    # Prepare the labels and data for the response
    labels = []
    data = []

    for camera_id, count in results:
        camera = Camera.query.get(camera_id)  # Fetch camera details
        if camera:
            labels.append(camera.name)  # Add camera name to labels
            data.append(count)          # Add photo count to data

    # Return the data as JSON
    return jsonify({"labels": labels, "data": data})

@stats.route('/api/lenses-chart-preference', methods=['GET'])
def get_lens_preference():
    results = (
        Photo.query
        .with_entities(Photo.lens_id, func.count(Photo.id).label('lens_count'))
        .filter(Photo.user_id == current_user.id) 
        .group_by(Photo.lens_id)
        .order_by(func.count(Photo.id).desc())
        .limit(3) 
        .all()
    )

    labels = []
    data = []

    for lens_id, count in results:
        lens = Lens.query.get(lens_id) 
        if lens:
            labels.append(lens.name) 
            data.append(count)

    # Return the data as JSON
    return jsonify({"labels": labels, "data": data})

@stats.route('/api/film-chart-preference', methods=['GET'])
def get_film_preference():
    results = (
        Photo.query
        .with_entities(Photo.film_id, func.count(Photo.id).label('film_count'))
        .filter(Photo.user_id == current_user.id) 
        .group_by(Photo.film_id)
        .order_by(func.count(Photo.id).desc())
        .limit(3) 
        .all()
    )

    labels = []
    data = []
    images = []

    for film_id, count in results:
        film = Film.query.get(film_id) 
        if film:
            labels.append(film.name) 
            data.append(count)
            images.append(film.image_path)

    # Return the data as JSON
    return jsonify({"labels": labels, "data": data, "images": images})

@stats.route('/api/top-locations', methods=['GET'])
def get_top_locations():
    # Query the database for the top 5 most shot-at locations by the current user
    results = (
        Photo.query
        .with_entities(Photo.location, func.count(Photo.id).label('location_count'))
        .filter(Photo.user_id == current_user.id)  # Filter by the current user's ID
        .group_by(Photo.location)
        .order_by(func.count(Photo.id).desc())  # Order by count in descending order
        .limit(5)  # Limit to the top 5 locations
        .all()
    )

    # Prepare the labels and data for the response
    labels = [result[0] for result in results if result[0]]  # Location names (exclude None)
    data = [result[1] for result in results]  # Counts

    # Return the data as JSON
    return jsonify({"labels": labels, "data": data, "total": sum(data)})
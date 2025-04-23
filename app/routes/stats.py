from flask import Blueprint, render_template, request, jsonify
from app.models import Photo, Film
from sqlalchemy import func, extract
from flask_login import current_user
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

@stats.route('/api/favourite-films', methods=['GET'])
def get_favourite_films():
    results = (
        Photo.query
        .with_entities(Photo.film_id, func.count(Photo.id).label('photo_count'))
        .filter(Photo.user_id == current_user.id)  # Filter by the current user's ID
        .group_by(Photo.film_id)
        .order_by(func.count(Photo.id).desc())
        .limit(3)
        .all()
    )

    # Get the film names for the top 3 films
    favourite_films = []
    for film_id, _ in results:
        film = Film.query.get(film_id)
        if film:
            favourite_films.append(film.name)

    return jsonify(favourite_films)
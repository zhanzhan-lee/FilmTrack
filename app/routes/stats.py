from flask import Blueprint, render_template, request, jsonify
from app.models import Photo
from sqlalchemy import func
from flask_login import current_user

stats = Blueprint('stats', __name__)

@stats.route('/stats')
def stats_page():
    return render_template('stats.html', title="Stats", message="Visualise your shooting habits.")

@stats.route('/api/user-photos', methods=['GET'])
def get_monthly_trend():
    # Query the database for monthly trend data
    data = Photo.query.with_entities(Photo.shot_date).all()
    
    # Example: Group data by month (you can customize this logic)
    monthly_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        "data": [20, 30, 25, 40, 35, 50, 60]  # Replace with actual data
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

    serialized_results = [{"film_id": film_id, "photo_count": photo_count} for film_id, photo_count in results]

    return jsonify(serialized_results)

    # Get the film names for the top 3 films
    top_films = []
    for film_id, _ in results:
        film = Film.query.get(film_id)
        if film:
            top_films.append(film.name)

    return jsonify(top_films)
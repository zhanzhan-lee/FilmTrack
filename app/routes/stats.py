from flask import Blueprint, render_template

stats = Blueprint('stats', __name__)

@stats.route('/stats')
def stats_page():
    return render_template('stats.html', title="Stats", message="Visualise your shooting habits.")

@stats.route('/api/monthly-trend', methods=['GET'])
def get_monthly_trend():
    # Query the database for monthly trend data
    data = Photo.query.with_entities(Photo.shot_date).all()
    
    # Example: Group data by month (you can customize this logic)
    monthly_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        "data": [20, 30, 25, 40, 35, 50, 60]  # Replace with actual data
    }
    
    return jsonify(monthly_data)
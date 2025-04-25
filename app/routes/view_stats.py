from flask import Blueprint, render_template

view_stats = Blueprint('view_stats', __name__)

@view_stats.route('/view_stats')
def view_stats_page():
    return render_template('view-stats.html', title="View Stats", message="See other user's activity!")

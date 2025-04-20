from flask import Blueprint, render_template

stats = Blueprint('stats', __name__)

@stats.route('/stats')
def stats_page():
    return render_template('stats.html', title="Stats", message="Visualise your shooting habits.")

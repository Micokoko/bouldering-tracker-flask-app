from flask import Blueprint, render_template
from bouldering_app.db import get_db

bp = Blueprint('leaderboards', __name__, url_prefix='/leaderboards')

@bp.route('/leaderboards')
def leaderboards():
    db = get_db()
    rankings = db.execute(
        """
        SELECT
            boulder.id AS boulder_id,
            boulder.name AS boulder_name,
            boulder.image AS boulder_image,
            COALESCE(user.username, 'No Attempts') AS climber,
            COALESCE(attempt.number_of_attempts, 0) AS number_of_attempts,
            RANK() OVER (
                PARTITION BY boulder.id
                ORDER BY COALESCE(attempt.number_of_attempts, 0) ASC, MIN(attempt.attempt_date) ASC
            ) AS rank
        FROM boulder
        LEFT JOIN attempt ON boulder.id = attempt.boulder_id AND attempt.status IN ('completed', 'flashed')
        LEFT JOIN user ON attempt.user_id = user.id
        WHERE boulder.difficulty >= 6
        GROUP BY boulder.id, user.username
        ORDER BY boulder.name, rank;
        """
    ).fetchall()
    

    boulder_rankings = {}
    for row in rankings:
        boulder_id = row['boulder_id']
        if boulder_id not in boulder_rankings:
            boulder_rankings[boulder_id] = {'name': row['boulder_name'],'image':row['boulder_image'], 'data': []}
        boulder_rankings[boulder_id]['data'].append({
            'climber': row['climber'],
            'number_of_attempts': row['number_of_attempts'],
            'rank': row['rank']
        })

    return render_template('climber/leaderboards.html', boulder_rankings=boulder_rankings)

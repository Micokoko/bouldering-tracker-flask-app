from flask import Blueprint, render_template
from bouldering_app.models import db, Boulder, Attempt, User
from sqlalchemy import func

bp = Blueprint('leaderboards', __name__, url_prefix='/leaderboards')

@bp.route('/leaderboards')
def leaderboards():
    rankings = db.session.query(
        Boulder.id.label('boulder_id'),
        Boulder.name.label('boulder_name'),
        Boulder.difficulty.label('boulder_difficulty'),
        Boulder.image.label('boulder_image'),
        func.coalesce(User.username, 'No Attempts').label('climber'),
        func.coalesce(Attempt.number_of_attempts, 0).label('number_of_attempts'),
        func.rank().over(
            partition_by=Boulder.id,
            order_by=[
                func.coalesce(Attempt.number_of_attempts, 0).asc(),
                func.min(Attempt.attempt_date).asc()
            ]
        ).label('rank')
    ).outerjoin(
        Attempt,
        (Boulder.id == Attempt.boulder_id) & (Attempt.status.in_(['completed', 'flashed']))
    ).outerjoin(
        User,
        Attempt.user_id == User.id
    ).filter(
        Boulder.difficulty >= 6
    ).group_by(
        Boulder.id, User.username
    ).order_by(
        Boulder.difficulty.desc(),  
        Boulder.name,  
        'rank' 
    ).all()


    boulder_rankings = {}
    for row in rankings:
        boulder_id = row.boulder_id
        if boulder_id not in boulder_rankings:
            boulder_rankings[boulder_id] = {
                'name': row.boulder_name,
                'difficulty': row.boulder_difficulty,
                'image': row.boulder_image,
                'data': []
            }
        boulder_rankings[boulder_id]['data'].append({
            'climber': row.climber,
            'number_of_attempts': row.number_of_attempts,
            'rank': row.rank
        })

    return render_template('climber/leaderboards.html', boulder_rankings=boulder_rankings)

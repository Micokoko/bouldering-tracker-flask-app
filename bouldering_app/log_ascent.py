from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from .auth import login_required
from datetime import datetime, date
from bouldering_app.models import db
from bouldering_app.models import Boulder, Attempt, User
from sqlalchemy import func


bp = Blueprint('log_ascent', __name__, url_prefix='/climber')

@bp.route('/<int:id>/log_ascent', methods=('GET', 'POST'))
@login_required
def log_ascent_user(id):
    boulder = Boulder.query.get(id)

    if boulder is None:
        flash('Boulder not found.')
        return redirect(url_for('climber.user_page'))

    attempt = Attempt.query.filter_by(user_id=g.user.id, boulder_id=id).first()

    rankings = db.session.query(
        User.username,
        func.count(Attempt.id).label('number_of_attempts')
    ).select_from(Attempt).join(User).filter(
        Attempt.boulder_id == id,
        Attempt.status.in_(['completed', 'flashed']),
        Boulder.difficulty >= 6
    ).group_by(User.username).order_by(
        func.count(Attempt.id).asc(),
        func.min(Attempt.attempt_date).asc()
    ).all()

    if request.method == 'POST':
        attempts_str = request.form.get('number_of_attempts')
        moves_completed_str = request.form.get('moves_completed')
        attempt_date_str = request.form.get('attempt_date')
        error = None

        try:
            number_of_attempts = int(attempts_str)
            moves_completed = int(moves_completed_str)
            attempt_date = datetime.strptime(attempt_date_str, '%Y-%m-%d').date()

            if attempt_date > datetime.today().date():
                flash('Attempt date cannot be future dated.', 'danger')
                return render_template('climber/log_ascent.html', boulder=boulder, attempt=attempt, rankings=rankings)

            if moves_completed > boulder.numberofmoves:
                flash('Moves completed cannot be greater than the total number of moves.', 'danger')
                return render_template('climber/log_ascent.html', boulder=boulder, attempt=attempt, rankings=rankings)

            if number_of_attempts == 1 and moves_completed == boulder.numberofmoves:
                status = 'flashed'
            elif moves_completed == boulder.numberofmoves:
                status = 'completed'
            else:
                status = 'incomplete'

            if attempt:
                attempt.number_of_attempts = number_of_attempts
                attempt.status = status
                attempt.attempt_date = attempt_date
                attempt.moves_completed = moves_completed
                attempt.difficulty = boulder.difficulty
                db.session.commit()
                flash('Ascent updated successfully.')
            else:
                new_attempt = Attempt(
                    number_of_attempts=number_of_attempts,
                    status=status,
                    attempt_date=attempt_date,
                    user_id=g.user.id,
                    boulder_id=boulder.id,
                    moves_completed=moves_completed,
                    difficulty=boulder.difficulty
                )
                db.session.add(new_attempt)
                db.session.commit()
                flash('Ascent logged successfully.')

            return redirect(url_for('auth.user_page'))

        except ValueError as ve:
            flash(f"Invalid input: {ve}", 'danger')
        except Exception as e:
            flash(f"Unexpected Error: {e}", 'danger')

    return render_template('climber/log_ascent.html', boulder=boulder, attempt=attempt, rankings=rankings)


@bp.route('/archive')
@login_required
def archive():
    user_id = g.user.id


    completed_flashed_boulders = db.session.query(Boulder).join(Attempt).filter(
        Attempt.user_id == user_id,
        Attempt.status.in_(['completed', 'flashed'])
    ).distinct().all()

    attempts = db.session.query(Attempt).filter(
        Attempt.user_id == user_id,
        Attempt.status.in_(['completed', 'flashed'])
    ).all()


    formatted_attempts = []
    for attempt in attempts:
        attempt_date = attempt.attempt_date
        formatted_attempt = attempt.__dict__.copy()  

        if isinstance(attempt_date, str):
            try:
                formatted_attempt['attempt_date'] = datetime.strptime(attempt_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                formatted_attempt['attempt_date'] = 'Invalid Date'
        elif isinstance(attempt_date, datetime):
            formatted_attempt['attempt_date'] = attempt_date.strftime('%Y-%m-%d')
        elif isinstance(attempt_date, date):
            formatted_attempt['attempt_date'] = attempt_date.strftime('%Y-%m-%d')
        else:
            formatted_attempt['attempt_date'] = 'N/A'

        formatted_attempts.append(formatted_attempt)

    return render_template(
        'climber/archive.html',
        archived_boulders=completed_flashed_boulders,
        attempts=formatted_attempts
    )



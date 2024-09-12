from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from bouldering_app.db import get_db
from .auth import login_required
from datetime import datetime, date


bp = Blueprint('log_ascent', __name__, url_prefix='/climber')

@bp.route('/<int:id>/log_ascent', methods=('GET', 'POST'))
@login_required
def log_ascent_user(id):
    db = get_db()
    boulder = db.execute('SELECT * FROM boulder WHERE id = ?', (id,)).fetchone()

    if boulder is None:
        flash('Boulder not found.')
        return redirect(url_for('climber.user_page'))

    attempt = db.execute(
        'SELECT * FROM attempt WHERE boulder_id = ? AND user_id = ?', (id, g.user['id'])
    ).fetchone()

    # Rank users based on number of attempts for completed and flashed boulders with difficulty >= 6
    rankings = db.execute(
        """
        SELECT user.username, attempt.number_of_attempts,
            RANK() OVER (
                PARTITION BY attempt.boulder_id
                ORDER BY attempt.number_of_attempts ASC, MIN(attempt.attempt_date) ASC
            ) AS rank
        FROM attempt
        JOIN user ON attempt.user_id = user.id
        JOIN boulder ON attempt.boulder_id = boulder.id
        WHERE boulder.difficulty >= 6
        AND attempt.boulder_id = ?
        AND attempt.status IN ('completed', 'flashed')
        GROUP BY user.username, attempt.number_of_attempts
        """, (id,)
    ).fetchall()

    if request.method == 'POST':
        attempts_str = request.form.get('number_of_attempts')
        moves_completed_str = request.form.get('moves_completed')
        attempt_date_str = request.form.get('attempt_date')
        error = None

        print(f"DEBUG: Attempts: {attempts_str}, Moves Completed: {moves_completed_str}, Attempt Date: {attempt_date_str}")

        try:
            number_of_attempts = int(attempts_str)
            moves_completed = int(moves_completed_str)
            attempt_date = datetime.strptime(attempt_date_str, '%Y-%m-%d').date()

            if moves_completed > boulder['numberofmoves']:
                flash('Moves completed cannot be greater than the total number of moves.', 'danger')
                return render_template('climber/log_ascent.html', boulder=boulder, attempt=attempt, rankings=rankings)

            # Determine the status based on the moves completed and number of attempts
            if number_of_attempts == 1 and moves_completed == boulder['numberofmoves']:
                status = 'flashed'
            elif moves_completed == boulder['numberofmoves']:
                status = 'completed'
            else:
                status = 'incomplete'

            print(f"DEBUG: Determined Status (for DB): {status}")

            # Update or insert the attempt
            if attempt:
                db.execute(
                    """
                    UPDATE attempt 
                    SET number_of_attempts = ?, status = ?, attempt_date = ?, moves_completed = ?, difficulty = ? 
                    WHERE id = ?
                    """,
                    (number_of_attempts, status, attempt_date, moves_completed, boulder['difficulty'], attempt['id'])
                )
                flash('Ascent updated successfully.')
            else:
                db.execute(
                    """
                    INSERT INTO attempt (number_of_attempts, status, attempt_date, user_id, boulder_id, moves_completed, difficulty) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (number_of_attempts, status, attempt_date, g.user['id'], boulder['id'], moves_completed, boulder['difficulty'])
                )
                flash('Ascent logged successfully.')

            db.commit()

            return redirect(url_for('auth.user_page'))

        except ValueError as ve:
            flash(f"Invalid input: {ve}", 'danger')
            print(f"DEBUG: ValueError: {ve}")
        except db.IntegrityError as db_error:
            flash(f"Database Error: {db_error}", 'danger')
            print(f"DEBUG: Database Error: {db_error}")
        except Exception as e:
            flash(f"Unexpected Error: {e}", 'danger')
            print(f"DEBUG: Unexpected Error: {e}")

    return render_template('climber/log_ascent.html', boulder=boulder, attempt=attempt, rankings=rankings)




@bp.route('/archive')
@login_required
def archive():
    db = get_db()
    user_id = g.user['id']

    # Query to get completed and flashed boulders
    completed_flashed_boulders = db.execute(
        '''
        SELECT boulder.* 
        FROM boulder 
        JOIN attempt ON boulder.id = attempt.boulder_id 
        WHERE attempt.user_id = ? AND attempt.status IN ('completed', 'flashed')
        ''',
        (user_id,)
    ).fetchall()

    # Query to get attempts for these boulders
    attempts = db.execute(
        '''
        SELECT * 
        FROM attempt 
        WHERE user_id = ? AND status IN ('completed', 'flashed')
        ''',
        (user_id,)
    ).fetchall()

    # Format attempts dates
    formatted_attempts = []
    for attempt in attempts:
        attempt_date = attempt['attempt_date']
        formatted_attempt = dict(attempt)

        if isinstance(attempt_date, str):
            try:
                # Convert string to datetime.date
                formatted_attempt['attempt_date'] = datetime.strptime(attempt_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                formatted_attempt['attempt_date'] = 'Invalid Date'
        elif isinstance(attempt_date, datetime):
            # Convert datetime to string
            formatted_attempt['attempt_date'] = attempt_date.strftime('%Y-%m-%d')
        elif isinstance(attempt_date, date):
            # Convert date to string
            formatted_attempt['attempt_date'] = attempt_date.strftime('%Y-%m-%d')
        else:
            formatted_attempt['attempt_date'] = 'N/A'  # Handle other unexpected data types

        formatted_attempts.append(formatted_attempt)

    return render_template(
        'climber/archive.html',
        archived_boulders=completed_flashed_boulders,
        attempts=formatted_attempts
    )




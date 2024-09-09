from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from bouldering_app.db import get_db
from .auth import login_required
from datetime import datetime

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
                return render_template('climber/log_ascent.html', boulder=boulder, attempt=attempt)


            if number_of_attempts == 1 and moves_completed == boulder['numberofmoves']:
                status = 'flashed'
            elif moves_completed == boulder['numberofmoves']:
                status = 'completed'
            else:
                status = 'incomplete'  
            
            print(f"DEBUG: Determined Status (for DB): {status}")


            if attempt:
                db.execute(
                    """
                    UPDATE attempt 
                    SET number_of_attempts = ?, status = ?, attempt_date = ?, moves_completed = ? 
                    WHERE id = ?
                    """,
                    (number_of_attempts, status, attempt_date, moves_completed, attempt['id'])
                )
                flash('Ascent updated successfully.')
            else:
                db.execute(
                    """
                    INSERT INTO attempt (number_of_attempts, status, attempt_date, user_id, boulder_id, moves_completed) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (number_of_attempts, status, attempt_date, g.user['id'], boulder['id'], moves_completed)
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

    return render_template('climber/log_ascent.html', boulder=boulder, attempt=attempt)

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
    
    attempt_id = request.args.get('attempt_id')
    attempt = db.execute('SELECT * FROM attempt WHERE id = ?', (attempt_id,)).fetchone() if attempt_id else None

    if request.method == 'POST':
        attempts_str = request.form.get('number_of_attempts')
        status = request.form.get('status')
        attempt_date_str = request.form.get('attempt_date')
        error = None

        print(f"DEBUG: Attempts: {attempts_str}, Status: {status}, Attempt Date: {attempt_date_str}")

        try:
            number_of_attempts = int(attempts_str)
            attempt_date = datetime.strptime(attempt_date_str, '%Y-%m-%d').date()

            if status not in ('incomplete', 'completed', 'flash'):
                raise ValueError("Invalid status value.")
            
            if attempt:
                db.execute(
                    "UPDATE attempt SET number_of_attempts = ?, status = ?, attempt_date = ? WHERE id = ?",
                    (number_of_attempts, status, attempt_date, attempt_id)
                )
            else:
                db.execute(
                    "INSERT INTO attempt (number_of_attempts, status, attempt_date, user_id, boulder_id) VALUES (?, ?, ?, ?, ?)",
                    (number_of_attempts, status, attempt_date, g.user['id'], boulder['id'])
                )
            
            db.commit()
            return redirect(url_for('auth.user_page'))
        except ValueError as ve:
            error = f"Invalid input: {ve}"
        except db.IntegrityError:
            error = "Unable to log the ascent. Please try again."
            
        if error:
            flash(error)

    return render_template('climber/log_ascent.html', boulder=boulder, attempt=attempt)

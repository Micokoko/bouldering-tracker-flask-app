from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from bouldering_app.db import get_db
from .auth import login_required
from datetime import datetime

bp = Blueprint('archive', __name__, url_prefix='/archive')

@bp.route('/<int:id>')
@login_required
def archive(id):
    user_id = g.user['id']
    db = get_db()
    boulder = db.execute('SELECT * FROM boulder WHERE id = ?', (id,)).fetchone()
    if boulder is None:
        flash('Boulder not found.')
        return redirect(url_for('index'))  # Redirect to an appropriate page

    attempts = db.execute(
        'SELECT * FROM attempt WHERE boulder_id = ? AND user_id = ?', (id, g.user['id'])
    ).fetchall()

    completed_boulders = []
    flashed_boulders = []

    # Categorize boulders based on status
    for attempt in attempts:
        if attempt.status == 'completed':
            completed_boulders.append(boulder)
        elif attempt.status == 'flashed':
            flashed_boulders.append(boulder)

    completed_boulders.sort(key=lambda b: b.difficulty, reverse=True)
    flashed_boulders.sort(key=lambda b: b.difficulty, reverse=True)

    return render_template('archive.html',
                        completed_boulders=completed_boulders,
                        flashed_boulders=flashed_boulders)

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from bouldering_app.db import get_db
from .auth import login_required
from datetime import datetime


bp = Blueprint('archive', __name__, url_prefix='/archive')

@bp.route('/archive')
@login_required
def archive():
    user_id = g.user['id']
    db = get_db()
    
    # Fetch all boulders
    boulders = db.execute('SELECT * FROM boulder').fetchall()
    
    # Fetch all attempts for the user
    attempts = db.execute('SELECT * FROM attempt WHERE user_id = ?', (user_id,)).fetchall()
    
    completed_boulders = []
    flashed_boulders = []

    # Categorize boulders based on status
    for boulder in boulders:
        # Find attempts for the current boulder
        attempts_for_boulder = [a for a in attempts if a['boulder_id'] == boulder['id']]
        if attempts_for_boulder:
            attempt = attempts_for_boulder[0]
            if attempt['status'] == 'completed':
                completed_boulders.append(boulder)
            elif attempt['status'] == 'flashed':
                flashed_boulders.append(boulder)

    completed_boulders.sort(key=lambda b: b['difficulty'], reverse=True)
    flashed_boulders.sort(key=lambda b: b['difficulty'], reverse=True)

    return render_template('climber/archive.html',
                        completed_boulders=completed_boulders,
                        flashed_boulders=flashed_boulders)

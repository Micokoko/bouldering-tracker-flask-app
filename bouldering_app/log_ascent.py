from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bouldering_app.db import get_db
from .auth import login_required

bp = Blueprint('log_ascent', __name__, url_prefix='/climber')


@bp.route('/<int:id>/log_ascent', methods=('GET', 'POST'))
@login_required
def log_ascent_user(id):
    db = get_db()
    boulder = db.execute('SELECT * FROM boulder WHERE id = ?', (id,)).fetchone()
    
    if boulder is None:
        flash('Boulder not found.')
        
    
    return render_template('climber/log_ascent.html', boulder=boulder)
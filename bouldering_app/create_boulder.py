from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bouldering_app.db import get_db

bp = Blueprint('boulder', __name__, url_prefix='/boulder')

@bp.route('/boulders', methods=('GET', 'POST'))
def create_boulder():
    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        difficulty = request.form['difficulty']
        numberofmoves  = ['numberofmoves']
        db = get_db()
        error = None
        
        if not name:
            error = 'name is required.'
        elif not color:
            error = 'color is required.'
        elif not difficulty:
            error = 'difficulty name is required.'
        elif not numberofmoves:
            error = 'Last name is required.'

        if error is None:
            try:
                db.execute(
                        "INSERT INTO boulder (name, color, difficulty, numberofmoves) VALES (?, ?, ?, ?)",
                        (name, color, difficulty, numberofmoves),
                )
                db.commit()
                return redirect(url_for('auth.admin'))
            
            except db.IntegrityError:
                error = "Unable to add boulder"
        
        flash(error)
    
    return render_template('route_setter/boulders.html')


@bp.route('/admin')
def admin():
    return render_template('route_setter/admin.html')
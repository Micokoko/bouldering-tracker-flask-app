from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bouldering_app.db import get_db
from .auth import login_required  

bp = Blueprint('boulder', __name__, url_prefix='/route_setter')

@bp.route('/boulders', methods=('GET', 'POST'))
@login_required  
def create_boulder():
    if g.user['username'] != 'admin':  
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))  

    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        difficulty = request.form['difficulty']
        numberofmoves  = request.form['numberofmoves']
        db = get_db()
        error = None
        
        if not name:
            error = 'Name is required.'
        elif not color:
            error = 'Color is required.'
        elif not difficulty:
            error = 'Difficulty is required.'
        elif not numberofmoves:
            error = 'Number of moves is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO boulder (name, color, difficulty, numberofmoves) VALUES (?, ?, ?, ?)",
                    (name, color, difficulty, numberofmoves),
                )
                db.commit()
                return redirect(url_for('auth.admin'))
            except db.IntegrityError:
                error = "Unable to add boulder"
        
        flash(error)
    
    return render_template('route_setter/boulders.html')

@bp.route('/route_setter')
@login_required  
def admin():
    if g.user['username'] != 'admin':  
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))

    return render_template('route_setter/admin.html')


@bp.route('/add_boulder')
@login_required  
def add_boulder_route():
    if g.user['username'] != 'admin':
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))

    return render_template('route_setter/add_boulder.html')

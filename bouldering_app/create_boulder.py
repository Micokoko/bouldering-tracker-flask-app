from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bouldering_app.db import get_db
from .auth import login_required

bp = Blueprint('create_boulder', __name__, url_prefix='/route_setter')

@bp.route('/add_boulder', methods=('GET', 'POST'))
@login_required
def create_boulder_form():
    if g.user['username'] != 'admin':
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))

    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        difficulty = request.form['difficulty']
        numberofmoves = request.form['numberofmoves']
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
                return redirect(url_for('create_boulder.admin'))
            except db.IntegrityError:
                error = "Unable to add boulder."

        flash(error)

    return render_template('route_setter/add_boulder.html')



@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_boulder_form(id):
    db = get_db()
    boulder = db.execute('SELECT * FROM boulder WHERE id = ?', (id,)).fetchone()

    if boulder is None:
        flash('Boulder not found.')
        return redirect(url_for('create_boulder.admin'))

    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        difficulty = request.form['difficulty']
        numberofmoves = request.form['numberofmoves']
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
                    "UPDATE boulder SET name = ?, color = ?, difficulty = ?, numberofmoves = ? WHERE id = ?",
                    (name, color, difficulty, numberofmoves, id),
                )
                db.commit()
                return redirect(url_for('create_boulder.admin'))
            except db.IntegrityError:
                error = "Unable to update boulder."

        flash(error)

    return render_template('route_setter/update_boulder.html', boulder=boulder)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_boulder(id):
    db = get_db()
    boulder = db.execute('SELECT * FROM boulder WHERE id = ?', (id,)).fetchone()

    if boulder is None:
        flash('Boulder not found.')
        return redirect(url_for('create_boulder.admin'))

    if g.user['username'] != 'admin':
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))

    db.execute('DELETE FROM boulder WHERE id = ?', (id,))
    db.commit()
    flash('Boulder deleted successfully.')
    return redirect(url_for('create_boulder.admin'))




@bp.route('/admin')
@login_required
def admin():
    if g.user['username'] != 'admin':
        flash("You do not have access to this page.")
        return redirect(url_for('auth.login'))

    db = get_db()
    boulders = db.execute('SELECT * FROM boulder').fetchall()
    return render_template('route_setter/admin.html', boulders=boulders)




@bp.route('/add_boulder_page')
@login_required
def add_boulder_page():
    if g.user['username'] != 'admin':
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))

    return render_template('route_setter/add_boulder.html')

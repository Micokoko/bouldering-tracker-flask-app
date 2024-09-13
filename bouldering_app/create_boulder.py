from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
import os
from werkzeug.utils import secure_filename
from bouldering_app.db import get_db
from .auth import login_required
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('create_boulder', __name__, url_prefix='/route_setter')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/add_boulder', methods=('GET', 'POST'))
@login_required
def create_boulder_form():
    if g.user['username'] != 'admin':
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))

    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        difficulty = request.form.get('difficulty', type=int)
        numberofmoves = request.form.get('numberofmoves', type=int)
        set_date = request.form.get('set_date')
        description = request.form['description']
        boulder_image = request.files.get('boulder_image')
        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        elif not color:
            error = 'Color is required.'
        elif difficulty is None:
            error = 'Difficulty is required and must be an integer.'
        elif numberofmoves is None:
            error = 'Number of moves is required and must be an integer.'
        elif not set_date:
            error = 'Set date is required.'

        if error is None:
            try:
                image_filename = None
                if boulder_image and boulder_image.filename:
                    if allowed_file(boulder_image.filename):
                        image_filename = secure_filename(boulder_image.filename)
                        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
                        if not os.path.exists(os.path.dirname(image_path)):
                            os.makedirs(os.path.dirname(image_path))
                        boulder_image.save(image_path)
                    else:
                        error = 'File type not allowed.'
                        raise ValueError(error)

                set_date = datetime.strptime(set_date, '%Y-%m-%d').date()
                db.execute(
                    "INSERT INTO boulder (name, color, difficulty, numberofmoves, set_date, description, image, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, color, difficulty, numberofmoves, set_date, description, image_filename, g.user['id']),
                )
                db.commit()
                return redirect(url_for('create_boulder.admin'))
            except db.IntegrityError as e:
                error = f"Unable to add boulder: {e}"
            except ValueError as e:
                flash(str(e))

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
        difficulty = request.form.get('difficulty', type=int)
        numberofmoves = request.form.get('numberofmoves', type=int)
        set_date = request.form.get('set_date')
        description = request.form['description']
        boulder_image = request.files.get('boulder_image')
        error = None

        if not name:
            error = 'Name is required.'
        elif not color:
            error = 'Color is required.'
        elif difficulty is None:
            error = 'Difficulty is required and must be an integer.'
        elif numberofmoves is None:
            error = 'Number of moves is required and must be an integer.'
        elif not set_date:
            error = 'Set date is required.'

        if error is None:
            try:

                image_filename = boulder['image']  
                if boulder_image and boulder_image.filename:
                    if allowed_file(boulder_image.filename):
                        image_filename = secure_filename(boulder_image.filename)
                        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
                        boulder_image.save(image_path)
                    else:
                        error = 'File type not allowed.'
                        raise ValueError(error)

                set_date = datetime.strptime(set_date, '%Y-%m-%d').date()
                db.execute(
                    "UPDATE boulder SET name = ?, color = ?, difficulty = ?, numberofmoves = ?, description = ?, image = ?, set_date = ? WHERE id = ?",
                    (name, color, difficulty, numberofmoves, description, image_filename, set_date, id),
                )
                db.commit()
                return redirect(url_for('create_boulder.admin'))
            except db.IntegrityError as e:
                error = f"Unable to update boulder: {e}"
            except ValueError as e:
                flash(str(e))

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

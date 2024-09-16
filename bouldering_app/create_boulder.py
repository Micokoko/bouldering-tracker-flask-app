from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
import os
from werkzeug.utils import secure_filename
from .auth import login_required
from datetime import datetime
from bouldering_app.models import db
from bouldering_app.models import Boulder



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('create_boulder', __name__, url_prefix='/route_setter')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/add_boulder', methods=('GET', 'POST'))
@login_required
def create_boulder_form():
    if g.user.username != 'admin':
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

                new_boulder = Boulder(
                    name=name,
                    color=color,
                    difficulty=difficulty,
                    numberofmoves=numberofmoves,
                    set_date=set_date,
                    description=description,
                    image=image_filename, 
                    created_by=g.user.id
                )

                db.session.add(new_boulder)
                db.session.commit()
                return redirect(url_for('create_boulder.admin'))
            except Exception as e:
                db.session.rollback() 
                flash(f"Unable to add boulder: {e}")

        flash(error)

    return render_template('route_setter/add_boulder.html')




@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_boulder_form(id):
    boulder = Boulder.query.get(id)

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
                image_filename = boulder.image
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
                
                boulder.name = name
                boulder.color = color
                boulder.difficulty = difficulty
                boulder.numberofmoves = numberofmoves
                boulder.set_date = set_date
                boulder.description = description
                boulder.image = image_filename
                
                db.session.commit()
                return redirect(url_for('create_boulder.admin'))
            except Exception as e:
                db.session.rollback()
                flash(f"Unable to update boulder: {e}")
            except ValueError as e:
                flash(str(e))

        flash(error)

    return render_template('route_setter/update_boulder.html', boulder=boulder)




@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_boulder(id):
    boulder = Boulder.query.get(id)

    if boulder is None:
        flash('Boulder not found.')
        return redirect(url_for('create_boulder.admin'))

    if g.user.username != 'admin':
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))

    try:
        db.session.delete(boulder)
        db.session.commit()
        flash('Boulder deleted successfully.')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}')

    return redirect(url_for('create_boulder.admin'))



@bp.route('/admin')
@login_required
def admin():
    try:
        boulders = Boulder.query.all() 
        return render_template('route_setter/admin.html', boulders=boulders)
    except Exception as e:
        flash(f"Error retrieving boulders: {e}")
        return redirect(url_for('auth.user_page'))
    


@bp.route('/add_boulder_page')
@login_required
def add_boulder_page():
    if g.user.username != 'admin':
        flash("You do not have access to this page.")
        return redirect(url_for('auth.user_page'))

    return render_template('route_setter/add_boulder.html')

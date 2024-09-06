import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from bouldering_app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        gender = request.form['gender']
        age = request.form['age']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not firstname:
            error = 'First name is required.'
        elif not lastname:
            error = 'Last name is required.'
        elif not email:
            error = 'Email address is required.'
        elif not gender:
            error = 'Gender is required.'
        elif not age:
            error = 'Age is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, firstname, lastname, email, gender, age) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), firstname, lastname, email, gender, age),
                )
                db.commit()
                return redirect(url_for('auth.login'))
            except db.IntegrityError:
                error = f"User {username} is already registered."
        
        flash(error)
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # Check if the user exists
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        

        if user is None:
            error = 'Username or password cannot be found'
        elif not check_password_hash(user['password'], password):
            error = 'Username or password cannot be found'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            if user['username'] == 'admin':
                return redirect(url_for('auth.admin'))
            return redirect(url_for('auth.user_page'))  # Redirect to user_page on successful login

        flash(error)
        return redirect(url_for('index'))# Flash error message if login fails

    return render_template('climber/user_page.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))  

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/user_page')
@login_required
def user_page():
    return render_template('climber/user_page.html')


@bp.route('/route_setter')
@login_required
def admin():
    return render_template('route_setter/admin.html')


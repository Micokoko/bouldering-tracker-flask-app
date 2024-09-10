import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from bouldering_app.db import get_db

from datetime import datetime, date


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
                return redirect(url_for('index'))
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
            return redirect(url_for('auth.user_page')) 

        flash(error)
        return redirect(url_for('index'))

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



def format_date(date_value):
    if isinstance(date_value, str):
        try:
            return datetime.strptime(date_value, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            return 'Invalid date'
    elif isinstance(date_value, date):
        return date_value.strftime('%Y-%m-%d')
    else:
        return 'Invalid date'



@bp.route('/user_page')
@login_required
def user_page():
    db = get_db()
    user_id = g.user['id']

    boulders = db.execute('SELECT * FROM boulder').fetchall()
    attempts = db.execute('SELECT * FROM attempt WHERE user_id = ?', (user_id,)).fetchall()

    formatted_attempts = []
    for attempt in attempts:
        attempt_date = attempt['attempt_date']  
        formatted_date = format_date(attempt_date) if attempt_date else 'Invalid date'
        formatted_attempt = dict(attempt) 
        formatted_attempt['attempt_date'] = formatted_date
        formatted_attempts.append(formatted_attempt)

    highest_grade_climbed = max(
        (boulder['difficulty'] for boulder in boulders 
        if any(attempt['boulder_id'] == boulder['id'] and attempt['status'] in ['completed', 'flashed']
                for attempt in attempts)), 
        default=0
    )

    highest_grade_flashed = max(
        (boulder['difficulty'] for boulder in boulders 
        if any(attempt['boulder_id'] == boulder['id'] and attempt['status'] == 'flashed'
                for attempt in attempts)), 
        default=0
    )

    boulders_completed = len(set(
        attempt['boulder_id'] for attempt in attempts 
        if attempt['status'] in ['completed', 'flashed']
    ))

    return render_template(
        'climber/user_page.html', 
        boulders=boulders, 
        attempts=formatted_attempts,
        highest_grade_climbed=highest_grade_climbed,
        highest_grade_flashed=highest_grade_flashed,
        boulders_completed=boulders_completed
    )




@bp.route('/route_setter')
@login_required
def admin():
    db = get_db()
    boulders = db.execute('SELECT * FROM boulder').fetchall()
    return render_template('route_setter/admin.html', boulders=boulders)


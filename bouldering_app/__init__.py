from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "boulder.sqlite")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False, 
        UPLOAD_FOLDER='static/uploads/',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)


    from . import auth, create_boulder, log_ascent, leaderboards
    app.register_blueprint(auth.bp)
    app.register_blueprint(create_boulder.bp)
    app.register_blueprint(log_ascent.bp)
    app.register_blueprint(leaderboards.bp)

    # Define routes
    @app.route('/')
    def index():
        return render_template('auth/login.html')

    return app

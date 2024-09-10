import os
from flask import Flask, render_template

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',  # Consider changing this in production
        DATABASE=os.path.join(app.instance_path, 'boulder.sqlite'),
        UPLOAD_FOLDER='static/uploads/',  # Ensure this is set correctly
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    from . import db
    db.init_app(app)

    # Register blueprints
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import create_boulder
    app.register_blueprint(create_boulder.bp)
    
    from . import log_ascent
    app.register_blueprint(log_ascent.bp)
    
    # A simple page that says hello
    @app.route('/')
    def index():
        return render_template('auth/login.html')

    return app


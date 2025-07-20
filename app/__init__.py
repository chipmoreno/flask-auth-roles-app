# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize extensions but don't attach them to an app yet
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Tells LoginManager where the login route is
login_manager.login_message_category = 'info' # For better-looking flash messages

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    
    # --- Configuration ---
    # We'll use a simple config for now. In a real app, this would be more robust.
    app.config['SECRET_KEY'] = 'a_very_secret_key_that_you_should_change'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/auth_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Initialize Extensions ---
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # --- Import and Register Blueprints ---
        # Import parts of our application
        from . import models  # Import models to make sure they are known to SQLAlchemy
        
        from .auth.routes import auth_bp
        app.register_blueprint(auth_bp)

        from .main.routes import main_bp
        app.register_blueprint(main_bp)

        # You could add other blueprints here (e.g., for listings)

        # --- Create Database Tables ---
        # This is okay for development, for production you'd use Flask-Migrate
        db.create_all()

        return app
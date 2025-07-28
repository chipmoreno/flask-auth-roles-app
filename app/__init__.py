# app/__init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions but don't attach them to an app yet
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Tells LoginManager where the login route is
login_manager.login_message_category = 'info' # For better-looking flash messages

migrate = Migrate()

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
    migrate.init_app(app, db)
    
    with app.app_context():
        # Fix: Keep only one 'from . import models' and add 'from .models import Category'
        from . import models  
        from .models import Category # <--- ADD THIS IMPORT HERE FOR CATEGORY SEEDING
        from app.users.routes import users_bp
        app.register_blueprint(users_bp)    
        from .auth.routes import auth_bp
        app.register_blueprint(auth_bp)

        from .main.routes import main_bp
        app.register_blueprint(main_bp)
        
        from app.listings.routes import listings_bp
        app.register_blueprint(listings_bp)

        # --- NEW: Hardcode/Seed Initial Categories if they don't exist ---
        if not Category.query.first(): 
            print("Seeding initial categories...")
            tech = Category(name='Technology') # REMOVED: description='...'
            services = Category(name='Services') # REMOVED: description='...'
            real_estate = Category(name='Real Estate') # REMOVED: description='...'
            vehicles = Category(name='Vehicles') # REMOVED: description='...'
            jobs = Category(name='Jobs') # REMOVED: description='...'
            
            db.session.add_all([tech, services, real_estate, vehicles, jobs])
            db.session.commit()
            print("Initial categories seeded successfully.")
        else:
            print("Categories already exist in the database, skipping initial seeding.")
        # ------------------------------------------------------------------

        # --- Create Database Tables ---
        # This is okay for development, for production you'd use Flask-Migrate
        # Keep this commented if you're using Flask-Migrate to manage your schema
        # db.create_all() 


        # --- CUSTOM ERROR HANDLERS START ---
        @app.errorhandler(404) # <--- ADDED THIS MISSING DECORATOR!
        def not_found_error(error):
            # When an error occurs, Flask passes the error object as an argument
            return render_template('errors/404.html'), 404 # Return template and status code

        @app.errorhandler(403)
        def forbidden_error(error):
            return render_template('errors/403.html'), 403
        # --- CUSTOM ERROR HANDLERS END ---

        return app
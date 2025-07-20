# app/main/routes.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Create a Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    """Homepage."""
    return render_template('index.html', title='Welcome')

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    # current_user is automatically available from Flask-Login
    return render_template('profile.html', title='Your Profile', user=current_user)
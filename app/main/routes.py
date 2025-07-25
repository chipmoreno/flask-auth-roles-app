# app/main/routes.py

from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from ..models import User
# Create a Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/') ## I wonder why I need both of these? If I delete either, it breaks...
@main_bp.route('/index')
def index():
    """Homepage."""
    all_listings_url = url_for('listings.all_listings')
    create_listing_url = url_for('listings.new_listing')
    return render_template('index.html', title='Welcome',all_listings_url=all_listings_url, 
                           create_listing_url=create_listing_url)

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    # current_user is automatically available from Flask-Login
    return render_template('profile.html', title='Your Profile', user=current_user)

@main_bp.route('/listings')
def listings():
    """Browse all listings."""
    return render_template('listings/all_listings.html', title='All Listings')

@main_bp.route('/create_listing')
def create_listing():
    """Create a new listing."""
    return render_template('listings/create_listing.html', title='Create Listing')

@main_bp.route('/user/<string:username>')
def user_profile(username):
    # Fetch the user based on the username provided in the URL
    user = User.query.filter_by(username=username).first_or_404()
    
    # Render a template for the user's profile page
    return render_template('user_profile.html', title=f'{user.username}\'s Profile', user=user)
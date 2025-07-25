# app/listings/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import ListingForm
from ..models import Listing, Category, User # Import both models
from .. import db

listings_bp = Blueprint('listings', __name__, url_prefix='/listings')
@listings_bp.route('/')
@listings_bp.route('/all')
def all_listings():
    listings = Listing.query.filter_by(status='published').order_by(Listing.created_at.desc()).all()
    return render_template('listings/all_listings.html', title='All Listings', listings=listings)

@listings_bp.route('/new', methods=['GET', 'POST'])
@login_required # Only logged-in users can create listings
def new_listing():
    form = ListingForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by('name').all()]

    if form.validate_on_submit():
        category = Category.query.get(form.category.data) # Get the Category object
        listing = Listing(
            title=form.title.data,
            description=form.description.data,
            category=category, # Assign the Category object
            user_id=current_user.id, # Assign the current logged-in user as the owner
            location=form.location.data,
            contact_email=form.contact_email.data,
            contact_phone=form.contact_phone.data,
            price=form.price.data,
        )
        db.session.add(listing)
        db.session.commit()
        flash('Your listing has been created!', 'success')
        return redirect(url_for('listings.view_listing', listing_id=listing.id)) # Redirect to the new listing
    return render_template('listings/create_listing.html', title='New Listing', form=form)

@listings_bp.route('/<int:listing_id>')
def view_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    # Optionally increment views count here
    listing.views_count += 1
    db.session.commit()
    return render_template('listings/view_listing.html', title=listing.title, listing=listing) # Changed to listings/view_listing.html for clarity


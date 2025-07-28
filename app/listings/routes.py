# app/listings/routes.py

from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
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

@listings_bp.route('/<int:listing_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    listing = db.session.get(Listing, listing_id) # Use db.session.get for primary key lookup
    if listing is None:
        abort(404) # Not Found if listing_id doesn't exist

    # Authorization Check: Only the author can edit their listing
    if listing.author != current_user:
        abort(403) # Forbidden

    form = ListingForm()

    # Populate category choices for the form (same as create_listing)
    categories = Category.query.order_by(Category.name).all()
    form.category.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        listing.title = form.title.data
        listing.description = form.description.data
        listing.category_id = form.category.data
        listing.price = form.price.data if form.price.data is not None else None
        listing.location = form.location.data
        listing.contact_email = form.contact_email.data
        listing.contact_phone = form.contact_phone.data

        db.session.commit()
        flash('Your listing has been updated!', 'success')
        return redirect(url_for('listings.view_listing', listing_id=listing.id))
    elif request.method == 'GET':
        # Pre-populate the form with existing listing data on GET request
        form.title.data = listing.title
        form.description.data = listing.description
        form.category.data = listing.category_id
        form.price.data = listing.price
        form.location.data = listing.location
        form.contact_email.data = listing.contact_email
        form.contact_phone.data = listing.contact_phone

    return render_template('listings/edit_listing.html', title='Edit Listing', form=form, listing=listing)

@listings_bp.route('/<int:listing_id>/delete', methods=['POST'])
@login_required
def delete_listing(listing_id):
    listing = db.session.get(Listing, listing_id) # Use db.session.get for primary key lookup
    if listing is None:
        abort(404) # Not Found if listing_id doesn't exist

    # Authorization Check: Only the author can delete their listing
    if listing.author != current_user:
        abort(403) # Forbidden

    db.session.delete(listing)
    db.session.commit()
    flash('Your listing has been deleted!', 'success')
    return redirect(url_for('listings.all_listings'))
# app/users/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
# from ..forms import UpdateAccountForm # You might create this form later

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/<username>')
def profile(username):
    # This would eventually show a public profile page for a user
    # user = User.query.filter_by(username=username).first_or_404()
    # return render_template('users/profile.html', title=f"{user.username}'s Profile", user=user)
    flash(f"User profile page for {username} is under construction!", 'info')
    return redirect(url_for('main.index'))


@users_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # This is a placeholder. You'll need a form (e.g., UpdateAccountForm) here later.
    flash("Edit Profile page is under construction!", 'info')
    return render_template('users/edit_profile.html', title='Edit Profile') # You'd need to create this template
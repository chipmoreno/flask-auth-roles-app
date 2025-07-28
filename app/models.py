# my_flask_app3/app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from datetime import datetime # Import datetime for default timestamps if not using db.func.now()
from sqlalchemy_serializer import SerializerMixin # For easy serialization if needed later

# Flask-Login user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    return db.session.get(User, int(user_id)) # Recommended using db.session.get

# Many-to-many association table for Users and Roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users' # Correct
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model):
    __tablename__ = 'roles' # Correct
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f'<Role {self.name}>'

class Category(db.Model):
    """Category model for listings (e.g., Services, Housing, For Sale)."""
    __tablename__ = 'categories' # Correct
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    # The 'listings' relationship is managed by the backref on the Listing model.
    # Defining it here as well can lead to conflicts, especially if lazy/backref settings differ.
    # The backref from Listing is usually sufficient for simple one-to-many.
    # If you still want it here for explicit declaration or specific query needs,
    # it should be something like:
    # listings_explicit = db.relationship('Listing', backref='category_explicit_ref', lazy=True, primaryjoin="Category.id == Listing.category_id")
    # But for a basic setup, the backref in Listing is enough.

    def __repr__(self):
        return f'<Category {self.name}>'

class Listing(db.Model):
    __tablename__ = 'listings' # Correct
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # --- Corrected User relationship ---
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Refers to 'users.id' table
    author = db.relationship('User', backref=db.backref('listings', lazy='dynamic')) # 'listings' is the collection on User model

    # --- Corrected Category relationship ---
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False) # Refers to 'categories.id' table
    category = db.relationship('Category', backref=db.backref('listings', lazy=True)) # 'listings' is the collection on Category model

    location = db.Column(db.String(120), nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(60), nullable=True)
    price = db.Column(db.Float, nullable=True)
    # currency = db.Column(db.String(10), nullable=True) # <-- ADD THIS BACK IF YOU NEED CURRENCY FIELD

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    status = db.Column(db.String(20), nullable=False, default='published')
    views_count = db.Column(db.Integer, default=0)
    is_sponsored = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f'<Listing {self.title} by User {self.user_id}>'
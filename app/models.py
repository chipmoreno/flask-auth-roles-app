# my_flask_app3/app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

# Flask-Login user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    return User.query.get(int(user_id))

# Many-to-many association table for Users and Roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')), # CORRECTED: 'users.id'
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))  # CORRECTED: 'roles.id'
)

class User(UserMixin, db.Model):
    __tablename__ = 'users' # CORRECTED: Added __tablename__
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # Using backref with lazy='dynamic' for better query flexibility on the 'users' side
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
    __tablename__ = 'roles' # CORRECTED: Added __tablename__
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self): # CORRECTED: Indentation fixed
        return f'<Role {self.name}>'

class Category(db.Model):
    """Category model for listings (e.g., Services, Housing, For Sale)."""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    listings = db.relationship('Listing', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='listings', lazy=True) 
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    location = db.Column(db.String(120), nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(60), nullable=True)
    price = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    status = db.Column(db.String(20), nullable=False, default='published')
    views_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Listing {self.title} by User {self.user_id}>'
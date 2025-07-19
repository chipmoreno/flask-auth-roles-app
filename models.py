from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

user_roles = db.Table('user_roles',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(128))
	roles = db.relationship('Role', secondary=user_roles, backref='users')

	def set_password(self, password):
		self.password_hash=generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def has_role(self, role_name):
		return any(role.name == role_name for role in self.roles)

class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)

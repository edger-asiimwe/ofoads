from datetime import datetime
from ofoads_app import db, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model): 
 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # ['admin', 'restaurant', client]

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('Password cannot be accessed') 
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_restaurant(self):
        return self.role == 'restaurant'
    
    @property
    def is_client(self):
        return self.role == 'client'
    
    @property
    def next_page_url(self):
        return f'{self.role}.dashboard'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return 'User: {} - {}'.format(self.email, self.role)
    


class Restaurant(db.Model):

    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_admin(self, user_id):
        self.admin_id = user_id

    def __repr__(self):
        return 'Restaurant: {} - {}'.format(self.name, self.id)


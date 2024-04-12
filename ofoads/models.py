from ofoads import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):  

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
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'User: {} - {}'.format(self.email, self.role)
from datetime import datetime
from ofoads_app import db, login_manager

from flask_login import UserMixin, current_user
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
    def restaurant_id(self):
        return Restaurant.query.filter_by(admin_id=current_user.id).first().id
    
    @property
    def restaurant_name(self):
        return Restaurant.query.filter_by(admin_id=current_user.id).first().name
    
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
    name = db.Column(db.String, nullable=False) # TODO: Add unique constraint and rollback on error
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_admin(self, user_id):
        self.admin_id = user_id

    def add_restaurant(self, form):
        # Create a new user to access the restaurant dashboard
        user = User(email=form.email.data, role='restaurant')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Retrieve the new created user to set as the admin of the restaurant
        created_user = User.query.filter_by(email=form.email.data).first()

        # Add the restaurant to the database with created user as the admin
        self.set_admin(created_user.id)
        self.first_name = form.first_name.data
        self.last_name = form.last_name.data
        self.name = form.name.data
        self.latitude = form.latitude.data
        self.longitude = form.longitude.data
        db.session.add(self)
        db.session.commit()

        return self

    def __repr__(self):
        return 'Restaurant: {} - {}'.format(self.name, self.id)



class Food(db.Model):

    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def get_foods(self):
        foods = Food.query.filter_by(restaurant_id=current_user.restaurant_id).order_by(Food.created_at.desc()).all()
        return [{
            'id': food.id,
            'name': food.name,
            'price': food.price,
            'time': food.time,
        } for food in foods
        ]
        

    def add_food(self, request):
        self.restaurant_id = current_user.restaurant_id
        self.name = request.form['name']
        self.price = request.form['price']
        self.time = self.add_time_calculation(request.form['time'], request.form['min_hour'])
        db.session.add(self)
        db.session.commit()

        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'time': self.time,
            'status': self.status
        }
    
    def update_food(self, request):
        food = Food.query.filter_by(id=request.form['id']).first()
        food.name = request.form['name']
        food.price = request.form['price']
        food.time = self.add_time_calculation(request.form['time'], request.form['min_hour'])
        db.session.commit()

        return {
            'id': food.id,
            'name': food.name,
            'price': food.price,
            'time': food.time,
            'status': food.status
        }
    
    def add_time_calculation(self, time, min_hour):
        if min_hour == "hours":
            return int(time) * 60
        return int(time)

    def __repr__(self):
        return 'Food: {} - {} - {} - {} - {}'.format(self.id, self.name, self.price, self.time, self.status)
    




    class Client(db.model):
     __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)




    def add_client(self, form):
        user = User(
            email=form.email.data,
            password=form.password.data,
            
            name=form.name.data,
            role='client'
        )
        # Add the user to the database
        db.session.add(user)
        db.session.commit()

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from ..models import User, Restaurant
from ..forms import LoginForm
from .. import db

from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(request.args.get('next') or url_for(user.next_page_url))
        else:
            flash('Invalid Login Credentials', 'danger')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out!', 'success')
    return redirect(url_for('auth.login'))


# Method to add demo users in the database.
# DO NOT DELETE THIS METHOD
@auth.route('/demo_users')
def register():
    users = [
        {
            'email': 'admin@gmail.com',
            'password': 'admin',
            'role': 'admin',
        },
        {
            'email': 'rest@gmail.com',
            'password': 'rest',
            'role': 'restaurant',
        },
        {
            'email': 'client@gmail.com',
            'password': 'client',
            'role': 'client',
        }
    ]

    hotels = {
        "first_name": "Ndayisenga",
        "last_name": "Jean Paul",
        "name": "Kigali Serena Hotel",
        "latitude": "-1.9441",
        "longitude": "30.0619",
        "verified": True
    }

    for user in users:
        new_user = User(email=user['email'], role=user['role'])
        new_user.set_password(user['password'])
        db.session.add(new_user)
        db.session.commit()

        print('User Added')

        if new_user.is_restaurant:
            restaurant = Restaurant()
            restaurant.set_admin(new_user.id)
            restaurant.first_name = hotels['first_name']
            restaurant.last_name = hotels['last_name']
            restaurant.name = hotels['name']
            restaurant.latitude = hotels['latitude']
            restaurant.longitude = hotels['longitude']
            restaurant.verified = hotels['verified']
            db.session.add(restaurant)
            db.session.commit()

            print('Restaurant Added')

    return "Success"
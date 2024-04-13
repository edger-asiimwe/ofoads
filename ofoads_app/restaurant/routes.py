from flask import render_template, flash, redirect, url_for

from .. import db
from ..models import User, Restaurant
from ..forms import RestaurantRegistrationForm

from . import restaurant

@restaurant.route('/dashboard')
def dashboard():
    return render_template('restaurant/dashboard.html')

@restaurant.route('/register', methods=['GET', 'POST'])
def register():
    form = RestaurantRegistrationForm()
    if form.validate_on_submit():
        print("Form Submitted")
        user = User(email=form.email.data, role='restaurant')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        created_user = User.query.filter_by(email=form.email.data).first()
        restaurant = Restaurant(
            admin_id=created_user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            name=form.name.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data
        )
        db.session.add(restaurant)
        db.session.commit()

        flash('Restaurant Account Created Successfully', 'success')
        return redirect(url_for('auth.login'))
    
    print("Form Not Submitted")
    return render_template('restaurant/register.html', form=form)
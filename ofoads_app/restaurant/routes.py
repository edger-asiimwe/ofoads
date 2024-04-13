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
        restaurant = Restaurant().add_restaurant(form)
        flash(message='{} Account Created Successfully'.format(restaurant.name), 
              category='success')
        return redirect(url_for('auth.login'))

    return render_template('restaurant/register.html', form=form)
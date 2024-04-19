from flask import render_template, flash, redirect, url_for, request, jsonify
import random

from .. import db
from ..models import User, Restaurant, Food
from ..forms import RestaurantRegistrationForm


from . import restaurant


@restaurant.route('/register', methods=['GET', 'POST'])
def register():
    form = RestaurantRegistrationForm()
    if form.validate_on_submit():
        restaurant = Restaurant().add_restaurant(form)
        flash(message='{} Account Created Successfully'.format(restaurant.name), 
              category='success')
        return redirect(url_for('auth.login'))

    return render_template('restaurant/register.html', form=form)


@restaurant.route('/order_count')
def order_count():
    updated_value = random.randint(1, 100)
    # TODO: Update to query the database for orders under a restaurant
    return str(updated_value)

@restaurant.route('/dashboard')
def dashboard():
    return render_template('restaurant/dashboard.html')


@restaurant.route('/orders')
def orders():
    return render_template('restaurant/orders.html')


@restaurant.route('/menu')
def menu():
    #foods = Food().get_foods()
    food_model = Food()
    foods = food_model.get_foods_by_restaurant()
    return render_template('restaurant/menu.html', foods=foods)

@restaurant.route('/add_food', methods=['POST', 'PUT'])
def add_food():
    food = Food().add_food(request)
    return jsonify({'food': food})




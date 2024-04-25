from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user
import random

from .. import db
from ..models import User, Restaurant, Food, Order
from ..forms import RestaurantRegistrationForm
from sqlalchemy.orm import joinedload


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


# @restaurant.route('/orders')
# def orders():

#     return render_template('restaurant/orders.html')



@restaurant.route('/menu')
def menu():
    # Query foods for the current restaurant
    food_model = Food()
    foods = food_model.get_foods_by_restaurant()
    
    # Render the menu template with foods
    return render_template('restaurant/menu.html', foods=foods)


@restaurant.route('/add_food', methods=['POST', 'PUT'])
def add_food():
    food = Food().add_food(request)
    return jsonify({'food': food})




@restaurant.route('/orders')
def orders():
    # Query pending orders for the current restaurant
    pending_orders = Order.query.filter_by(restaurant_id=current_user.restaurant_id).options(joinedload(Order.food)).all()
    
    

    # Render the orders template with pending orders
    return render_template('restaurant/orders.html', orders=pending_orders)

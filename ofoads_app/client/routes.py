
from flask import render_template, flash, redirect, url_for, request, jsonify, session
import threading
from flask_login import current_user
from .. import db
from ..models import Client, Food , Order
from ..forms import ClientRegistrationForm, ClientLocationForm
from . import client
from ..algo import find_best_restaurant, get_food_info, compare_food_items
from datetime import datetime


@client.route('/register', methods=['GET', 'POST'])
def register():
    form = ClientRegistrationForm()
    if form.validate_on_submit():
        client = Client().add_client(form)
        flash('Account Created Successfully', 'success')
        return redirect(url_for('auth.login'))

    return render_template('client/register.html', form=form)

@client.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = ClientLocationForm()
    if form.validate_on_submit():
        latitude = form.latitude.data
        longitude = form.longitude.data
        session[f'{current_user}_user_location'] = (latitude, longitude)
        return redirect(url_for('client.food_display'))
    return render_template('client/dashboard.html', form=form)

@client.route('/food_display', methods=['GET', 'POST'])
def food_display():
    foods = Food().get_all_foods()
    return render_template('client/food_display.html', foods=foods)

@client.route('/submit_location', methods=['POST'])
def submit_location():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    user_location = (float(latitude), float(longitude))
    best_restaurant = find_best_restaurant(user_location)
    return jsonify({'restaurant_id': best_restaurant.id, 'restaurant_name': best_restaurant.name})



@client.route('/select_food/<selected_food>', methods=['POST', 'GET'])
def select_food(selected_food):
    user_location = session.get(f'{current_user}_user_location')
    user_location = (float(user_location[0]), float(user_location[1]))
    
    # Find the best restaurant based on the user's location and selected food
    best_restaurant = find_best_restaurant(user_location)
    
    # Get information about the selected food from the valid restaurants
    food_info = get_food_info(selected_food, best_restaurant.keys())
    
    # Compare the food items and select the best option
    valid_foods = compare_food_items(food_info, best_restaurant, user_location)
    
    # Assuming the first item in valid_foods is the best option
    best_food = valid_foods[0]

    print(best_food['restaurant_id'])

    
    # Render the template with selected food information
    return render_template('client/confirm_order.html', selected_food=selected_food, price=best_food['price'], restaurant_id=best_food['restaurant_id'])



@client.route('/place_order/<selected_food>/<restaurant_id>', methods=['POST'])
def place_order(selected_food, restaurant_id):
    # Assuming the form submits directly to this route
    # Create a new order
    order = Order(
        food_id=selected_food,  # Replace selected_food_id with the actual ID of the selected food
        restaurant_id=restaurant_id,
        client_id=current_user.id 
    )

    db.session.add(order)
    db.session.commit()
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('client.dashboard'))
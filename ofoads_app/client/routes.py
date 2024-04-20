
from flask import render_template, flash, redirect, url_for, request, jsonify, session
import threading
from flask_login import current_user
from .. import db
from ..models import Client, Food
from ..forms import ClientRegistrationForm, ClientLocationForm
from . import client
from ..algo import find_best_restaurant, update_order_count, get_preparation_time, schedule_order_completion


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
    print(user_location)
    selected_food = selected_food
    print(selected_food)
    print('Before calling the distance this')
    best_restaurant = find_best_restaurant(selected_food, user_location)
    update_order_count(best_restaurant.id)
    preparation_time = get_preparation_time(selected_food, best_restaurant.id)
    schedule_order_completion(best_restaurant.id, preparation_time)
    return jsonify({'restaurant_id': best_restaurant.id, 'restaurant_name': best_restaurant.name})

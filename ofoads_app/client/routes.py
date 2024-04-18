
from flask import render_template, flash, redirect, url_for, request, jsonify
import threading
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

@client.route('/select_food', methods=['POST'])
def select_food():
    selected_food = request.form['food']
    user_location = (float(request.form['latitude']), float(request.form['longitude']))
    best_restaurant = find_best_restaurant(selected_food, user_location)
    update_order_count(best_restaurant.id)
    preparation_time = get_preparation_time(selected_food, best_restaurant.id)
    schedule_order_completion(best_restaurant.id, preparation_time)
    return jsonify({'restaurant_id': best_restaurant.id, 'restaurant_name': best_restaurant.name})

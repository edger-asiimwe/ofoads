
from datetime import datetime, time, timedelta
from geopy.distance import geodesic
import threading
#import requests
from .models import Food, Restaurant
from . import db
def find_best_restaurant(user_location, radius=6):
    all_restaurants = Restaurant.query.all()
    valid_restaurants = []

    for restaurant in all_restaurants:
        distance = get_distance(user_location, (float(restaurant.latitude), float(restaurant.longitude)))
        if distance <= radius:
            valid_restaurants.append((restaurant, distance))

    if not valid_restaurants:
        return None

    best_restaurant = min(valid_restaurants, key=lambda x: x[1])[0]
    return best_restaurant

def get_distance(origin, destination):
    return geodesic(origin, destination).kilometers

def get_preparation_time(selected_food, restaurant_id):
    food = Food.query.filter_by(restaurant_id=restaurant_id, name=selected_food).first()
    return food.preparation_time if food else None

def get_food_price(selected_food, restaurant_id):
    food = Food.query.filter_by(restaurant_id=restaurant_id, name=selected_food).first()
    return food.price if food else None

def update_order_count(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        restaurant.orders += 1
        db.session.commit()

def decrement_order_count(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant and restaurant.orders > 0:
        restaurant.orders -= 1
        db.session.commit()

def schedule_order_completion(restaurant_id, preparation_time):
    def complete_order():
        timedelta(seconds=preparation_time)
        decrement_order_count(restaurant_id)

    thread = threading.Thread(target=complete_order)
    thread.start()

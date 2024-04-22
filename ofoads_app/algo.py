from geopy.distance import geodesic
from .models import Food, Restaurant
from . import db

def find_best_restaurant(user_location, radius=5):
    all_restaurants = Restaurant.query.all()
    valid_restaurants = {}

    for restaurant in all_restaurants:
        distance = get_distance(user_location, (float(restaurant.latitude), float(restaurant.longitude)))
        if distance <= radius:
            valid_restaurants[restaurant.id] = {
                'location': (restaurant.latitude, restaurant.longitude),
                'distance': distance
            }

    return valid_restaurants

def get_distance(origin, destination):
    return geodesic(origin, destination).kilometers

def get_food_info(selected_food, restaurant_ids):
    food_info = {}
    for restaurant_id in restaurant_ids:
        food = Food.query.filter_by(restaurant_id=restaurant_id, name=selected_food).first()
        if food:
            food_info[food.id] = {
                'restaurant_id': restaurant_id,
                'price': food.price,
                'time': food.time
            }
    return food_info

def compare_food_items(food_info, restaurant_data, user_location):
    valid_foods = []

    for food_id, info in food_info.items():
        restaurant_id = info['restaurant_id']
        restaurant_location = restaurant_data.get(restaurant_id)
        if restaurant_location:
            distance = restaurant_location['distance']
            valid_foods.append({
                'food_id': food_id,
                'restaurant_id': restaurant_id,
                'price': info['price'],
                'time': info['time'],
                'distance': distance
            })

    valid_foods.sort(key=lambda x: (x['price'], x['time'], x['distance']))

    return valid_foods

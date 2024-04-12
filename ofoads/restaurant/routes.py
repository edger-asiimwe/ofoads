from flask import render_template

from . import restaurant

@restaurant.route('/login')
def login():
    return render_template('restaurant/login.html')
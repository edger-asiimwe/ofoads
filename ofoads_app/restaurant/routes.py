from flask import render_template

from . import restaurant

@restaurant.route('/dashboard')
def dashboard():
    return render_template('restaurant/dashboard.html')
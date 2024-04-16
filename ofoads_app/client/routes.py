from flask import render_template, flash, redirect, url_for, request
from .. import db
from ..models import Client, User, Food
from ..forms import ClientRegistrationForm, ClientLocationForm
from . import client

@client.route('/register', methods=['GET', 'POST'])
def register():
    form = ClientRegistrationForm()
    print('Before IF')
    if form.validate_on_submit():
        print('Form Validated')
        client = Client().add_client(form)
        flash(message='Account Created Successfully', category='success')
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

from flask import render_template, flash, redirect, url_for, request
from .. import db
from ..models import Client, User
from ..forms import ClientRegistrationForm
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


@client.route('/dashboard')
def dashboard():
    return render_template('client/dashboard.html')
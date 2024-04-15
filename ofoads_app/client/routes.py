from flask import render_template

from . import client
from ..models import Client
from ..forms import ClientRegistrationForm

@client.route('/dashboard')
def dashboard():
    return render_template('client/dashboard.html')


@client.route('/register')
def dashboard():        
    return "Success"

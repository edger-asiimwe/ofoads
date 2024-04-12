from flask import render_template

from . import client

@client.route('/dashboard')
def dashboard():
    return render_template('client/dashboard.html')
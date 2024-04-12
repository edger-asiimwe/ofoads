from flask import render_template

from . import client

@client.route('/login')
def login():
    return render_template('client/login.html')
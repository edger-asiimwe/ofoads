from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from .admin import admin as admin_blueprint
from .restaurant import restaurant as restaurant_blueprint
from .client import client as client_blueprint
from .auth import auth as auth_blueprint

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

db = SQLAlchemy()

def init_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(client_blueprint, url_prefix='/client')
        app.register_blueprint(admin_blueprint, url_prefix='/admin')
        app.register_blueprint(restaurant_blueprint, url_prefix='/restaurant')   

        return app


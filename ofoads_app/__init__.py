from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

db = SQLAlchemy()
login_manager = LoginManager()

# Settings for the Login Manager
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'

def init_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    with app.app_context():
        from .admin import admin as admin_blueprint
        from .restaurant import restaurant as restaurant_blueprint
        from .client import client as client_blueprint
        from .auth import auth as auth_blueprint

        db.create_all()

        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(client_blueprint, url_prefix='/client')
        app.register_blueprint(admin_blueprint, url_prefix='/admin')
        app.register_blueprint(restaurant_blueprint, url_prefix='/restaurant')

        register_error_handlers(app)   

        return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def unathorized_access(e):
        return render_template('403.html'), 403
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from .admin import admin as admin_blueprint
from .restaurant import restaurant as restaurant_blueprint

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

db = SQLAlchemy()

def init_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        register_blueprints(app)
        register_extensions(app)
        register_errorhandlers(app)

        return app


def register_blueprints(app):
    """
        Register the application blueprints

        args:
            app: `[obj]`

        return None
        
    """

    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(restaurant_blueprint, url_prefix='/restaurant')    

    return None


def register_extensions(app):
    """
        Register the application extensions

        args:
            app: `[obj]`

        return None
        
    """

    db.init_app(app)

    return None


def register_errorhandlers(app):
    """
        Register error handlers.
        
        return None
    """

    @app.errorhandler(401)
    def internal_error(error):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return None
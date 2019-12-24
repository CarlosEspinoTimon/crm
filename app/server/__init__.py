"""
Server Module
"""
import sys

import requests

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


sys.stdout.flush()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(app_config='config.Prod'):
    app = Flask(__name__)
    app.config.from_object(app_config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Import models
    from .models.customer import Customer
    from .models.user import User

    # Import blueprints
    from .controllers.customer_controller import customers
    app.register_blueprint(customers)
    from .controllers.user_controller import users
    app.register_blueprint(users)
    from .controllers.authentication_controller import authentication
    app.register_blueprint(authentication)

    # A simple page that says server status
    @app.route('/')
    def home():
        return jsonify('The server is running!!!')

    return app

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


sys.stdout.flush()
db = SQLAlchemy()
migrate = Migrate()


def create_app(app_config):
    app = Flask(__name__)
    app.config.from_object(app_config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # A simple page that says server status
    @app.route('/')
    def home():
        return jsonify('The server is running!!')

    return app

# app/__init__.py
from flask import Flask, g
from flask_mysqldb import MySQL
import os

mysql = MySQL()  # Global MySQL extension instance


def create_app():
    app = Flask(__name__)

    # Application Configuration
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'bryanmarshall.com')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'uo6wzuqzpup3g')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'rrgx24vazvll')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'dbptztdppxhiif')

    mysql.init_app(app)

    # Import Blueprints
    from .blueprints.home import home_bp
    from .blueprints.fantasy import fantasy_bp
    from .blueprints.core import core_bp
    from .blueprints.mock_draft import mock_draft_bp
    # Register Blueprints
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(fantasy_bp, url_prefix='/fantasy')
    app.register_blueprint(core_bp, url_prefix='/core')
    app.register_blueprint(mock_draft_bp, url_prefix='/mock_draft')

    return app
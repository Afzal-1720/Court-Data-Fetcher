from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Enable CORS for all routes

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import api
        app.register_blueprint(api.bp)

    return app
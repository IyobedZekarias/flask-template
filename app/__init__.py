"""Flask application for Quality Deviations"""
from flask import Flask

# Register blueprints
from app.routes import health_routes,hello_world_routes

from app.config import config_by_name

def create_app(config_name='DEV'):
    """App factory for Flask app"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    app.register_blueprint(hello_world_routes)
    app.register_blueprint(health_routes)

    return app

"""MODULE FOR INITIALIZED THE ROUTES"""
import logging
import os

from flask import Blueprint

from app.routes.hello_world import hello_world_routes

from app.utils.response_handling import error_response, success_response

health_routes = Blueprint('health_routes', __name__)

logger = logging.getLogger(__name__)


@health_routes.route('/')
def hello_world():
    """Hello World for deviations api endpoint"""
    return '<h2>app</h2>', 200


@health_routes.route('/health')
def health_check():
    """Health Check for api endpoint"""
    return 'OK', 200

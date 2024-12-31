"""WSGI handling for Gunicorn"""
from app import create_app

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def app(gunicorn_env):
    """Accepts ENV from Gunicorn call and passes to create_app"""
    return create_app(config_name=gunicorn_env)
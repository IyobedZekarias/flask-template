"""CONFIGURATION FILE FOR GUNICORN"""
import os
import multiprocessing
import gunicorn

app_env = os.getenv("APP_ENV", None)

gunicorn.SERVER_SOFTWARE = 'Takeda Quality Deviations Generator'
gunicorn.SERVER = 'undisclosed'
if app_env is None or app_env != "LOCAL":
    workers = (2 * multiprocessing.cpu_count()) + 1
else:
    workers = 1
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '300'))
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:80')
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}

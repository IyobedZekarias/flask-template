"""Module for standardized success and error responses."""
from flask import jsonify

def success_response(data=None, message="", status_code=200):
    """Creates a standardized JSON success response."""
    response_body = {
        'status': 'success',
        'data': data,
        'message': message
    }
    response = jsonify(response_body)
    response.status_code = status_code
    return response

def error_response(message, status_code):
    """Creates a standardized JSON error response."""
    response_body = {
        'status': 'error',
        'message': message
    }
    response = jsonify(response_body)
    response.status_code = status_code
    return response

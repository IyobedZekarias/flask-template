"""ROUTE FOR TRANSLATION ENDPOINT"""
import logging
import time
from flask import Blueprint
from app.utils import requires_auth, use_cors, success_response, error_response

logger = logging.getLogger(__name__)

hello_world_routes = Blueprint('hello_world_routes', __name__)

@hello_world_routes.route('/hello_world/<string:user_name>', methods=['OPTIONS', 'GET'])
@use_cors(methods="GET")
@requires_auth
def hello_world(claims, user_name: str):
    """
    tells you hello

    Returns:
    - `200 OK`: Translated text.
    - `400 Bad Request`: Missing name in url
    - `500 Internal Server Error`: Error during translation processing.
    ```
    """
    # email = claims["sub"]
    if user_name is None:
        return error_response("user name not included", 400)

    start_time = time.time()

    response_data = {
        'time': f'{time.time() - start_time:.2f}s',
        'text': f"hello {user_name}"
    }

    return success_response(data=response_data)

"""HANDLES CORS (CROSS-ORIGIN-RESOURCE-SHARING) FOR FRONTEND"""
from functools import wraps

from flask import Response, request, current_app


def use_cors(methods):
    """
    Wrapper for handling CORS of a flask endpoint, put this around any endpoint that will be directly called by the frontend in a browser.
    For CORS standars check here: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    """
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            origin = request.headers.get('Origin', None)
            if origin is None:
                origin = request.headers.get('Referer', None)

            if origin is not None:
                allowed_origins = current_app.config.get('ALLOWED_ORIGINS', [])
                captured_origin = current_app.config.get('CAPTURED_ORIGIN', "*")
                for allowed in allowed_origins:
                    if allowed in origin:
                        # captured_origin = origin
                        protocol = 'https://' if 'https' in origin else 'http://'
                        captured_origin = protocol + allowed
            else:
                captured_origin = "*"

            headers = {
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": captured_origin,
                "Access-Control-Allow-Methods": methods,
                "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept, Connection, reportID, Origin",
                "Access-Control-Allow-Credentials": 'true'
            }
            if request.method == "OPTIONS":
                return Response(response={"test": "here"}, status=204, headers=headers)

            res = f(*args, **kwargs)
            if isinstance(res, Response):
                res_headers = dict(res.headers)
                res_headers.update(headers)

                res = (res.get_data(as_text=True), res.status, res_headers)
            elif isinstance(res, tuple):
                if len(res) > 2:
                    res[2].update(headers)
                else:
                    res = res + (headers, )
            return res

        return decorated
    return wrapper

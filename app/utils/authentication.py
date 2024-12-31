"""AUTHENTICATION USING OKTA AUTHENTICATION PATTERNS"""
import asyncio
import os
from functools import wraps

from dotenv import load_dotenv
from flask import current_app, request
from okta_jwt_verifier import BaseJWTVerifier

from app.utils.response_handling import error_response

load_dotenv()


CLIENT_ID = os.getenv('CLIENT_ID')
ISSUER = os.getenv('ISSUER')


class AuthError(Exception):
    """Custom error for auth errors"""

    def __init__(self, messages: dict, code):
        self.messages = messages
        self.code = code


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(messages={"code": "authorization_header_missing",
                        "description":
                                  "Authorization header is expected"}, code=401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(messages={"code": "invalid_header",
                        "description":
                                  "Authorization header must start with"
                                  " Bearer"}, code=401)
    if len(parts) == 1:
        raise AuthError(messages={"code": "invalid_header",
                        "description": "Token not found"}, code=401)
    if len(parts) > 2:
        raise AuthError(messages={"code": "invalid_header",
                        "description":
                                  "Authorization header must be"
                                  " Bearer token"}, code=401)

    token = parts[1]
    return token


def requires_auth(f):
    """
    Wrapper of a flask endpoint, if you'd like the endpoint to only be called by authenticated users decorated it with @required_auth

    For development you don't need to pass a token to your call
    For prod and testing you will need to include "Authorization": "Bearer {token}" as a header in your call

    When developing an endpoint this wrapper will pass the argument (claims) into the function that it wraps. Claims contains the user's details from okta as a dictionary. The key "sub" contains the user's email
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_app.config.get('ENV') == 'LOCAL':
            return f(*args, **kwargs, claims={"sub": current_app.config.get('EMAIL')})
        try:
            token = get_token_auth_header()
        except AuthError as exc:
            return error_response(exc.messages, exc.code)
        except Exception:
            return error_response('There was an error reading your token', 500)
        jwt_verifier = BaseJWTVerifier(
            issuer=ISSUER, client_id=CLIENT_ID, audience='api://default')
        try:
            asyncio.run(jwt_verifier.verify_access_token(token))
        except Exception:
            return error_response('Your token was invalid', 400)

        _, claims, _, _ = jwt_verifier.parse_token(token)
        if "sub" not in claims:
            return error_response("sub needs to be included in the token and must contain email of user", 400)

        return f(*args, **kwargs, claims=claims)

    return decorated

from flask import request, abort
from functools import wraps
from authtools import authenticate_user


def is_authenticated(f):
    """
    User's authentication must be present and up to date
    """

    @wraps(f)
    def fn(*args, **kwargs):

        headers = request.headers
        user_id = headers['user_id']
        fb_auth_token = headers['fb_auth_token']

        if not authenticate_user(user_id, fb_auth_token):
            # 401: Unauthorized
            abort(401)

        return f(*args, **kwargs)
    return fn

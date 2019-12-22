from functools import wraps
from .token_managment import process_token
from flask import request, jsonify


def check_user_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        payload, error = process_token()
        if error:
            return payload
        else:
            return func(*args, **kwargs)

    return decorated_funcion


def validate_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                return jsonify(errors), 400
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

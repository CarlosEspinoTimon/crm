from functools import wraps
from flask import jsonify, request, current_app as app

from ..models.user import User

import jwt


def check_user_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        payload, error, kwargs = process_token(**kwargs)
        if error:
            return payload
        else:
            return func(*args, **kwargs)

    return decorated_funcion


def process_token(**kwargs):
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token = authorization_header.split('Bearer ')[1]
        return decode_token(token, **kwargs)
    else:
        return jsonify('Forbidden'), 403, None


def decode_token(token, **kwargs):
    try:
        payload = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        kwargs = get_user_id_from_token(payload, **kwargs)
    except jwt.ExpiredSignatureError:
        return jsonify('''Token expired'''), 401, None
    except jwt.InvalidSignatureError:
        return jsonify('''Signature verification failed'''), 401, None
    except Exception:
        try:
            request.get_json()
        except Exception:
            return jsonify('''The request must have a body'''), 400, None
        return jsonify('''Signature verification failed'''), 401, None
    return payload, False, kwargs


def get_user_id_from_token(payload, **kwargs):
    # When request method is not posible to add params to the request
    if request.method == 'DELETE':
        kwargs['id_obtained_from_token'] = payload['id']
    # When using GET there is no need to obtain user id
    elif request.method != 'GET':
        request.json['id'] = payload['id']
    return kwargs

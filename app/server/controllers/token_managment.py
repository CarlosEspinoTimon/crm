from flask import jsonify, request, current_app as app

import jwt


def process_token():
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token = authorization_header.split('Bearer ')[1]
        return decode_token(token)
    else:
        error = 'Forbidden, there must be a token as Authorization header'
        return jsonify(error), 403


def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        return jsonify('''Token expired'''), 401
    except jwt.InvalidSignatureError:
        return jsonify('''Signature verification failed'''), 401
    except Exception:
        return jsonify('''Signature verification failed'''), 401
    return payload, False


def get_user_id_from_token():
    payload, _ = process_token()
    return payload['id']

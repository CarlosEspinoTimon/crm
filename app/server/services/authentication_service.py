from flask import request, jsonify

from ..models.user import User

def basic_login():
    try:
        email = request.headers['email']
        password = request.headers['password']
    except KeyError:
        return jsonify('Email and password must be provided as headers'), 401

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return jsonify('Token: {}'.format(user.generate_auth_token(1800)))
    
    return jsonify('Unauthorized, wrong email or password'), 401

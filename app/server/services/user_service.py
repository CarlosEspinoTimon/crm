from datetime import datetime
from flask import jsonify
from marshmallow_sqlalchemy import ModelSchema

from server import db
from ..models.user import User, UserSchema


def all_users():
    user_schema = UserSchema(many=True)
    users = User.query.filter_by(is_deleted=False)
    response = user_schema.dump(users)
    return jsonify(response), 200


def get_a_user(user_id):
    user = User.query.get(user_id)
    if user and user.is_deleted is False:
        user_schema = UserSchema()
        response = user_schema.dump(user), 200
    else:
        response = jsonify('User not found'), 404
    return response


def create_user(data):
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        user = User(
            email=data.get('email'),
            name=data.get('name'),
            surname=data.get('surname'),
            created_at=datetime.now(),
            created_by=1,
            modified_at=datetime.now(),
            modified_by=1,
            password_hash=data.get('password')
        )
        _save_user(user)
        user_schema = UserSchema()
        response = user_schema.dump(user), 201
    else:
        response = jsonify('User already exists'), 409
    return response


def update_user(data, user_id):
    user = User.query.get(user_id)
    if user:
        fields_to_update = ['name', 'surname']
        for field in fields_to_update:
            if data.get(field):
                setattr(user, field, data[field])
        user.modified_by = 1
        user.modified_at = datetime.now()
        _save_user(user)
        response = jsonify('User sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def delete(user_id, admin_id):
    user = User.query.get(user_id)
    if user:
        user.modified_by = admin_id
        user.modified_at = datetime.now()
        user.is_deleted = True
        _save_user(user)
        response = jsonify('User deleted'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def _save_user(user):
    db.session.add(user)
    db.session.commit()

from datetime import datetime
from flask import current_app as app
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from marshmallow import Schema
from marshmallow import fields

from server import db
from server import ma


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    surname = db.Column(db.String(120), index=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    password_hash = db.Column(db.String(128))
    is_deleted = db.Column(
        db.Boolean,
        index=True,
        nullable=False,
        default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=300):
        return jwt.encode(
            {
                'id': self.id,
                'exp': time() + expiration
            },
            app.config['SECRET_KEY'], algorithm='HS256'
        ).decode('utf-8')

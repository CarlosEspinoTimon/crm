from datetime import datetime
from marshmallow import Schema, fields

from server import db, ma


class Customer(db.Model):
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    name = db.Column(db.String(120), index=True, nullable=False)
    surname = db.Column(db.String(120), index=True, nullable=False)
    photo_url = db.Column(db.String(120), index=True, nullable=True)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    last_modified_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        index=True,
        nullable=False,
        default=datetime.utcnow)
    last_modified_at = db.Column(
        db.DateTime,
        index=True,
        nullable=False,
        default=datetime.utcnow)
    is_deleted = db.Column(
        db.Boolean,
        index=True,
        nullable=False,
        default=False)


class CustomerSchema(ma.ModelSchema):

    class Meta:
        model = Customer
        include_fk = True


class PhotoSchema(Schema):
    str_image = fields.Str(required=True)
    extension = fields.Str(required=True)


class CreateCustomerSchema(Schema):
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    photo = fields.Nested(PhotoSchema, required=False)


class UpdateCustomerSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    photo = fields.Nested(PhotoSchema, required=False)

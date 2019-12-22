from datetime import datetime
from flask import jsonify

from server import db
from ..models.customer import Customer, CustomerSchema
from .image_managment import get_photo_url


def all_customers():
    customer_schema = CustomerSchema(many=True)
    customers = Customer.query.filter_by(is_deleted=False)
    response = customer_schema.dump(customers)
    return jsonify(response), 200


def get_a_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer and customer.is_deleted is False:
        customer_schema = CustomerSchema()
        response = customer_schema.dump(customer), 200
    else:
        response = jsonify('User not found'), 404
    return response


def create_customer(data):
    customer = Customer.query.filter_by(email=data['email']).first()
    if not customer:
        photo_url = get_photo_url(data)
        customer = Customer(
            email=data.get('email'),
            name=data.get('name'),
            surname=data.get('surname'),
            photo_url=photo_url,
            created_by=data.get('id'),
            last_modified_by=data.get('id'),
            created_at=datetime.now(),
            last_modified_at=datetime.now()
        )
        _save_customer(customer)
        customer_schema = CustomerSchema()
        response = customer_schema.dump(customer), 201
    else:
        response = jsonify('User already exists'), 409
    return response


def update_customer(data, customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        photo_url = get_photo_url(data)
        fields_to_update = ['name', 'surname']
        for field in fields_to_update:
            if field in data:
                setattr(customer, field, data[field])
        if photo_url:
            customer.photo_url = photo_url
        customer.last_modified_by = data.get('id')
        customer.last_modified_at = datetime.now()
        _save_customer(customer)
        response = jsonify('Customer sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def delete_a_customer(customer_id, user_id):
    customer = Customer.query.get(customer_id)
    if customer:
        customer.last_modified_by = user_id
        customer.last_modified_at = datetime.now()
        customer.is_deleted = True
        _save_customer(customer)
        response = jsonify('Customer deleted'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def _save_customer(customer):
    db.session.add(customer)
    db.session.commit()

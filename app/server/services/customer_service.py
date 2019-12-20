from datetime import datetime
from flask import jsonify

from server import db
from ..models.customer import Customer, CustomerSchema


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
        # TODO handle photo upload
        photo_url = 'fake-foto-url'
        customer = Customer(
            email=data.get('email'),
            name=data.get('name'),
            surname=data.get('surname'),
            photo_url=photo_url,
            # TODO get id from user
            created_by=1,
            # TODO get id from user
            last_modified_by=1,
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
        # TODO handle photo upload
        photo_url = 'fake-foto-url'
        fields_to_update = ['name', 'surname']
        for field in fields_to_update:
            if data.get(field):
                setattr(customer, field, data[field])
        if photo_url:
            customer.photo_url = photo_url
        # TODO get id from user
        customer.last_modified_by = 1
        customer.last_modified_at = datetime.now()
        _save_customer(customer)
        response = jsonify('Customer sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def delete(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        # TODO get id from user
        customer.last_modified_by = 1
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

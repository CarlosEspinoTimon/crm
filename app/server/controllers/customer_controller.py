from flask import Blueprint
from flask import request
from flask_cors import CORS

from ..services.customer_service import (
    all_customers,
    get_a_customer,
    create_customer,
    update_customer
)

customers = Blueprint('customers', __name__, url_prefix='/customers')
CORS(customers, max_age=30 * 86400)


@customers.route('/')
def get_all_customers():
    """
    .. http:get:: /customers/

    Function that returns all the customers.

    :returns: The Customers.
    :rtype: list.
    """
    return all_customers()


@customers.route('/<int:customer_id>')
def get_customer(customer_id):
    """
    .. http:get:: /customers/(int:customer_id)

    Function that given an id it returns the customer.

    :param customer_id: the id of the customer.
    :type customer_id: int

    :returns: The customer
    :rtype: Customer

    """
    return get_a_customer(customer_id)


@customers.route('', methods=['POST'])
def post_customer():
    """
    .. http:post:: /customers

    Function that given the customer data it creates it.

    Example::

        body = {
            'email': 'email@example.com',
            'name': 'name',
            'surname': 'surname',
            'photo': {
                'str_image': 'aXk39jacml',
                'extension': 'jpg'
            }
        }

    :param body: the data of the customer sent in the body of the request.
    :type body: dict

    """
    data = request.get_json()
    return create_customer(data)


@customers.route('/<int:customer_id>', methods=['PUT'])
def put_customer(customer_id):
    """
    .. http:put:: /customers/(int:customer_id)

    Function that given the customer_id it updates it with the data sent in the
    body of the request.

    Example::

        body = {
            'name': 'name',
            'surname': 'surname',
            'photo': {
                'str_image': 'aXk39jacml',
                'extension': 'jpg'
            }
        }

    :param customer_id: the id of the customer.
    :type customer_id: int
    :param body: the data of the customer sent in the body of the request.
    :type body: dict
    """
    data = request.get_json()
    return update_customer(data, customer_id)


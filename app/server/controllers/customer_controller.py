from flask import Blueprint
from flask_cors import CORS

from ..services.customer_service import dummy_method


customers = Blueprint('customers', __name__, url_prefix='/customers')
CORS(customers, max_age=30 * 86400)


@customers.route('/', methods=['GET'])
def dummy_endpoint():
    """
    .. http:get:: /customers/

    Dummy endpoint that calls a method from the service that says hello.

    :returns: The Customers.
    :rtype: string.
    """
    return dummy_method()
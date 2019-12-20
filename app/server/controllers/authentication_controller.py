from flask import Blueprint
from flask_cors import CORS

from ..services.authentication_service import basic_login


authentication = Blueprint('authentication', __name__, url_prefix='/login')
CORS(authentication, max_age=30 * 86400)


@authentication.route('', methods=['POST'])
def login():
    """
    .. http:post:: /login

    Function that given a email and a password as headers it checks if there
    is a user in the database and generates a token.

    :returns: The token
    :rtype: String
    
    """
    return basic_login()


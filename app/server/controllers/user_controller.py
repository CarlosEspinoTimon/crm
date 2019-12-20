from flask import Blueprint
from flask import request
from flask_cors import CORS

from ..services.user_service import (
    all_users,
    get_a_user,
    create_user,
    update_user
)

users = Blueprint('users', __name__, url_prefix='/users')
CORS(users, max_age=30 * 86400)


@users.route('/')
def get_all_users():
    """
    .. http:get:: /users/

    Function that returns all the users.

    :returns: The users.
    :rtype: list.
    """
    return all_users()


@users.route('/<int:user_id>')
def get_user(user_id):
    """
    .. http:get:: /users/(int:user_id)

    Function that given an id it returns the user.

    :param user_id: the id of the user.
    :type user_id: int

    :returns: The user
    :rtype: User

    """
    return get_a_user(user_id)


@users.route('', methods=['POST'])
def post_user():
    """
    .. http:post:: /users

    Function that given the user data it creates it.

    Example::

        body = {
            'email': 'email@example.com',
            'name': 'name',
            'surname': 'surname',
            'password': '1234'
        }

    :param body: the data of the user sent in the body of the request.
    :type body: dict

    """
    data = request.get_json()
    return create_user(data)


@users.route('/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    """
    .. http:put:: /users/(int:user_id)

    Function that given the user_id it updates it with the data sent in the
    body of the request.

    Example::

        body = {
            'name': 'name',
            'surname': 'surname',
        }

    :param user_id: the id of the user.
    :type user_id: int
    :param body: the data of the user sent in the body of the request.
    :type body: dict
    """
    data = request.get_json()
    return update_user(data, user_id)



from functools import wraps
from .token_managment import process_token

def check_user_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        payload, error = process_token()
        if error:
            return payload
        else:
            return func(*args, **kwargs)

    return decorated_funcion

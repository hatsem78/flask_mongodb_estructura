from functools import wraps
from flask import request
from flask_restplus import Namespace, Resource, marshal
from flask_jwt_extended import (get_jwt_identity, get_jwt_claims)
from models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if 'Bearer' not in request.headers.environ['HTTP_AUTHORIZATION']:
            request.headers.environ['HTTP_AUTHORIZATION'] = 'Bearer ' + \
                request.headers.environ['HTTP_AUTHORIZATION']
            return f(*args, **kwargs)
        elif len(request.headers.environ['HTTP_AUTHORIZATION'].split()) == 2:
            return f(*args, **kwargs)
        else:
            response_object = {
                'status': 'fail',
                'message': 'token required'
            }
            return response_object, 401

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(args)
        payload = get_jwt_identity()

        try:

            if not payload[0]['is_admin']:
                response_object = {
                    'status': 'fail',
                    'message': 'admin token required'
                }
                return response_object, 401

        except Exception as err:
            print(err)
            return err

        return f(*args, **kwargs)

    return decorated

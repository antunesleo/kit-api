import re
from functools import wraps

from flask_restx import Resource
from flask import Response, request


class ResourceBase(Resource):

    def __init__(self,  *args, **kwargs):
        super(ResourceBase, self).__init__( *args, **kwargs)

    @staticmethod
    def _get_files():
        return request.files

    @staticmethod
    def _return_unexpected_error():
        return {'result': 'error', 'error': 'Internal Server Error', 'exception': 'An unexpected error occurred'}, 500

    @staticmethod
    def _return_success_created():
        return {'result': 'Created'}, 201


def not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return Response('{"result": "Method not allowed"}', 405, content_type='application/json')
    return decorated_function

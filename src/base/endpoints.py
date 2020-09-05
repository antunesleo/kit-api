import re
from functools import wraps

from flask_restx import Resource
from flask import Response, request


class ResourceBase(Resource):

    def __init__(self,  *args, **kwargs):
        super(ResourceBase, self).__init__( *args, **kwargs)

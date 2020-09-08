from flask import request
from flask_restx import Resource, marshal

from src.base.serializers import CaseStyleConverter

RESPONSES_DOC = {
    200: 'OK. Standard response for successful HTTP requests. The actual response will depend on the request method used. In a GET request, the response will contain an entity corresponding to the requested resource. In a POST request, the response will contain an entity describing or containing the result of the action',
    201: 'Created. The request has been fulfilled, resulting in the creation of a new resource.',
    400: 'The server cannot or will not process the request due to an apparent client error (e.g., malformed request syntax, size too large, invalid request message framing, or deceptive request routing).',
    403: 'Forbidden. The request contained valid data and was understood by the server, but the server is refusing action. This may be due to the user not having the necessary permissions for a resource or needing an account of some sort, or attempting a prohibited action (e.g. creating a duplicate record where only one is allowed). This code is also typically used if the request provided authentication by answering the WWW-Authenticate header field challenge, but the server did not accept that authentication. The request should not be repeated.',
    404: 'Not Found. The requested resource could not be found but may be available in the future. Subsequent requests by the client are permissible.',
    405: 'Method Not Allowed. A request method is not supported for the requested resource; for example, a GET request on a form that requires data to be presented via POST, or a PUT request on a read-only resource.',
    500: 'Internal Server Error. A generic error message, given when an unexpected condition was encountered and no more specific message is suitable.'
}


def responses_doc_for(*args):
    responses_doc = {}
    for arg in args:
        try:
            responses_doc[arg] = RESPONSES_DOC[arg]
        except KeyError:
            pass

    return responses_doc


class ResourceBase(Resource):

    def __init__(self,  *args, **kwargs):
        super(ResourceBase, self).__init__( *args, **kwargs)
        self._converter = CaseStyleConverter()

    def _serialize_in(self, model):
        return self._converter.camel_to_snake(marshal(request.json, model))

from unittest import mock

from src.base.endpoints import responses_doc_for
from src.kitmanagement.domain import Product, KitProduct, Kit, CalculatedKit
from tests.unit.testbase import TestCase


class TestResponsesDocFor(TestCase):

    def test_response_doc_for(self):
        result = responses_doc_for(200, 201, 400)
        self.assertEqual(result, {
            200: 'OK. Standard response for successful HTTP requests. The actual response will depend on the request method used. In a GET request, the response will contain an entity corresponding to the requested resource. In a POST request, the response will contain an entity describing or containing the result of the action',
            201: 'Created. The request has been fulfilled, resulting in the creation of a new resource.',
            400: 'The server cannot or will not process the request due to an apparent client error (e.g., malformed request syntax, size too large, invalid request message framing, or deceptive request routing).'
        })

    def test_response_doc_for_should_ignore_any_unsupported_status_code(self):
        result = responses_doc_for(200, 201, 400, 4930493)
        self.assertEqual(result, {
            200: 'OK. Standard response for successful HTTP requests. The actual response will depend on the request method used. In a GET request, the response will contain an entity corresponding to the requested resource. In a POST request, the response will contain an entity describing or containing the result of the action',
            201: 'Created. The request has been fulfilled, resulting in the creation of a new resource.',
            400: 'The server cannot or will not process the request due to an apparent client error (e.g., malformed request syntax, size too large, invalid request message framing, or deceptive request routing).'
        })

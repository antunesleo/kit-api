from src.exceptions import NotFound
from src.kitmanagement.domain import Product
from src.web_app import get_api

from src.base.endpoints import ResourceBase
from src.kitmanagement import serializers


api = get_api()


@api.doc()
class ProductsResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(ProductsResource, self).__init__(*args, **kwargs)
        self.__products_service = kwargs['products_service']

    @api.marshal_list_with(serializers.product_model)
    @api.doc(responses={
        200: 'It works!',
        500: 'Sorry, this is my own fault.'
    })
    def get(self):
        return self.__products_service.list_products()

    @api.expect(serializers.product_creation_parser)
    @api.marshal_with(serializers.product_model, code=201)
    @api.doc(responses={
        201: 'It works!',
        400: 'Checkout the payload and query strings, bad parameter.',
        500: 'Sorry, this is my own fault.'
    })
    def post(self):
        product_creation_command = serializers.product_creation_parser.parse_args()
        product = self.__products_service.create_product(product_creation_command)
        return product, 201


class ProductResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(ProductResource, self).__init__(*args, **kwargs)
        self.__products_service = kwargs['products_service']

    @api.marshal_with(serializers.product_model)
    @api.doc(responses={
        200: 'It works!',
        500: 'Sorry, this is my own fault.'
    })
    def get(self, product_id):
        try:
            return self.__products_service.get_product(product_id)
        except NotFound:
            api.abort(404, 'Product Not Found.', product_id=product_id)

    @api.doc(responses={
        204: 'It works!',
        500: 'Sorry, this is my own fault.'
    })
    def delete(self, product_id):
        try:
            self.__products_service.remove_product(product_id)
            return {}, 204
        except NotFound:
            api.abort(404, 'Product Not Found.', product_id=product_id)


def register(products_service):
    api.add_resource(ProductResource, '/api/products/<int:product_id>', resource_class_kwargs={'products_service': products_service})
    api.add_resource(ProductsResource, '/api/products', resource_class_kwargs={'products_service': products_service})

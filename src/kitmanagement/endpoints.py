from src.web_app import get_api

from src.base.endpoints import ResourceBase, not_allowed
from src.kitmanagement import serializers


api = get_api()


@api.doc()
class ProductsResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(ProductsResource, self).__init__(*args, **kwargs)
        self.__products_service = kwargs['products_service']

    @api.marshal_list_with(serializers.product_model)
    @api.doc(responses={500: 'Sorry dude, its my fault', 400: 'Dude, what are you saying?'})
    def get(self):
        try:
            products = self.__products_service.list_products()
            return products
        except Exception:
            api.abort(400, 'My custom message', custom='value')

    @api.expect(serializers.product_creation_parser)
    def post(self):
        self.__products_service.create_item(serializers.product_creation_parser.parse_args())
        return self._return_success_created()

    @not_allowed
    def put(self):
        pass

    @not_allowed
    def delete(self):
        pass


def register(products_service):
    api.add_resource(ProductsResource, '/api/products', resource_class_kwargs={'products_service': products_service})

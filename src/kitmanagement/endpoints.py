from flask import request
from flask_restx.reqparse import ParseResult

from src.exceptions import NotFound, SKUExistsError
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
        try:
            product = self.__products_service.create_product(product_creation_command)
            return product, 201
        except SKUExistsError:
            api.abort(400, 'The product SKU is already being used by another product', SKU=product_creation_command['SKU'])


class ProductResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(ProductResource, self).__init__(*args, **kwargs)
        self.__products_service = kwargs['products_service']

    @api.marshal_with(serializers.product_model)
    @api.doc(responses={
        200: 'It works!',
        500: 'Sorry, this is my own fault.',
        404: 'The Resource doesnt exists.'
    })
    def get(self, product_id: str):
        try:
            return self.__products_service.get_product(product_id)
        except NotFound:
            api.abort(404, 'Product Not Found.', product_id=product_id)

    @api.expect(serializers.product_update_parser)
    @api.marshal_with(serializers.product_model, code=200)
    @api.doc(responses={
        200: 'It works!',
        500: 'Sorry, this is my own fault.',
        404: 'The Resource doesnt exists.'
    })
    def put(self, product_id: str):
        try:
            product_update_command = serializers.product_update_parser.parse_args()
            product = self.__products_service.update_product(product_id, product_update_command)
            return product, 200
        except NotFound:
            api.abort(404, 'Product Not Found.', product_id=product_id)

    @api.doc(responses={
        204: 'It works!',
        404: 'The Resource doesnt exists.',
        500: 'Sorry, this is my own fault.'
    })
    def delete(self, product_id: str):
        try:
            self.__products_service.remove_product(product_id)
            return {}, 204
        except NotFound:
            api.abort(404, 'Product Not Found.', product_id=product_id)


@api.doc()
class KitsResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(KitsResource, self).__init__(*args, **kwargs)
        self.__kits_service = kwargs['kits_service']

    @api.expect(api.schema_model('kit_creation_command', serializers.kit_creation_schema), validate=True)
    @api.marshal_with(serializers.kit_model, code=201)
    @api.doc(responses={
        201: 'It works!',
        400: 'Checkout the payload and query strings, bad parameter.',
        404: 'The Resource doesnt exists.',
        500: 'Sorry, this is my own fault.'
    })
    def post(self):
        kit_creation_command = serializers.kit_creation_parser.parse_args()
        kit_creation_command['kit_products'] = [
            serializers.kit_product_parser.parse_args(
                req=ParseResult(json=kit_product)
            )
            for kit_product in kit_creation_command.pop('kitProducts')
        ]

        try:
            kit = self.__kits_service.create_kit(kit_creation_command)
            return kit, 201
        except NotFound:
            api.abort(404, 'Product Not Found.')
        except SKUExistsError:
            api.abort(400, 'The kit SKU is already being used by another kit ', SKU=kit_creation_command['SKU'])

    @api.doc(responses={
        200: 'It works!',
        500: 'Sorry, this is my own fault.'
    })
    @api.marshal_list_with(serializers.kit_model, code=200)
    def get(self):
        return self.__kits_service.list_kits()


@api.doc()
class KitResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(KitResource, self).__init__(*args, **kwargs)
        self.__kits_service = kwargs['kits_service']

    @api.doc(responses={
        200: 'It works!',
        500: 'Sorry, this is my own fault.',
        404: 'The Resource doesnt exists.'
    })
    @api.marshal_with(serializers.kit_model, code=200)
    def get(self, kit_id: str):
        try:
            return self.__kits_service.get_kit(kit_id)
        except NotFound:
            api.abort(404, 'Kit Not Found.', kit_id=kit_id)

    @api.expect(api.schema_model('kit_update_command', serializers.kit_update_schema), validate=True)
    @api.marshal_with(serializers.kit_model, code=200)
    @api.doc(responses={
        200: 'It works!',
        400: 'Checkout the payload and query strings, bad parameter.',
        404: 'The Resource doesnt exists.',
        500: 'Sorry, this is my own fault.'
    })
    def put(self, kit_id: str):
        kit_update_command = serializers.kit_update_parser.parse_args()
        kit_update_command['kit_products'] = [
            serializers.kit_product_parser.parse_args(
                req=ParseResult(json=kit_product)
            )
            for kit_product in kit_update_command.pop('kitProducts')
        ]

        try:
            return self.__kits_service.update_kit(kit_id, kit_update_command)
        except NotFound:
            api.abort(404, 'Kit Not Found.', kit_id=kit_id)

    @api.doc(responses={
        204: 'It works!',
        500: 'Sorry, this is my own fault.',
        404: 'The Resource doesnt exists.'
    })
    def delete(self, kit_id: str):
        try:
            self.__kits_service.remove_kit(kit_id)
            return {}, 204
        except NotFound:
            api.abort(404, 'Kit Not Found.', kit_id=kit_id)


class CalculatedKitResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(CalculatedKitResource, self).__init__(*args, **kwargs)
        self.__calculated_kits_service = kwargs['calculated_kits_service']

    @api.doc(responses={
        200: 'It works!',
        500: 'Sorry, this is my own fault.',
        404: 'The Resource doesnt exists.'
    })
    @api.marshal_with(serializers.calculated_kit_model, code=200)
    def get(self, kit_id: str):
        try:
            return self.__calculated_kits_service.calculate_kit(kit_id)
        except NotFound:
            api.abort(404, 'Kit Not Found.', kit_id=kit_id)


def register(products_service, kits_service, calculated_kits_service):
    api.add_resource(ProductResource, '/api/products/<string:product_id>', resource_class_kwargs={'products_service': products_service})
    api.add_resource(ProductsResource, '/api/products', resource_class_kwargs={'products_service': products_service})
    api.add_resource(KitResource, '/api/kits/<string:kit_id>', resource_class_kwargs={'kits_service': kits_service})
    api.add_resource(KitsResource, '/api/kits', resource_class_kwargs={'kits_service': kits_service})
    api.add_resource(CalculatedKitResource, '/api/calculated-kits/<string:kit_id>', resource_class_kwargs={'calculated_kits_service': calculated_kits_service})

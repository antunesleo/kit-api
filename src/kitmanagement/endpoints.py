from src.exceptions import NotFound, skuExistsError, ProductInUseError
from src.web_app import get_api

from src.base.endpoints import ResourceBase, responses_doc_for
from src.kitmanagement import serialization


api = get_api()


@api.doc()
class ProductsResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(ProductsResource, self).__init__(*args, **kwargs)
        self.__products_service = kwargs['products_service']

    @api.marshal_list_with(serialization.product_model)
    @api.doc(responses=responses_doc_for(200, 500))
    def get(self):
        zas = self.__products_service.list_products()
        return self.__products_service.list_products()

    @api.expect(serialization.product_creation_command_model, validate=True)
    @api.marshal_with(serialization.product_model, code=201)
    @api.doc(responses=responses_doc_for(201, 400, 500))
    def post(self):
        product_creation_command = self._serialize_in(serialization.product_creation_command_model)
        try:
            product = self.__products_service.create_product(product_creation_command)
            return product, 201
        except skuExistsError:
            api.abort(403, 'The product sku is already being used by another product', sku=product_creation_command['sku'])


class ProductResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(ProductResource, self).__init__(*args, **kwargs)
        self.__products_service = kwargs['products_service']

    @api.marshal_with(serialization.product_model)
    @api.doc(responses=responses_doc_for(200, 403, 404, 500))
    def get(self, product_id: str):
        try:
            return self.__products_service.get_product(product_id)
        except NotFound:
            api.abort(404, 'Product Not Found.', product_id=product_id)

    @api.expect(serialization.product_update_command_model, validate=True)
    @api.marshal_with(serialization.product_model, code=200)
    @api.doc(responses=responses_doc_for(200, 404, 500))
    def put(self, product_id: str):
        try:
            product_update_command = self._serialize_in(serialization.product_update_command_model)
            product = self.__products_service.update_product(product_id, product_update_command)
            return product, 200
        except NotFound:
            api.abort(404, 'Product Not Found.', product_id=product_id)

    @api.doc(responses=responses_doc_for(204, 403, 404, 500))
    def delete(self, product_id: str):
        try:
            self.__products_service.remove_product(product_id)
            return {}, 204
        except ProductInUseError:
            api.abort(403, 'Product is being used by a kit.', product_id=product_id)
        except NotFound:
            api.abort(404, 'Product Not Found.', product_id=product_id)


@api.doc()
class KitsResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(KitsResource, self).__init__(*args, **kwargs)
        self.__kits_service = kwargs['kits_service']

    @api.expect(serialization.kit_creation_command_model, validate=True)
    @api.marshal_with(serialization.kit_model, code=201)
    @api.doc(responses=responses_doc_for(201, 400, 404, 500))
    def post(self):
        kit_creation_command = self._serialize_in(serialization.kit_creation_command_model)

        try:
            kit = self.__kits_service.create_kit(kit_creation_command)
            return kit, 201
        except NotFound:
            api.abort(404, 'Product Not Found.')
        except skuExistsError:
            api.abort(400, 'The kit sku is already being used by another kit ', sku=kit_creation_command['sku'])

    @api.doc(responses=responses_doc_for(200, 500))
    @api.marshal_list_with(serialization.kit_model, code=200)
    def get(self):
        return self.__kits_service.list_kits()


@api.doc()
class KitResource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(KitResource, self).__init__(*args, **kwargs)
        self.__kits_service = kwargs['kits_service']

    @api.doc(responses=responses_doc_for(200, 404, 500))
    @api.marshal_with(serialization.kit_model, code=200)
    def get(self, kit_id: str):
        try:
            return self.__kits_service.get_kit(kit_id)
        except NotFound:
            api.abort(404, 'Kit Not Found.', kit_id=kit_id)

    @api.expect(serialization.kit_update_command_model, validate=True)
    @api.marshal_with(serialization.kit_model, code=200)
    @api.doc(responses=responses_doc_for(200, 400, 404, 500))
    def put(self, kit_id: str):
        kit_update_command = self._serialize_in(serialization.kit_update_command_model)

        try:
            return self.__kits_service.update_kit(kit_id, kit_update_command)
        except NotFound:
            api.abort(404, 'Kit Not Found.', kit_id=kit_id)

    @api.doc(responses=responses_doc_for(204, 404, 500))
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

    @api.doc(responses=responses_doc_for(200, 404, 500))
    @api.marshal_with(serialization.calculated_kit_model, code=200)
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

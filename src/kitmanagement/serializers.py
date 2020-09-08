from copy import deepcopy

from flask_restx import fields, reqparse
from src.web_app import get_api

api = get_api()

product_model = api.model('Product', {
    'id': fields.String,
    'name': fields.String,
    'sku': fields.String,
    'cost': fields.String,
    'price': fields.String,
    'inventoryQuantity': fields.String(attribute='inventory_quantity')
})

product_creation_parser = reqparse.RequestParser()
product_creation_parser.add_argument('name', type=str, required=True, location='json')
product_creation_parser.add_argument('sku', type=str, required=True, location='json')
product_creation_parser.add_argument('cost', type=float, required=True, location='json')
product_creation_parser.add_argument('price', type=float, required=True, location='json')
product_creation_parser.add_argument('inventoryQuantity', dest='inventory_quantity', type=int, required=True, location='json')

product_update_parser = deepcopy(product_creation_parser)
product_update_parser.remove_argument('sku')

kit_product_field = api.model('KitProduct', {
    'productSku': fields.String(attribute='product_sku'),
    'quantity': fields.Integer,
    'discountPercentage': fields.Float(attribute='discount_percentage')
})

kit_model = api.model('Kit', {
    'id': fields.String,
    'name': fields.String,
    'sku': fields.String,
    'kitProducts': fields.List(fields.Nested(kit_product_field), attribute='kit_products')
})


kit_product_for_command_field = api.model('KitProductForCommandField', {
    'productSku': fields.String(required=True, attribute='productSku'),
    'quantity': fields.Integer(required=True),
    'discountPercentage': fields.Float(required=True, attribute='discountPercentage')
})

kit_creation_command_model = api.model('KitCreationCommand', {
    'name': fields.String(required=True),
    'sku': fields.String(required=True),
    'kitProducts': fields.List(fields.Nested(kit_product_for_command_field), attribute='kitProducts', required=True)
})

kit_update_command_model = api.model('KitUpdateCommand', {
    'name': fields.String(required=True),
    'kitProducts': fields.List(fields.Nested(kit_product_for_command_field), attribute='kitProducts', required=True)
})

calculated_kit_model = api.model('CalculatedKit', {
    'name': fields.String,
    'sku': fields.String,
    'cost': fields.Float,
    'price': fields.Float,
    'inventoryQuantity': fields.Integer(attribute='inventory_quantity')
})

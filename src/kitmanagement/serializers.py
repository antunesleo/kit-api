from copy import deepcopy

from flask_restx import fields, reqparse

from src.web_app import get_api

api = get_api()

product_model = api.model('Product', {
    'id': fields.Integer,
    'name': fields.String,
    'SKU': fields.String,
    'cost': fields.String,
    'price': fields.String,
    'inventoryQuantity': fields.String(attribute='inventory_quantity')
})

product_creation_parser = reqparse.RequestParser()
product_creation_parser.add_argument('name', type=str, required=True, location='json')
product_creation_parser.add_argument('SKU', type=str, required=True, location='json')
product_creation_parser.add_argument('cost', type=float, required=True, location='json')
product_creation_parser.add_argument('price', type=float, required=True, location='json')
product_creation_parser.add_argument('inventoryQuantity', dest='inventory_quantity', type=int, required=True, location='json')

product_update_parser = deepcopy(product_creation_parser)
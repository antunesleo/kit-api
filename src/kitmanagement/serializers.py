from copy import deepcopy

from flask_restx import fields, reqparse
from src.web_app import get_api

api = get_api()

product_model = api.model('Product', {
    'id': fields.String,
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
product_update_parser.remove_argument('SKU')

kit_product_field = api.model('KitProduct', {
    'productSKU': fields.String(attribute='product_SKU'),
    'quantity': fields.Integer,
    'discountPercentage': fields.Float(attribute='discount_percentage')
})

kit_model = api.model('Kit', {
    'id': fields.String,
    'name': fields.String,
    'SKU': fields.String,
    'kitProducts': fields.List(fields.Nested(kit_product_field), attribute='kit_products')
})

kit_product_parser = reqparse.RequestParser()
kit_product_parser.add_argument('productSKU', dest='product_SKU', type=str, required=True, location='json')
kit_product_parser.add_argument('quantity', type=int, required=True, location='json')
kit_product_parser.add_argument('discountPercentage', dest='discount_percentage', type=float, required=True, location='json')

kit_creation_parser = reqparse.RequestParser()
kit_creation_parser.add_argument('name', type=str, required=True, location='json')
kit_creation_parser.add_argument('SKU', type=str, required=True, location='json')
kit_creation_parser.add_argument('kitProducts', type=list, required=True, location='json')

kit_creation_schema = {
    'type': 'object',
    'properties': {
        'SKU': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        "kitProducts": {
            "type": "array",
            "items": [
                {
                    "type": "object",
                    "properties": {
                        "productSKU": {
                            "type": "string"
                        },
                        "quantity": {
                            "type": "integer"
                        },
                        "discountPercentage": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "productSKU",
                        "quantity",
                        "discountPercentage"
                    ]
                }
            ]
        }
    },
    'additionalProperties': True,
    "required": [
        "SKU",
        "name",
        "kitProducts"
    ]
}

kit_update_parser = deepcopy(kit_creation_parser)
kit_update_parser.remove_argument('SKU')
# TODO: Remove SKU from update
kit_update_schema = deepcopy(kit_creation_schema)
kit_update_schema['properties'].pop('SKU')


calculated_kit_model = api.model('CalculatedKit', {
    'name': fields.String,
    'SKU': fields.String,
    'cost': fields.Float,
    'price': fields.Float,
    'inventoryQuantity': fields.Integer(attribute='inventory_quantity')
})

from flask_restx import fields
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

product_creation_command_model = api.model('ProductCreationCommand', {
    'name': fields.String(required=True),
    'sku': fields.String(required=True),
    'cost': fields.String(required=True),
    'price': fields.String(required=True),
    'inventoryQuantity': fields.String(required=True, attribute='inventory_quantity')
})

product_update_command_model = api.model('ProductUpdateCommand', {
    'name': fields.String(required=True),
    'cost': fields.String(required=True),
    'price': fields.String(required=True),
    'inventoryQuantity': fields.String(required=True, attribute='inventory_quantity')
})


kit_product_field_out = api.model('KitProductFieldOut', {
    'productSku': fields.String(attribute='product_sku'),
    'quantity': fields.Integer,
    'discountPercentage': fields.Float(attribute='discount_percentage')
})

kit_model = api.model('Kit', {
    'id': fields.String,
    'name': fields.String,
    'sku': fields.String,
    'kitProducts': fields.List(fields.Nested(kit_product_field_out), attribute='kit_products')
})

kit_product_field_in = api.model('KitProductFieldIn', {
    'productSku': fields.String(required=True),
    'quantity': fields.Integer(required=True),
    'discountPercentage': fields.Float(required=True)
})

kit_creation_command_model = api.model('KitCreationCommand', {
    'name': fields.String(required=True),
    'sku': fields.String(required=True),
    'kitProducts': fields.List(fields.Nested(kit_product_field_in), required=True)
})

kit_update_command_model = api.model('KitUpdateCommand', {
    'name': fields.String(required=True),
    'kitProducts': fields.List(fields.Nested(kit_product_field_in), required=True)
})

calculated_kit_model = api.model('CalculatedKit', {
    'name': fields.String,
    'sku': fields.String,
    'cost': fields.Float,
    'price': fields.Float,
    'inventoryQuantity': fields.Integer(attribute='inventory_quantity')
})

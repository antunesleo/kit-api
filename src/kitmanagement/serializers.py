from flask_restx import fields, reqparse

from src.web_app import get_api


api = get_api()


product_model = api.model('Product', {
})

product_creation_parser = reqparse.RequestParser()
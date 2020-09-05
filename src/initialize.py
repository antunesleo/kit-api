# -*- coding: utf-8 -*-

from src import configurations, web_app as web_app_module
from src import connections
from src.kitmanagement import endpoints as kitmanagement_endpoints
from src.kitmanagement.application_services import ProductsService
from src.kitmanagement.repositories import InMemoryProductRepository

config = configurations.get_config()
web_app = web_app_module.get_web_app()
api = web_app_module.get_api()

connections.register(web_app)
elasticsearch_connection = connections.example2_elastic_search_connection

in_memory_product_repository = InMemoryProductRepository()
products_service = ProductsService(in_memory_product_repository)
kitmanagement_endpoints.register(products_service=products_service)

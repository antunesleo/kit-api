# -*- coding: utf-8 -*-

from src import configurations, web_app as web_app_module
from src import connections
from src.kitmanagement import endpoints as kitmanagement_endpoints
from src.kitmanagement.application_services import ProductsService, KitsService, CalculatedKitsService
from src.kitmanagement.repositories import InMemoryProductRepository, InMemoryKitRepository, MongoProductRepository

config = configurations.get_config()
web_app = web_app_module.get_web_app()
api = web_app_module.get_api()

connections.register(web_app)

mongo_product_repository = MongoProductRepository(connections.mongo_kit_db)
in_memory_product_repository = InMemoryProductRepository()
products_service = ProductsService(mongo_product_repository)
in_memory_kit_repository = InMemoryKitRepository()
kits_service = KitsService(in_memory_kit_repository, in_memory_product_repository)
calculated_kits_service = CalculatedKitsService(in_memory_kit_repository, in_memory_product_repository)
kitmanagement_endpoints.register(
    products_service=products_service,
    kits_service=kits_service,
    calculated_kits_service=calculated_kits_service
)

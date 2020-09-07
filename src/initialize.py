# -*- coding: utf-8 -*-

from src import configurations, web_app as web_app_module
from src import connections
from src.kitmanagement import endpoints as kitmanagement_endpoints
from src.kitmanagement.application_services import ProductsService, KitsService, CalculatedKitsService
from src.kitmanagement.repositories import InMemoryProductRepository, InMemoryKitRepository, MongoProductRepository, MongoKitRepository

config = configurations.get_config()
web_app = web_app_module.get_web_app()
api = web_app_module.get_api()

connections.register(web_app)

# INFO: If you dont like databases, just use an inmemory repository
# product_repository = InMemoryProductRepository()
# kit_repository = InMemoryKitRepository()

product_repository = MongoProductRepository(connections.mongo_kit_db)
kit_repository = MongoKitRepository(connections.mongo_kit_db)

products_service = ProductsService(product_repository)
kits_service = KitsService(kit_repository, product_repository)
calculated_kits_service = CalculatedKitsService(kit_repository, product_repository)

kitmanagement_endpoints.register(
    products_service=products_service,
    kits_service=kits_service,
    calculated_kits_service=calculated_kits_service
)

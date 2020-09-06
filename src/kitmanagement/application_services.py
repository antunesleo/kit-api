from typing import List
from src.base.application_services import ApplicationService
from src.kitmanagement.domain import Product, Kit, KitProduct, ProductRepository, KitRepository


class ProductsService(ApplicationService):

    def __init__(self, repository: ProductRepository):
        self.__repository = repository

    def create_product(self, product_creation_command: dict) -> Product:
        product = Product(**product_creation_command)
        product_id = self.__repository.add(product)
        product.define_id(product_id)
        return product

    def list_products(self) -> List[Product]:
        return self.__repository.list()

    def get_product(self, product_id: int) -> Product:
        return self.__repository.get_by_id(product_id)

    def remove_product(self, product_id: int):
        self.__repository.remove(product_id)

    def update_product(self, product_id: int, product_update_command: dict) -> Product:
        product = self.__repository.get_by_id(product_id)
        product.update_infos(**product_update_command)
        self.__repository.update(product)
        return product


class KitsService(ApplicationService):

    def __init__(self, repository: KitRepository):
        self.__repository = repository

    def create_kit(self, kit_creation_command: dict) -> Kit:
        kit_products = [KitProduct(**kit_product) for kit_product in kit_creation_command.pop('kit_products')]
        kit = Kit(**kit_creation_command, kit_products=kit_products)
        kit_id = self.__repository.add(kit)
        kit.define_id(kit_id)
        return kit

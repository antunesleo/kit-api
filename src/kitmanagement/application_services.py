from typing import List
from src.base.application_services import ApplicationService
from src.kitmanagement.domain import Product, ProductRepository


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

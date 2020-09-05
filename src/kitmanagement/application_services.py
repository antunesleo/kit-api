from typing import List
from src.base.application_services import ApplicationService
from src.kitmanagement.domain import Product, ProductRepository


class ProductsService(ApplicationService):

    def __init__(self, repository: ProductRepository):
        self.__repository = repository

    def create_product(self, product_creation_command: dict) -> None:
        item = Product(**product_creation_command)
        self.__repository.add(item)

    def list_items(self) -> List[Product]:
        return self.__repository.list()

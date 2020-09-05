from typing import List

from src.kitmanagement.domain import ProductRepository, Product


class InMemoryProductRepository(ProductRepository):

    def __init__(self):
        self.__products = []

    def add(self, product: Product) -> None:
        self.__products.append(product)

    def list(self, for_read=True) -> List[Product]:
        return self.__products

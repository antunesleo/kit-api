from copy import deepcopy
from typing import List
from src.exceptions import NotFound
from src.kitmanagement.domain import ProductRepository, Product


class InMemoryProductRepository(ProductRepository):

    def __init__(self):
        self.__products : List[Product] = []

    def add(self, product: Product) -> int:
        product = deepcopy(product)
        product.define_id(self.__next_id())
        self.__products.append(product)
        return product.id

    def list(self, for_read=True) -> List[Product]:
        return self.__products

    def get_by_id(self, product_id) -> Product:
        for product in self.__products:
            if product.id == product_id:
                return product
        raise NotFound(f'product id: {product_id} not found')

    def remove(self, product_id) -> None:
        index_to_remove = None

        for index, product in enumerate(self.__products):
            if product.id == product_id:
                index_to_remove = index
                break

        if index_to_remove is None:
            raise NotFound(f'product id: {product_id} not found')

        self.__products.pop(index_to_remove)

    def update(self, product_to_update: Product) -> None:
        index_to_remove = None

        for index, product in enumerate(self.__products):
            if product.id == product_to_update.id:
                index_to_remove = index
                break

        if index_to_remove is None:
            raise NotFound(f'product id: {product_to_update.id} not found')

        self.__products[index_to_remove] = product_to_update

    def __next_id(self) -> int:
        try:
            return max(self.__products, key=lambda p: p.id).id + 1
        except ValueError:
            return 1

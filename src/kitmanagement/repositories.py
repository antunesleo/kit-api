from copy import deepcopy
from typing import List
from src.exceptions import NotFound
from src.kitmanagement.domain import ProductRepository, KitRepository, Kit, Product


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
        index_to_update = None

        for index, product in enumerate(self.__products):
            if product.id == product_to_update.id:
                index_to_update = index
                break

        if index_to_update is None:
            raise NotFound(f'product id: {product_to_update.id} not found')

        self.__products[index_to_update] = product_to_update

    def __next_id(self) -> int:
        try:
            return max(self.__products, key=lambda p: p.id).id + 1
        except ValueError:
            return 1


class InMemoryKitRepository(KitRepository):

    def __init__(self):
        self.__kits : List[Kit] = []

    def add(self, kit: Kit) -> int:
        kit = deepcopy(kit)
        kit.define_id(self.__next_id())
        self.__kits.append(kit)
        return kit.id

    def list(self, for_read=True) -> List[Kit]:
        return self.__kits

    def get_by_id(self, kit_id) -> Kit:
        for kit in self.__kits:
            if kit.id == kit_id:
                return kit
        raise NotFound(f'product id: {kit_id} not found')

    def remove(self, kit_id) -> None:
        index_to_remove = None

        for index, kid in enumerate(self.__kits):
            if kid.id == kit_id:
                index_to_remove = index
                break

        if index_to_remove is None:
            raise NotFound(f'kit id: {kit_id} not found')

        self.__kits.pop(index_to_remove)

    def update(self, kit_to_update: Kit) -> None:
        index_to_update = None

        for index, kit in enumerate(self.__kits):
            if kit.id == kit_to_update.id:
                index_to_update = index
                break

        if index_to_update is None:
            raise NotFound(f'product id: {kit_to_update.id} not found')

        self.__kits[index_to_update] = kit_to_update

    def __next_id(self) -> int:
        try:
            return max(self.__kits, key=lambda k: k.id).id + 1
        except ValueError:
            return 1

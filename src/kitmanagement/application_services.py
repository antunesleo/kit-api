from copy import deepcopy
from typing import List
from src.base.application_services import ApplicationService
from src.kitmanagement.domain import Product, Kit, KitProduct, ProductRepository, KitRepository, CalculatedKit


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

    def remove_product(self, product_id: int) -> None:
        self.__repository.remove(product_id)

    def update_product(self, product_id: int, product_update_command: dict) -> Product:
        product = self.__repository.get_by_id(product_id)
        product.update_infos(**product_update_command)
        self.__repository.update(product)
        return product


class KitsService(ApplicationService):

    def __init__(self, kit_repository: KitRepository, product_repository: ProductRepository):
        self.__kit_repository = kit_repository
        self.__product_repository = product_repository

    def create_kit(self, kit_creation_command: dict) -> Kit:
        kit_products = []
        for kit_product_dict in kit_creation_command.pop('kit_products'):
            self.__product_repository.get_by_SKU(kit_product_dict['product_SKU'])
            kit_products.append(KitProduct(**kit_product_dict))

        kit = Kit(**kit_creation_command, kit_products=kit_products)
        kit_id = self.__kit_repository.add(kit)
        kit.define_id(kit_id)
        return kit

    def list_kits(self) -> List[Kit]:
        return self.__kit_repository.list()

    def get_kit(self, kit_id: int) -> Kit:
        return self.__kit_repository.get_by_id(kit_id)

    def update_kit(self, kit_id: int, kit_update_command: dict) -> Kit:
        kit_update_command = deepcopy(kit_update_command)
        kit = self.__kit_repository.get_by_id(kit_id)

        kit_products = []
        for kit_product_dict in kit_update_command.pop('kit_products'):
            self.__product_repository.get_by_SKU(kit_product_dict['product_SKU'])
            kit_products.append(KitProduct(**kit_product_dict))

        kit.update_infos(**kit_update_command, kit_products=kit_products)
        self.__kit_repository.update(kit)
        return kit

    def remove_kit(self, kit_id) -> None:
        self.__kit_repository.remove(kit_id)


class CalculatedKitsService(ApplicationService):

    def __init__(self, kit_repository: KitRepository, product_repository: ProductRepository):
        self.__kit_repository = kit_repository
        self.__product_repository = product_repository

    def calculate_kit(self, kit_id: int) -> CalculatedKit:
        kit = self.__kit_repository.get_by_id(kit_id)
        products = self.__product_repository.list_with_SKUs([
            kit_product.product_SKU
            for kit_product in kit.kit_products
        ])
        return CalculatedKit(kit, products)

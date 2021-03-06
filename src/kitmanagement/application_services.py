from copy import deepcopy
from typing import List
from src.base.application_services import ApplicationService
from src.exceptions import ProductInUseError
from src.kitmanagement.domain import Product, Kit, KitProduct, ProductRepository, KitRepository, CalculatedKit


class ProductsService(ApplicationService):

    def __init__(self, product_repository: ProductRepository, kit_repository: KitRepository):
        self.__product_repository = product_repository
        self.__kit_repository = kit_repository

    def create_product(self, product_creation_command: dict) -> Product:
        product = Product(**product_creation_command)
        product_id = self.__product_repository.add(product)
        product.define_id(product_id)
        return product

    def list_products(self) -> List[Product]:
        return self.__product_repository.list()

    def get_product(self, product_id: str) -> Product:
        return self.__product_repository.get_by_id(product_id)

    def remove_product(self, product_id: str) -> None:
        product = self.__product_repository.get_by_id(product_id)
        kits_using_product = self.__kit_repository.list_with_product(product.sku)
        if kits_using_product:
            raise ProductInUseError('products being used by kits cant be removed')
        self.__product_repository.remove(product_id)

    def update_product(self, product_id: str, product_update_command: dict) -> Product:
        product = self.__product_repository.get_by_id(product_id)
        product.update_infos(**product_update_command)
        self.__product_repository.update(product)
        return product


class KitsService(ApplicationService):

    def __init__(self, kit_repository: KitRepository, product_repository: ProductRepository):
        self.__kit_repository = kit_repository
        self.__product_repository = product_repository

    def create_kit(self, kit_creation_command: dict) -> Kit:
        kit_products = []
        for kit_product_dict in kit_creation_command.pop('kit_products'):
            self.__product_repository.get_by_sku(kit_product_dict['product_sku'])
            kit_products.append(KitProduct(**kit_product_dict))

        kit = Kit(**kit_creation_command, kit_products=kit_products)
        kit_id = self.__kit_repository.add(kit)
        kit.define_id(kit_id)
        return kit

    def list_kits(self) -> List[Kit]:
        return self.__kit_repository.list()

    def get_kit(self, kit_id: str) -> Kit:
        return self.__kit_repository.get_by_id(kit_id)

    def update_kit(self, kit_id: str, kit_update_command: dict) -> Kit:
        kit_update_command = deepcopy(kit_update_command)
        kit = self.__kit_repository.get_by_id(kit_id)

        kit_products = []
        for kit_product_dict in kit_update_command.pop('kit_products'):
            self.__product_repository.get_by_sku(kit_product_dict['product_sku'])
            kit_products.append(KitProduct(**kit_product_dict))

        kit.update_infos(**kit_update_command, kit_products=kit_products)
        self.__kit_repository.update(kit)
        return kit

    def remove_kit(self, kit_id: str) -> None:
        self.__kit_repository.remove(kit_id)


class CalculatedKitsService(ApplicationService):

    def __init__(self, kit_repository: KitRepository, product_repository: ProductRepository):
        self.__kit_repository = kit_repository
        self.__product_repository = product_repository

    def calculate_kit(self, kit_id: str) -> CalculatedKit:
        kit = self.__kit_repository.get_by_id(kit_id)
        products = self.__product_repository.list_with_skus([
            kit_product.product_sku
            for kit_product in kit.kit_products
        ])
        return CalculatedKit(kit, products)

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from src.exceptions import IdAlreadyDefined
from src.base.domain import AggregateRoot, ValueObject


class Product(AggregateRoot):

    def __init__(self, name: str, sku: str, cost: float, price: float, inventory_quantity: int, id: str=None):
        self.__id = id
        self.__name = name
        self.__sku = sku
        self.__cost = cost
        self.__price = price
        self.__inventory_quantity = inventory_quantity

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def sku(self) -> str:
        return self.__sku

    @property
    def cost(self) -> float:
        return self.__cost

    @property
    def price(self) -> float:
        return self.__price

    @property
    def inventory_quantity(self) -> int:
        return self.__inventory_quantity

    def define_id(self, product_id: str) -> None:
        if self.__id:
            raise IdAlreadyDefined
        self.__id = product_id

    def update_infos(self, name: str, cost: float, price: float, inventory_quantity: int):
        self.__name = name
        self.__cost = cost
        self.__price = price
        self.__inventory_quantity = inventory_quantity


@dataclass(frozen=True)
class KitProduct(ValueObject):
    product_sku: str
    quantity: int
    discount_percentage: float


class Kit(AggregateRoot):

    def __init__(self, name: str, sku: str, kit_products: List[KitProduct], id: str=None):
        self.__id = id
        self.__name = name
        self.__sku = sku
        self.__kit_products = kit_products

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def sku(self) -> str:
        return self.__sku

    @property
    def kit_products(self) -> List[KitProduct]:
        return self.__kit_products

    def define_id(self, product_id: str) -> None:
        if self.__id:
            raise IdAlreadyDefined
        self.__id = product_id

    def update_infos(self, name: str, kit_products: List[KitProduct]):
        self.__name = name
        self.__kit_products = kit_products


class CalculatedKit:

    def __init__(self, kit: Kit, products: List[Product]):
        self.__kit = kit
        self.__products = products

    @property
    def name(self):
        return self.__kit.name

    @property
    def sku(self):
        return self.__kit.sku

    @property
    def inventory_quantity(self) -> int:
        inventory_quantity = None

        for kit_product in self.__kit.kit_products:
            product = self.__get_product_with(kit_product.product_sku)
            kit_product_inventory_quantity = int(product.inventory_quantity / kit_product.quantity)

            if not inventory_quantity:
                inventory_quantity = kit_product_inventory_quantity
                break

            if kit_product_inventory_quantity < inventory_quantity:
                inventory_quantity = kit_product_inventory_quantity

        return inventory_quantity

    @property
    def cost(self) -> float:
        cost = 0.0

        for kit_product in self.__kit.kit_products:
            product = self.__get_product_with(kit_product.product_sku)
            cost += product.cost * kit_product.quantity

        return cost

    @property
    def price(self):
        price = 0.0

        for kit_product in self.__kit.kit_products:
            product = self.__get_product_with(kit_product.product_sku)
            kit_product_price = self.__apply_discount(product.price * kit_product.quantity, kit_product.discount_percentage)
            price += kit_product_price

        return price

    def __get_product_with(self, sku: str) -> Product:
        for product in self.__products:
            if sku == product.sku:
                return product
        raise ValueError('Must have one product for each kit.kit_product')

    def __apply_discount(self, price, discount_percentage):
        return price - (price / 100 * discount_percentage)


class ProductRepository(ABC):

    @abstractmethod
    def list(self) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def list_with_skus(self, skus: List[str]) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def add(self, product: Product) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, product_id: str) -> Product:
        raise NotImplementedError

    @abstractmethod
    def get_by_sku(self, sku: str) -> Product:
        raise NotImplementedError

    @abstractmethod
    def remove(self, product_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, product: Product) -> None:
        raise NotImplementedError


class KitRepository(ABC):

    @abstractmethod
    def list(self) -> List[Kit]:
        raise NotImplementedError

    @abstractmethod
    def list_with_product(self, product_sku: str) -> List[Kit]:
        raise NotImplementedError

    @abstractmethod
    def add(self, kit: Kit) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, kit_id: str) -> Kit:
        raise NotImplementedError

    @abstractmethod
    def remove(self, kit_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, kit: Kit) -> None:
        raise NotImplementedError

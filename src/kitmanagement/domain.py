from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union

from src.exceptions import IdAlreadyDefined
from src.base.domain import AggregateRoot, ValueObject


class Product(AggregateRoot):

    def __init__(self, name: str, SKU: str, cost: float, price: float, inventory_quantity: int, id: int=None):
        self.__id = id
        self.__name = name
        self.__SKU = SKU
        self.__cost = cost
        self.__price = price
        self.__inventory_quantity = inventory_quantity

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def SKU(self) -> str:
        return self.__SKU

    @property
    def cost(self) -> float:
        return self.__cost

    @property
    def price(self) -> float:
        return self.__price

    @property
    def inventory_quantity(self) -> int:
        return self.__inventory_quantity

    def define_id(self, product_id: int) -> None:
        if self.__id:
            raise IdAlreadyDefined
        self.__id = product_id

    def update_infos(self, name: str, SKU: str, cost: float, price: float, inventory_quantity: int):
        self.__name = name
        self.__SKU = SKU
        self.__cost = cost
        self.__price = price
        self.__inventory_quantity = inventory_quantity


@dataclass(frozen=True)
class KitProduct(ValueObject):
    product_SKU: str
    quantity: int
    discount_percentage: float


class Kit(AggregateRoot):

    def __init__(self, name: str, SKU: str, kit_products: List[KitProduct], id: int=None):
        self.__id = id
        self.__name = name
        self.__SKU = SKU
        self.__kit_products = kit_products

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def SKU(self) -> str:
        return self.__SKU

    @property
    def kit_products(self) -> List[KitProduct]:
        return self.__kit_products

    def define_id(self, product_id: int) -> None:
        if self.__id:
            raise IdAlreadyDefined
        self.__id = product_id

    def update_infos(self, name: str, SKU: str, kit_products: List[KitProduct]):
        self.__name = name
        self.__SKU = SKU
        self.__kit_products = kit_products


class CalculatedKit:

    def __init__(self, kit: Kit, products: List[Product]):
        self.__kit = kit
        self.__products = products

    @property
    def name(self):
        return self.__kit.name

    @property
    def SKU(self):
        return self.__kit.SKU

    @property
    def inventory_quantity(self) -> int:
        inventory_quantity = None

        for kit_product in self.__kit.kit_products:
            product = self.__get_product_with(kit_product.product_SKU)
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
            product = self.__get_product_with(kit_product.product_SKU)
            cost += product.cost * kit_product.quantity

        return cost

    @property
    def price(self):
        price = 0.0

        for kit_product in self.__kit.kit_products:
            product = self.__get_product_with(kit_product.product_SKU)
            kit_product_price = self.__apply_discount(product.price * kit_product.quantity, kit_product.discount_percentage)
            price += kit_product_price

        return price

    def __get_product_with(self, SKU: str) -> Product:
        for product in self.__products:
            if SKU == product.SKU:
                return product
        raise ValueError('Must have one product for each kit.kit_product')

    def __apply_discount(self, price, discount_percentage):
        return price - (price / 100 * discount_percentage)


class ProductRepository(ABC):

    @abstractmethod
    def list(self) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def list_with_SKUs(self, SKUs: List[str]) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def add(self, product: Product) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product:
        raise NotImplementedError

    @abstractmethod
    def remove(self, product_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, product: Product) -> None:
        raise NotImplementedError


class KitRepository(ABC):

    @abstractmethod
    def list(self) -> List[Kit]:
        raise NotImplementedError

    @abstractmethod
    def add(self, kit: Kit) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, kit_id: int) -> Kit:
        raise NotImplementedError

    @abstractmethod
    def remove(self, kit_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, kit: Kit) -> None:
        raise NotImplementedError

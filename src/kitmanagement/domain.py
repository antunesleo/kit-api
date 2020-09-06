from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

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


class ProductRepository(ABC):

    @abstractmethod
    def list(self) -> List[Product]:
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

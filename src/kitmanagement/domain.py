from abc import ABC, abstractmethod
from typing import List

from src.exceptions import IdAlreadyDefined
from src.base.domain import AggregateRoot


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


class ProductRepository(ABC):

    @abstractmethod
    def list(self) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def add(self, question: Product) -> int:
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

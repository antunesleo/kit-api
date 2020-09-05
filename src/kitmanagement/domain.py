from abc import ABC, abstractmethod
from typing import List

from src.base.domain import AggregateRoot


class Product(AggregateRoot):

    def __init__(self, name: str, SKU: str, cost: float, price: float, inventory_quantity: int):
        self.__name = name
        self.__SKU = SKU
        self.__cost = cost
        self.__price = price
        self.__inventory_quantity = inventory_quantity

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



class ProductRepository(ABC):

    @abstractmethod
    def list(self, for_read=True) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def add(self, question: Product) -> None:
        raise NotImplementedError

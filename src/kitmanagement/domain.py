from abc import ABC, abstractmethod
from typing import List

from src.base.domain import AggregateRoot


class Product(AggregateRoot):

    def __init__(self):
        pass


class ProductRepository(ABC):

    @abstractmethod
    def list(self, for_read=True) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def add(self, question: Product) -> None:
        raise NotImplementedError

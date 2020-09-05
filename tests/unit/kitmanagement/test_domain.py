from unittest import mock

from src.kitmanagement.domain import Product
from tests.unit.base import TestCase


class TestProduct(TestCase):

    def test_product_initialization_should_have_all_fields(self):
        product = Product(
            name='The Last of Us Part II',
            SKU='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        self.assertEqual(product.name, 'The Last of Us Part II')
        self.assertEqual(product.SKU, 'AHJU-49685')
        self.assertEqual(product.cost, 10.00)
        self.assertEqual(product.price, 220.00)
        self.assertEqual(product.inventory_quantity, 150)

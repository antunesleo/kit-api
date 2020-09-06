from unittest import mock

from src.kitmanagement.domain import Product, KitProduct, Kit
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

    def test_product_initialization_should_have_an_id(self):
        product = Product(
            id=1,
            name='The Last of Us Part II',
            SKU='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        self.assertEqual(product.id, 1)

    def test_should_update_infos(self):
        product = Product(
            id=1,
            name='Last of Us Part II',
            SKU='AHJU-4968',
            cost=2.00,
            price=100.00,
            inventory_quantity=100
        )
        product.update_infos(
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


class TestProductKit(TestCase):

    def test_product_kit_initialization_should_have_all_fields(self):
        kit_product = KitProduct(
            product_SKU='FASD-498',
            quantity=2,
            discount_percentage=10.5
        )
        self.assertEqual(kit_product.product_SKU, 'FASD-498')
        self.assertEqual(kit_product.quantity, 2)
        self.assertEqual(kit_product.discount_percentage, 10.5)


class TestKit(TestCase):

    def test_kit_initialization_shoul_have_all_fields(self):
        kit_products = [
            KitProduct(
                product_SKU='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_SKU='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            SKU='FASD-789',
            kit_products=kit_products
        )
        self.assertEqual(kit.name, 'Sony Gaming Pack')
        self.assertEqual(kit.SKU, 'FASD-789')
        self.assertEqual(kit.kit_products, kit_products)

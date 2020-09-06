from unittest import mock

from src.kitmanagement.domain import Product, KitProduct, Kit, CalculatedKit
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

    def test_product_kit_initialization(self):
        kit_product = KitProduct(
            product_SKU='FASD-498',
            quantity=2,
            discount_percentage=10.5
        )
        self.assertEqual(kit_product.product_SKU, 'FASD-498')
        self.assertEqual(kit_product.quantity, 2)
        self.assertEqual(kit_product.discount_percentage, 10.5)


class TestKit(TestCase):

    def test_kit_initialization(self):
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

    def test_should_update_infos(self):
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

        updated_kit_products = [
            KitProduct(
                product_SKU='FASD-4918',
                quantity=7,
                discount_percentage=20.5
            ),
            KitProduct(
                product_SKU='FASD-14289',
                quantity=7,
                discount_percentage=32.5
            )
        ]
        kit.update_infos(
            name='Sony Gaming Pack I',
            SKU='AHJU-49685',
            kit_products=updated_kit_products
        )

        self.assertEqual(kit.name, 'Sony Gaming Pack I')
        self.assertEqual(kit.SKU, 'AHJU-49685')
        self.assertEqual(kit.kit_products[0], updated_kit_products[0])
        self.assertEqual(kit.kit_products[1], updated_kit_products[1])


class TestCalculatedKit(TestCase):

    def setUp(self) -> None:
        product_A_mock = mock.MagicMock()
        product_A_mock.inventory_quantity = 10
        product_A_mock.cost = 20.00
        product_A_mock.SKU = 'A'
        product_B_mock = mock.MagicMock()
        product_B_mock.inventory_quantity = 50
        product_B_mock.cost = 10.00
        product_B_mock.SKU = 'B'
        product_C_mock = mock.MagicMock()
        product_C_mock.cost = 15.00
        product_C_mock.inventory_quantity = 38
        product_C_mock.SKU = 'C'
        self.products_mock = [
            product_A_mock,
            product_B_mock,
            product_C_mock
        ]

        kit_product_A_mock = mock.MagicMock()
        kit_product_A_mock.quantity = 2
        kit_product_A_mock.product_SKU = 'A'
        kit_product_B_mock = mock.MagicMock()
        kit_product_B_mock.quantity = 1
        kit_product_B_mock.product_SKU = 'B'
        kit_product_C_mock = mock.MagicMock()
        kit_product_C_mock.quantity = 5
        kit_product_C_mock.product_SKU = 'C'
        kit_products_mock = [
            kit_product_A_mock,
            kit_product_B_mock,
            kit_product_C_mock
        ]
        self.kit_mock = mock.MagicMock()
        self.kit_mock.kit_products = kit_products_mock

    def test_calculated_kit_initialization(self):
        kit_mock = mock.MagicMock()
        products_mock = mock.MagicMock()
        calculated_kit = CalculatedKit(
            kit=kit_mock,
            products=products_mock
        )
        self.assertIsInstance(calculated_kit, CalculatedKit)

    def test_calculate_kit_inventory_quantity(self):
        calculated_kit = CalculatedKit(self.kit_mock, self.products_mock)
        self.assertEqual(calculated_kit.inventory_quantity, 5)

    def test_cost(self):
        calculated_kit = CalculatedKit(self.kit_mock, self.products_mock)
        self.assertEqual(calculated_kit.cost, 125.00)

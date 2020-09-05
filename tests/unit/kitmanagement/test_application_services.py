from unittest import mock

from src.kitmanagement.application_services import ProductsService
from tests.unit.base import TestCase


class TestProductsService(TestCase):

    def test_create_product(self,):
        repository_mock = mock.MagicMock()
        service = ProductsService(repository_mock)
        product_creation_command = {
            'name': 'The Last of Us Part II',
            'SKU': 'AHJU-49685',
            'cost': 10.00,
            'price': 220.00,
            'inventory_quantity': 150
        }
        service.create_product(product_creation_command)

        repository_mock.add.assert_called()
        product = repository_mock.add.mock_calls[0].args[0]
        self.assertEqual(product.name, 'The Last of Us Part II')
        self.assertEqual(product.SKU, 'AHJU-49685')
        self.assertEqual(product.cost, 10.00)
        self.assertEqual(product.price, 220.00)
        self.assertEqual(product.inventory_quantity, 150)

    def test_list_products(self):
        products_mock = mock.MagicMock()
        repository_mock = mock.MagicMock()
        repository_mock.list.return_value = products_mock
        service = ProductsService(repository_mock)
        products = service.list_products()
        repository_mock.list.assert_called()
        self.assertEqual(products_mock, products)

    def test_get_by_id(self):
        product_mock = mock.MagicMock()
        repository_mock = mock.MagicMock()
        repository_mock.get_by_id.return_value = product_mock
        service = ProductsService(repository_mock)
        product = service.get_product_by_id(1)
        repository_mock.get_by_id.assert_called_with(1)
        self.assertEqual(product_mock, product)

from unittest import mock

from src.exceptions import ProductInUseError
from src.kitmanagement.application_services import ProductsService, KitsService, CalculatedKitsService
from src.kitmanagement.domain import Kit, KitProduct, CalculatedKit
from tests.unit.testbase import TestCase


class TestProductsService(TestCase):

    def test_create_product(self,):
        kit_repository_mock = mock.MagicMock()
        repository_mock = mock.MagicMock()
        service = ProductsService(repository_mock, kit_repository_mock)
        product_creation_command = {
            'name': 'The Last of Us Part II',
            'sku': 'AHJU-49685',
            'cost': 10.00,
            'price': 220.00,
            'inventory_quantity': 150
        }
        service.create_product(product_creation_command)

        repository_mock.add.assert_called()
        product = repository_mock.add.mock_calls[0].args[0]
        self.assertEqual(product.name, 'The Last of Us Part II')
        self.assertEqual(product.sku, 'AHJU-49685')
        self.assertEqual(product.cost, 10.00)
        self.assertEqual(product.price, 220.00)
        self.assertEqual(product.inventory_quantity, 150)

    def test_list_products(self):
        kit_repository_mock = mock.MagicMock()
        products_mock = mock.MagicMock()
        repository_mock = mock.MagicMock()
        repository_mock.list.return_value = products_mock
        service = ProductsService(repository_mock, kit_repository_mock)
        products = service.list_products()
        repository_mock.list.assert_called()
        self.assertEqual(products_mock, products)

    def test_get_product(self):
        kit_repository_mock = mock.MagicMock()
        product_mock = mock.MagicMock()
        repository_mock = mock.MagicMock()
        repository_mock.get_by_id.return_value = product_mock
        service = ProductsService(repository_mock, kit_repository_mock)
        product = service.get_product(1)
        repository_mock.get_by_id.assert_called_with(1)
        self.assertEqual(product_mock, product)

    def test_remove_product(self):
        kit_repository_mock = mock.MagicMock()
        kit_repository_mock.list_with_product.return_value = []

        product_mock = mock.MagicMock(sku='FASD-1')
        product_repository_mock = mock.MagicMock()
        product_repository_mock.get_by_id.return_value = product_mock

        service = ProductsService(product_repository_mock, kit_repository_mock)
        service.remove_product(1)
        product_repository_mock.remove.assert_called_with(1)
        kit_repository_mock.list_with_product.assert_called_with('FASD-1')

    def test_remove_product_should_raise_product_in_use_error_when_product_is_being_used_by_any_kit(self):
        kit_repository_mock = mock.MagicMock()
        kit_repository_mock.list_with_product.return_value = [mock.MagicMock()]

        product_mock = mock.MagicMock(sku='FASD-1')
        product_repository_mock = mock.MagicMock()
        product_repository_mock.get_by_id.return_value = product_mock

        service = ProductsService(product_repository_mock, kit_repository_mock)
        with self.assertRaises(ProductInUseError):
            service.remove_product(1)

        product_repository_mock.remove.assert_not_called()
        kit_repository_mock.list_with_product.assert_called_with('FASD-1')

    def test_update_product(self):
        kit_repository_mock = mock.MagicMock()
        product_update_command = {
            'name': 'The Last of Us Part II',
            'sku': 'AHJU-49685',
            'cost': 10.00,
            'price': 220.00,
            'inventory_quantity': 150
        }
        product_mock = mock.MagicMock()
        repository_mock = mock.MagicMock()
        repository_mock.get_by_id.return_value = product_mock

        service = ProductsService(repository_mock, kit_repository_mock)
        updated_product = service.update_product(1, product_update_command)

        self.assertEqual(updated_product, product_mock)
        repository_mock.get_by_id.assert_called_with(1)
        product_mock.update_infos.assert_called_with(**product_update_command)
        repository_mock.update.assert_called_with(product_mock)


class TestKitService(TestCase):

    def test_create_kit(self):
        kit_creation_command = {
            'sku': 'FASF-123',
            'name': 'Sony Pack I',
            'kit_products': [
                {
                    'product_sku': 'AHJU-49685',
                    'quantity': 1,
                    'discount_percentage': 10
                },
                {
                    'product_sku': 'AHJU-49621',
                    'quantity': 2,
                    'discount_percentage': 15
                }
            ]
        }
        kit_repository_mock = mock.MagicMock()
        product_repository_mock = mock.MagicMock()
        service = KitsService(kit_repository_mock, product_repository_mock)
        returned_kit = service.create_kit(kit_creation_command)

        created_kit = kit_repository_mock.add.mock_calls[0].args[0]
        self.assertIsInstance(returned_kit, Kit)
        self.assertEqual(created_kit.sku, 'FASF-123')
        self.assertEqual(created_kit.name, 'Sony Pack I')
        self.assertIsInstance(created_kit.kit_products[0], KitProduct)
        self.assertEqual(created_kit.kit_products[0].product_sku, 'AHJU-49685')
        self.assertEqual(created_kit.kit_products[0].quantity, 1)
        self.assertEqual(created_kit.kit_products[0].discount_percentage, 10)
        self.assertIsInstance(created_kit.kit_products[1], KitProduct)
        self.assertEqual(created_kit.kit_products[1].product_sku, 'AHJU-49621')
        self.assertEqual(created_kit.kit_products[1].quantity, 2)
        self.assertEqual(created_kit.kit_products[1].discount_percentage, 15)

    def test_list_kit(self):
        kits_mock = mock.MagicMock()
        product_repository_mock = mock.MagicMock()
        kit_repository_mock = mock.MagicMock()
        kit_repository_mock.list.return_value = kits_mock
        service = KitsService(kit_repository_mock, product_repository_mock)

        kits = service.list_kits()

        kit_repository_mock.list.assert_called()
        self.assertEqual(kits_mock, kits)

    def test_get_kit(self):
        kit_mock = mock.MagicMock()
        product_repository_mock = mock.MagicMock()
        kit_repository_mock = mock.MagicMock()
        kit_repository_mock.get_by_id.return_value = kit_mock
        service = KitsService(kit_repository_mock, product_repository_mock)

        kit = service.get_kit(1)

        kit_repository_mock.get_by_id.assert_called()
        self.assertEqual(kit_mock, kit)

    def test_update_kit(self):
        kit_update_command = {
            'sku': 'FASF-123',
            'name': 'Sony Pack I',
            'kit_products': [
                {
                    'product_sku': 'AHJU-49685',
                    'quantity': 1,
                    'discount_percentage': 10
                },
                {
                    'product_sku': 'AHJU-49621',
                    'quantity': 2,
                    'discount_percentage': 15
                }
            ]
        }
        kit_mock = mock.MagicMock()
        product_repository_mock = mock.MagicMock()
        kit_repository_mock = mock.MagicMock()
        kit_repository_mock.get_by_id.return_value = kit_mock

        service = KitsService(kit_repository_mock, product_repository_mock)
        updated_kit = service.update_kit(1, kit_update_command)

        self.assertEqual(updated_kit, kit_mock)
        kit_repository_mock.get_by_id.assert_called_with(1)
        kit_products = [KitProduct(**kit_product) for kit_product in kit_update_command.pop('kit_products')]
        kit_mock.update_infos.assert_called_with(**kit_update_command, kit_products=kit_products)
        kit_repository_mock.update.assert_called_with(kit_mock)

    def test_remove_kit(self):
        product_repository_mock = mock.MagicMock()
        kit_repository_mock = mock.MagicMock()
        service = KitsService(kit_repository_mock, product_repository_mock)
        service.remove_kit(1)
        kit_repository_mock.remove.assert_called_with(1)


class TestCalculatedKitsService(TestCase):

    def test_get_calculated_kit(self):
        product_A_mock = mock.MagicMock()
        product_A_mock.inventory_quantity = 10
        product_A_mock.cost = 20.00
        product_A_mock.price = 100.00
        product_A_mock.sku = 'A'
        products_mock = [product_A_mock]

        kit_product_A_mock = mock.MagicMock()
        kit_product_A_mock.quantity = 2
        kit_product_A_mock.product_sku = 'A'
        kit_product_A_mock.discount_percentage = 10.00
        kit_mock = mock.MagicMock()
        kit_mock.kit_products = [kit_product_A_mock]

        product_repository_mock = mock.MagicMock()
        product_repository_mock.list_with_skus.return_value = products_mock
        kit_repository_mock = mock.MagicMock()
        kit_repository_mock.get_by_id.return_value = kit_mock

        service = CalculatedKitsService(kit_repository_mock, product_repository_mock)
        calculated_kit = service.calculate_kit(1)
        self.assertIsInstance(calculated_kit, CalculatedKit)
        self.assertEqual(calculated_kit.cost, 40.00)

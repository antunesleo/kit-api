from src.exceptions import NotFound
from src.kitmanagement.domain import Product
from src.kitmanagement.repositories import InMemoryProductRepository
from tests.integration.base import TestCase


class TestInMemoryProductRepository(TestCase):

    def test_add(self):
        repository = InMemoryProductRepository()
        product = Product(
            name='The Last of Us Part II',
            SKU='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )

        product_id = repository.add(product)
        created_product = repository.get_by_id(product_id)

        self.assertIsInstance(product_id, int)
        self.assertEqual(1, product_id)
        self.assertEqual(1, created_product.id)
        self.assertEqual(product.name, created_product.name)
        self.assertEqual(product.SKU, created_product.SKU)
        self.assertEqual(product.price, created_product.price)
        self.assertEqual(product.inventory_quantity, created_product.inventory_quantity)
        self.assertEqual(2, repository.add(product))

    def test_list(self):
        repository = InMemoryProductRepository()
        first_product = Product(
            name='The Last of Us Part II',
            SKU='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        second_product = Product(
            name='God of war',
            SKU='AHJU-49685',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )
        first_product_id = repository.add(first_product)
        second_product_id = repository.add(second_product)

        created_products = repository.list()

        self.assertIsInstance(created_products, list)
        self.assertEqual(2, len(created_products))

        self.assertEqual(first_product_id, created_products[0].id)
        self.assertEqual(first_product.name, created_products[0].name)
        self.assertEqual(first_product.SKU, created_products[0].SKU)
        self.assertEqual(first_product.price, created_products[0].price)
        self.assertEqual(first_product.inventory_quantity, created_products[0].inventory_quantity)

        self.assertEqual(second_product_id, created_products[1].id)
        self.assertEqual(second_product.name, created_products[1].name)
        self.assertEqual(second_product.SKU, created_products[1].SKU)
        self.assertEqual(second_product.price, created_products[1].price)
        self.assertEqual(second_product.inventory_quantity, created_products[1].inventory_quantity)

    def test_get_by_id(self):
        repository = InMemoryProductRepository()
        product = Product(
            name='The Last of Us Part II',
            SKU='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        product_id = repository.add(product)

        created_product = repository.get_by_id(product_id)

        self.assertIsInstance(product, Product)
        self.assertEqual(product_id, created_product.id)
        self.assertEqual(product.name, created_product.name)
        self.assertEqual(product.SKU, created_product.SKU)
        self.assertEqual(product.price, created_product.price)
        self.assertEqual(product.inventory_quantity, created_product.inventory_quantity)

    def test_get_by_id_should_raise_not_found_when_cant_find_product(self):
        repository = InMemoryProductRepository()
        with self.assertRaises(NotFound):
            repository.get_by_id(1)

    def test_remove(self):
        repository = InMemoryProductRepository()
        product = Product(
            name='The Last of Us Part II',
            SKU='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        product_id = repository.add(product)
        repository.remove(product_id)
        with self.assertRaises(NotFound):
            repository.get_by_id(product_id)

from src.kitmanagement.domain import Product
from src.kitmanagement.repositories import InMemoryProductRepository
from tests.integration.base import TestCase


class TestInMemoryProductRepository(TestCase):

    def test_should_add_product(self):
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

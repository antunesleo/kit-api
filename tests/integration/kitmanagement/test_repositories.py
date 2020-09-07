from src.exceptions import NotFound, SKUExistsError
from src.kitmanagement.domain import Product, Kit, KitProduct
from src.kitmanagement.repositories import InMemoryProductRepository, InMemoryKitRepository
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
        self.assertEqual(2, repository.add(Product(
            name='The Last of Us Part II',
            SKU='AHJU-496851',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )))

    def test_add_should_raise_SKUExistsError_when_another_product_has_the_same_SKU(self):
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
        with self.assertRaises(SKUExistsError):
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
            SKU='AHJU-49681',
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

    def test_list_with_SKUs(self):
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
            SKU='AHJU-49684',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )
        third_product = Product(
            name='Horizon Zero Dawn',
            SKU='AHJU-49610',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )

        first_product_id = repository.add(first_product)
        second_product_id = repository.add(second_product)
        repository.add(third_product)

        skus_products = repository.list_with_SKUs(['AHJU-49685', 'AHJU-49684'])

        self.assertIsInstance(skus_products, list)
        self.assertEqual(2, len(skus_products))

        self.assertEqual(first_product_id, skus_products[0].id)
        self.assertEqual(first_product.name, skus_products[0].name)
        self.assertEqual(first_product.SKU, skus_products[0].SKU)
        self.assertEqual(first_product.price, skus_products[0].price)
        self.assertEqual(first_product.inventory_quantity, skus_products[0].inventory_quantity)

        self.assertEqual(second_product_id, skus_products[1].id)
        self.assertEqual(second_product.name, skus_products[1].name)
        self.assertEqual(second_product.SKU, skus_products[1].SKU)
        self.assertEqual(second_product.price, skus_products[1].price)
        self.assertEqual(second_product.inventory_quantity, skus_products[1].inventory_quantity)

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

        self.assertIsInstance(created_product, Product)
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

    def test_remove_should_raise_not_found_when_cant_find_product(self):
        repository = InMemoryProductRepository()
        with self.assertRaises(NotFound):
            repository.remove(1)

    def test_update(self):
        repository = InMemoryProductRepository()
        product = Product(
            name='Last of Us Part II',
            SKU='AHJU-4968',
            cost=2.00,
            price=100.00,
            inventory_quantity=100
        )
        product_id = repository.add(product)
        repository.add(Product(
            name='Bloodborne',
            SKU='AHJU-1458',
            cost=50.00,
            price=200.00,
            inventory_quantity=70
        ))
        product.define_id(product_id)

        product.update_infos(
            name='The Last of Us Part II',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        repository.update(product)

        product = repository.get_by_id(1)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, 'The Last of Us Part II')
        self.assertEqual(product.cost, 10.00)
        self.assertEqual(product.price, 220.00)
        self.assertEqual(product.inventory_quantity, 150)


class TestInMemoryKitRepository(TestCase):

    def test_add(self):
        repository = InMemoryKitRepository()
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
        kit_id = repository.add(kit)
        created_kit = repository.get_by_id(kit_id)

        self.assertIsInstance(kit_id, int)
        self.assertEqual(1, kit_id)
        self.assertEqual(1, created_kit.id)
        self.assertEqual(kit.SKU, created_kit.SKU)
        self.assertEqual(kit.name, created_kit.name)
        self.assertEqual(kit.kit_products[0], created_kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], created_kit.kit_products[1])

    def test_add_should_raise_SKUExistsError_when_another_kit_has_the_same_SKU(self):
        repository = InMemoryKitRepository()
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
        repository.add(kit)
        with self.assertRaises(SKUExistsError):
            repository.add(kit)

    def test_list(self):
        repository = InMemoryKitRepository()

        first_kit_products = [
            KitProduct(
                product_SKU='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_SKU='FASD-14891',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        first_kit = Kit(
            name='Sony Gaming Pack',
            SKU='FASD-789',
            kit_products=first_kit_products
        )
        second_kit_products = [
            KitProduct(
                product_SKU='FASD-498',
                quantity=9,
                discount_percentage=10.5
            ),
            KitProduct(
                product_SKU='FASD-1479',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        second_kit = Kit(
            name='Sony Gaming Pack II',
            SKU='FASD-7894',
            kit_products=second_kit_products
        )
        first_kit_id = repository.add(first_kit)
        second_kit_id = repository.add(second_kit)

        created_kits = repository.list()

        self.assertIsInstance(created_kits, list)
        self.assertEqual(2, len(created_kits))

        self.assertEqual(first_kit_id, created_kits[0].id)
        self.assertEqual(first_kit.SKU, created_kits[0].SKU)
        self.assertEqual(first_kit.name, created_kits[0].name)
        self.assertEqual(first_kit.kit_products[0], created_kits[0].kit_products[0])
        self.assertEqual(first_kit.kit_products[1], created_kits[0].kit_products[1])

        self.assertEqual(second_kit_id, created_kits[1].id)
        self.assertEqual(second_kit.SKU, created_kits[1].SKU)
        self.assertEqual(second_kit.name, created_kits[1].name)
        self.assertEqual(second_kit.kit_products[0], created_kits[1].kit_products[0])
        self.assertEqual(second_kit.kit_products[1], created_kits[1].kit_products[1])

    def test_get_by_id(self):
        repository = InMemoryKitRepository()
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
        kit_id = repository.add(kit)

        created_kit = repository.get_by_id(kit_id)

        self.assertIsInstance(created_kit, Kit)
        self.assertEqual(kit_id, created_kit.id)
        self.assertEqual(kit.name, created_kit.name)
        self.assertEqual(kit.SKU, created_kit.SKU)
        self.assertEqual(kit.kit_products[0], created_kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], created_kit.kit_products[1])

    def test_get_by_id_should_raise_not_found_when_cant_find_kit(self):
        repository = InMemoryProductRepository()
        with self.assertRaises(NotFound):
            repository.get_by_id(1)

    def test_remove(self):
        repository = InMemoryKitRepository()
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
        kit_id = repository.add(kit)
        repository.remove(kit_id)
        with self.assertRaises(NotFound):
            repository.get_by_id(kit_id)

    def test_remove_should_raise_not_found_when_cant_find_kit(self):
        repository = InMemoryKitRepository()
        with self.assertRaises(NotFound):
            repository.remove(1)

    def test_update(self):
        repository = InMemoryKitRepository()
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
        kit_id = repository.add(kit)
        kit.define_id(kit_id)

        repository.add(Kit(
            name='Sony Gaming Pack II',
            SKU='FASD-7894',
            kit_products=[
                KitProduct(
                    product_SKU='FASD-4988',
                    quantity=9,
                    discount_percentage=10.5
                ),
                KitProduct(
                    product_SKU='FASD-1489',
                    quantity=1,
                    discount_percentage=10.5
                )
            ]
        ))

        kit.update_infos(
            name='Sony Gaming Pack I',
            kit_products=[
                KitProduct(
                    product_SKU='FASD-498',
                    quantity=7,
                    discount_percentage=80.5
                ),
                KitProduct(
                    product_SKU='FASD-1429',
                    quantity=5,
                    discount_percentage=72.5
                )
            ]
        )
        repository.update(kit)

        kit = repository.get_by_id(1)
        self.assertEqual(kit.name, 'Sony Gaming Pack I')
        self.assertEqual(kit.kit_products[0], kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], kit.kit_products[1])

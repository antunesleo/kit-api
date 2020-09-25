import pymongo

from src import configurations
from src.exceptions import NotFound, skuExistsError
from src.kitmanagement.domain import Product, Kit, KitProduct
from src.kitmanagement.repositories import InMemoryProductRepository, InMemoryKitRepository, MongoProductRepository, MongoKitRepository
from tests.integration.testbase import TestCase


config = configurations.get_config()


class TestInMemoryProductRepository(TestCase):

    def test_add(self):
        repository = InMemoryProductRepository()
        product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )

        product_id = repository.add(product)
        created_product = repository.get_by_id(product_id)

        self.assertIsInstance(product_id, str)
        self.assertEqual('1', product_id)
        self.assertEqual('1', created_product.id)
        self.assertEqual(product.name, created_product.name)
        self.assertEqual(product.sku, created_product.sku)
        self.assertEqual(product.price, created_product.price)
        self.assertEqual(product.inventory_quantity, created_product.inventory_quantity)
        self.assertEqual('2', repository.add(Product(
            name='The Last of Us Part II',
            sku='AHJU-496851',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )))

    def test_add_should_raise_skuExistsError_when_another_product_has_the_same_sku(self):
        repository = InMemoryProductRepository()
        product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )

        product_id = repository.add(product)
        created_product = repository.get_by_id(product_id)

        self.assertIsInstance(product_id, str)
        self.assertEqual('1', product_id)
        self.assertEqual('1', created_product.id)
        self.assertEqual(product.name, created_product.name)
        self.assertEqual(product.sku, created_product.sku)
        self.assertEqual(product.price, created_product.price)
        self.assertEqual(product.inventory_quantity, created_product.inventory_quantity)
        with self.assertRaises(skuExistsError):
            self.assertEqual('2', repository.add(product))

    def test_list(self):
        repository = InMemoryProductRepository()
        first_product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        second_product = Product(
            name='God of war',
            sku='AHJU-49681',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )
        first_product_id = repository.add(first_product)
        second_product_id = repository.add(second_product)

        created_products = repository.list()

        self.assertIsInstance(created_products, tuple)
        self.assertEqual(2, len(created_products))

        self.assertEqual(first_product_id, created_products[0].id)
        self.assertEqual(first_product.name, created_products[0].name)
        self.assertEqual(first_product.sku, created_products[0].sku)
        self.assertEqual(first_product.price, created_products[0].price)
        self.assertEqual(first_product.inventory_quantity, created_products[0].inventory_quantity)

        self.assertEqual(second_product_id, created_products[1].id)
        self.assertEqual(second_product.name, created_products[1].name)
        self.assertEqual(second_product.sku, created_products[1].sku)
        self.assertEqual(second_product.price, created_products[1].price)
        self.assertEqual(second_product.inventory_quantity, created_products[1].inventory_quantity)

    def test_list_with_skus(self):
        repository = InMemoryProductRepository()
        first_product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        second_product = Product(
            name='God of war',
            sku='AHJU-49684',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )
        third_product = Product(
            name='Horizon Zero Dawn',
            sku='AHJU-49610',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )

        first_product_id = repository.add(first_product)
        second_product_id = repository.add(second_product)
        repository.add(third_product)

        skus_products = repository.list_with_skus(['AHJU-49685', 'AHJU-49684'])

        self.assertIsInstance(skus_products, tuple)
        self.assertEqual(2, len(skus_products))

        self.assertEqual(first_product_id, skus_products[0].id)
        self.assertEqual(first_product.name, skus_products[0].name)
        self.assertEqual(first_product.sku, skus_products[0].sku)
        self.assertEqual(first_product.price, skus_products[0].price)
        self.assertEqual(first_product.inventory_quantity, skus_products[0].inventory_quantity)

        self.assertEqual(second_product_id, skus_products[1].id)
        self.assertEqual(second_product.name, skus_products[1].name)
        self.assertEqual(second_product.sku, skus_products[1].sku)
        self.assertEqual(second_product.price, skus_products[1].price)
        self.assertEqual(second_product.inventory_quantity, skus_products[1].inventory_quantity)

    def test_get_by_id(self):
        repository = InMemoryProductRepository()
        product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        product_id = repository.add(product)

        created_product = repository.get_by_id(product_id)

        self.assertIsInstance(created_product, Product)
        self.assertEqual(product_id, created_product.id)
        self.assertEqual(product.name, created_product.name)
        self.assertEqual(product.sku, created_product.sku)
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
            sku='AHJU-49685',
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
            sku='AHJU-4968',
            cost=2.00,
            price=100.00,
            inventory_quantity=100
        )
        product_id = repository.add(product)
        repository.add(Product(
            name='Bloodborne',
            sku='AHJU-1458',
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

        product = repository.get_by_id('1')
        self.assertEqual(product.id, '1')
        self.assertEqual(product.name, 'The Last of Us Part II')
        self.assertEqual(product.cost, 10.00)
        self.assertEqual(product.price, 220.00)
        self.assertEqual(product.inventory_quantity, 150)


class TestInMemoryKitRepository(TestCase):

    def test_add(self):
        repository = InMemoryKitRepository()
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        kit_id = repository.add(kit)
        created_kit = repository.get_by_id(kit_id)

        self.assertIsInstance(kit_id, str)
        self.assertEqual('1', kit_id)
        self.assertEqual('1', created_kit.id)
        self.assertEqual(kit.sku, created_kit.sku)
        self.assertEqual(kit.name, created_kit.name)
        self.assertEqual(kit.kit_products[0], created_kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], created_kit.kit_products[1])

    def test_add_should_raise_skuExistsError_when_another_kit_has_the_same_sku(self):
        repository = InMemoryKitRepository()
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        repository.add(kit)
        with self.assertRaises(skuExistsError):
            repository.add(kit)

    def test_list(self):
        repository = InMemoryKitRepository()

        first_kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-14891',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        first_kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=first_kit_products
        )
        second_kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=9,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1479',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        second_kit = Kit(
            name='Sony Gaming Pack II',
            sku='FASD-7894',
            kit_products=second_kit_products
        )
        first_kit_id = repository.add(first_kit)
        second_kit_id = repository.add(second_kit)

        created_kits = repository.list()

        self.assertIsInstance(created_kits, tuple)
        self.assertEqual(2, len(created_kits))

        self.assertEqual(first_kit_id, created_kits[0].id)
        self.assertEqual(first_kit.sku, created_kits[0].sku)
        self.assertEqual(first_kit.name, created_kits[0].name)
        self.assertEqual(first_kit.kit_products[0], created_kits[0].kit_products[0])
        self.assertEqual(first_kit.kit_products[1], created_kits[0].kit_products[1])

        self.assertEqual(second_kit_id, created_kits[1].id)
        self.assertEqual(second_kit.sku, created_kits[1].sku)
        self.assertEqual(second_kit.name, created_kits[1].name)
        self.assertEqual(second_kit.kit_products[0], created_kits[1].kit_products[0])
        self.assertEqual(second_kit.kit_products[1], created_kits[1].kit_products[1])

    def test_get_by_id(self):
        repository = InMemoryKitRepository()
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        kit_id = repository.add(kit)

        created_kit = repository.get_by_id(kit_id)

        self.assertIsInstance(created_kit, Kit)
        self.assertEqual(kit_id, created_kit.id)
        self.assertEqual(kit.name, created_kit.name)
        self.assertEqual(kit.sku, created_kit.sku)
        self.assertEqual(kit.kit_products[0], created_kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], created_kit.kit_products[1])

    def test_get_by_id_should_raise_not_found_when_cant_find_kit(self):
        repository = InMemoryProductRepository()
        with self.assertRaises(NotFound):
            repository.get_by_id('1')

    def test_remove(self):
        repository = InMemoryKitRepository()
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
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
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        kit_id = repository.add(kit)
        kit.define_id(kit_id)

        repository.add(Kit(
            name='Sony Gaming Pack II',
            sku='FASD-7894',
            kit_products=[
                KitProduct(
                    product_sku='FASD-4988',
                    quantity=9,
                    discount_percentage=10.5
                ),
                KitProduct(
                    product_sku='FASD-1489',
                    quantity=1,
                    discount_percentage=10.5
                )
            ]
        ))

        kit.update_infos(
            name='Sony Gaming Pack I',
            kit_products=[
                KitProduct(
                    product_sku='FASD-498',
                    quantity=7,
                    discount_percentage=80.5
                ),
                KitProduct(
                    product_sku='FASD-1429',
                    quantity=5,
                    discount_percentage=72.5
                )
            ]
        )
        repository.update(kit)

        kit = repository.get_by_id('1')
        self.assertEqual(kit.name, 'Sony Gaming Pack I')
        self.assertEqual(kit.kit_products[0], kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], kit.kit_products[1])

    def test_list_with_product(self):
        repository = InMemoryKitRepository()

        first_kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-14891',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        first_kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=first_kit_products
        )
        second_kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=9,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1479',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        second_kit = Kit(
            name='Sony Gaming Pack II',
            sku='FASD-7894',
            kit_products=second_kit_products
        )
        third_kit_products = [
            KitProduct(
                product_sku='FASD-49809',
                quantity=9,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-147099',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        third_kit = Kit(
            name='Sony Gaming Pack III',
            sku='FASD-78990',
            kit_products=third_kit_products
        )
        first_kit_id = repository.add(first_kit)
        second_kit_id = repository.add(second_kit)
        third_kit_id = repository.add(third_kit)

        created_kits = repository.list_with_product('FASD-498')

        self.assertIsInstance(created_kits, tuple)
        self.assertEqual(2, len(created_kits))

        self.assertEqual(first_kit_id, created_kits[0].id)
        self.assertEqual(first_kit.sku, created_kits[0].sku)
        self.assertEqual(first_kit.name, created_kits[0].name)
        self.assertEqual(first_kit.kit_products[0], created_kits[0].kit_products[0])
        self.assertEqual(first_kit.kit_products[1], created_kits[0].kit_products[1])

        self.assertEqual(second_kit_id, created_kits[1].id)
        self.assertEqual(second_kit.sku, created_kits[1].sku)
        self.assertEqual(second_kit.name, created_kits[1].name)
        self.assertEqual(second_kit.kit_products[0], created_kits[1].kit_products[0])
        self.assertEqual(second_kit.kit_products[1], created_kits[1].kit_products[1])


class TestMongoProductRepository(TestCase):

    def setUp(self) -> None:
        self.mongo_client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        self.mongo_db = self.mongo_client['test-database']
        self.mongo_db.products.create_index("sku", unique=True)

    def test_add(self):
        repository = MongoProductRepository(self.mongo_db)

        product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )

        product_id = repository.add(product)
        created_product = repository.get_by_id(product_id)

        self.assertIsInstance(product_id, str)
        self.assertEqual(product_id, created_product.id)
        self.assertEqual(product.name, created_product.name)
        self.assertEqual(product.sku, created_product.sku)
        self.assertEqual(product.price, created_product.price)
        self.assertEqual(product.inventory_quantity, created_product.inventory_quantity)

    def test_add_should_raise_skuExistsError_when_another_product_has_the_same_sku(self):
        repository = MongoProductRepository(self.mongo_db)

        product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )

        repository.add(product)

        with self.assertRaises(skuExistsError):
            repository.add(product)

    def test_get_by_id(self):
        repository = MongoProductRepository(self.mongo_db)
        product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        product_id = repository.add(product)

        created_product = repository.get_by_id(product_id)

        self.assertIsInstance(created_product, Product)
        self.assertEqual(product_id, created_product.id)
        self.assertEqual(product.name, created_product.name)
        self.assertEqual(product.sku, created_product.sku)
        self.assertEqual(product.price, created_product.price)
        self.assertEqual(product.inventory_quantity, created_product.inventory_quantity)

    def test_get_by_id_should_raise_not_found_when_cant_find_product(self):
        repository = MongoProductRepository(self.mongo_db)
        with self.assertRaises(NotFound):
            repository.get_by_id('5f566e9c1022bd08188d674b')

    def test_get_by_sku(self):
        repository = MongoProductRepository(self.mongo_db)
        product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        product_id = repository.add(product)

        created_product = repository.get_by_sku('AHJU-49685')

        self.assertIsInstance(created_product, Product)
        self.assertEqual(product_id, created_product.id)
        self.assertEqual(product.name, created_product.name)
        self.assertEqual(product.sku, created_product.sku)
        self.assertEqual(product.price, created_product.price)
        self.assertEqual(product.inventory_quantity, created_product.inventory_quantity)

    def test_list(self):
        repository = MongoProductRepository(self.mongo_db)
        first_product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        second_product = Product(
            name='God of war',
            sku='AHJU-49681',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )
        first_product_id = repository.add(first_product)
        second_product_id = repository.add(second_product)

        created_products = repository.list()

        self.assertIsInstance(created_products, tuple)
        self.assertEqual(2, len(created_products))

        self.assertEqual(first_product_id, created_products[0].id)
        self.assertEqual(first_product.name, created_products[0].name)
        self.assertEqual(first_product.sku, created_products[0].sku)
        self.assertEqual(first_product.price, created_products[0].price)
        self.assertEqual(first_product.inventory_quantity, created_products[0].inventory_quantity)

        self.assertEqual(second_product_id, created_products[1].id)
        self.assertEqual(second_product.name, created_products[1].name)
        self.assertEqual(second_product.sku, created_products[1].sku)
        self.assertEqual(second_product.price, created_products[1].price)
        self.assertEqual(second_product.inventory_quantity, created_products[1].inventory_quantity)

    def test_list_with_skus(self):
        repository = MongoProductRepository(self.mongo_db)

        first_product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        second_product = Product(
            name='God of war',
            sku='AHJU-49684',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )
        third_product = Product(
            name='Horizon Zero Dawn',
            sku='AHJU-49610',
            cost=20.00,
            price=220.00,
            inventory_quantity=80
        )

        first_product_id = repository.add(first_product)
        second_product_id = repository.add(second_product)
        repository.add(third_product)

        skus_products = repository.list_with_skus(['AHJU-49685', 'AHJU-49684'])

        self.assertIsInstance(skus_products, tuple)
        self.assertEqual(2, len(skus_products))

        self.assertEqual(first_product_id, skus_products[0].id)
        self.assertEqual(first_product.name, skus_products[0].name)
        self.assertEqual(first_product.sku, skus_products[0].sku)
        self.assertEqual(first_product.price, skus_products[0].price)
        self.assertEqual(first_product.inventory_quantity, skus_products[0].inventory_quantity)

        self.assertEqual(second_product_id, skus_products[1].id)
        self.assertEqual(second_product.name, skus_products[1].name)
        self.assertEqual(second_product.sku, skus_products[1].sku)
        self.assertEqual(second_product.price, skus_products[1].price)
        self.assertEqual(second_product.inventory_quantity, skus_products[1].inventory_quantity)

    def test_remove(self):
        repository = MongoProductRepository(self.mongo_db)

        product = Product(
            name='The Last of Us Part II',
            sku='AHJU-49685',
            cost=10.00,
            price=220.00,
            inventory_quantity=150
        )
        product_id = repository.add(product)
        repository.remove(product_id)

        with self.assertRaises(NotFound):
            repository.get_by_id(product_id)

    def test_remove_should_raise_not_found_when_cant_find_product(self):
        repository = MongoProductRepository(self.mongo_db)
        with self.assertRaises(NotFound):
            repository.remove('5f566e9c1022bd08188d674b')

    def test_update(self):
        repository = MongoProductRepository(self.mongo_db)
        product = Product(
            name='Last of Us Part II',
            sku='AHJU-4968',
            cost=2.00,
            price=100.00,
            inventory_quantity=100
        )
        product_id = repository.add(product)
        repository.add(Product(
            name='Bloodborne',
            sku='AHJU-1458',
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

        product = repository.get_by_id(product_id)
        self.assertEqual(product.id, product_id)
        self.assertEqual(product.name, 'The Last of Us Part II')
        self.assertEqual(product.cost, 10.00)
        self.assertEqual(product.price, 220.00)
        self.assertEqual(product.inventory_quantity, 150)

    def test_update_should_raise_not_found_when_cant_find_product(self):
        repository = MongoProductRepository(self.mongo_db)
        product = Product(
            id='5f566e9c1022bd08188d674b',
            name='Last of Us Part II',
            sku='AHJU-4968',
            cost=2.00,
            price=100.00,
            inventory_quantity=100
        )
        with self.assertRaises(NotFound):
            repository.update(product)

    def tearDown(self) -> None:
        self.mongo_db.drop_collection('products')


class TestMongoKitRepository(TestCase):

    def setUp(self) -> None:
        self.mongo_client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        self.mongo_db = self.mongo_client['test-database']
        self.mongo_db.kits.create_index("sku", unique=True)

    def test_add(self):
        repository = MongoKitRepository(self.mongo_db)
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        kit_id = repository.add(kit)
        created_kit = repository.get_by_id(kit_id)

        self.assertIsInstance(kit_id, str)
        self.assertEqual(kit_id, created_kit.id)
        self.assertEqual(kit.sku, created_kit.sku)
        self.assertEqual(kit.name, created_kit.name)
        self.assertEqual(kit.kit_products[0], created_kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], created_kit.kit_products[1])

    def test_add_should_raise_skuExistsError_when_another_kit_has_the_same_sku(self):
        repository = MongoKitRepository(self.mongo_db)
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        repository.add(kit)
        with self.assertRaises(skuExistsError):
            repository.add(kit)

    def test_list(self):
        repository = MongoKitRepository(self.mongo_db)

        first_kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-14891',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        first_kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=first_kit_products
        )
        second_kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=9,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1479',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        second_kit = Kit(
            name='Sony Gaming Pack II',
            sku='FASD-7894',
            kit_products=second_kit_products
        )
        first_kit_id = repository.add(first_kit)
        second_kit_id = repository.add(second_kit)

        created_kits = repository.list()

        self.assertIsInstance(created_kits, tuple)
        self.assertEqual(2, len(created_kits))

        self.assertEqual(first_kit_id, created_kits[0].id)
        self.assertEqual(first_kit.sku, created_kits[0].sku)
        self.assertEqual(first_kit.name, created_kits[0].name)
        self.assertEqual(first_kit.kit_products[0], created_kits[0].kit_products[0])
        self.assertEqual(first_kit.kit_products[1], created_kits[0].kit_products[1])

        self.assertEqual(second_kit_id, created_kits[1].id)
        self.assertEqual(second_kit.sku, created_kits[1].sku)
        self.assertEqual(second_kit.name, created_kits[1].name)
        self.assertEqual(second_kit.kit_products[0], created_kits[1].kit_products[0])
        self.assertEqual(second_kit.kit_products[1], created_kits[1].kit_products[1])

    def test_list_with_product(self):
        repository = MongoKitRepository(self.mongo_db)

        first_kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-14891',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        first_kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=first_kit_products
        )
        second_kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=9,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1479',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        second_kit = Kit(
            name='Sony Gaming Pack II',
            sku='FASD-7894',
            kit_products=second_kit_products
        )
        third_kit_products = [
            KitProduct(
                product_sku='FASD-49809',
                quantity=9,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-147099',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        third_kit = Kit(
            name='Sony Gaming Pack III',
            sku='FASD-78990',
            kit_products=third_kit_products
        )
        first_kit_id = repository.add(first_kit)
        second_kit_id = repository.add(second_kit)
        third_kit_id = repository.add(third_kit)

        created_kits = repository.list_with_product('FASD-498')

        self.assertIsInstance(created_kits, tuple)
        self.assertEqual(2, len(created_kits))

        self.assertEqual(first_kit_id, created_kits[0].id)
        self.assertEqual(first_kit.sku, created_kits[0].sku)
        self.assertEqual(first_kit.name, created_kits[0].name)
        self.assertEqual(first_kit.kit_products[0], created_kits[0].kit_products[0])
        self.assertEqual(first_kit.kit_products[1], created_kits[0].kit_products[1])

        self.assertEqual(second_kit_id, created_kits[1].id)
        self.assertEqual(second_kit.sku, created_kits[1].sku)
        self.assertEqual(second_kit.name, created_kits[1].name)
        self.assertEqual(second_kit.kit_products[0], created_kits[1].kit_products[0])
        self.assertEqual(second_kit.kit_products[1], created_kits[1].kit_products[1])

    def test_get_by_id(self):
        repository = InMemoryKitRepository()
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        kit_id = repository.add(kit)

        created_kit = repository.get_by_id(kit_id)

        self.assertIsInstance(created_kit, Kit)
        self.assertEqual(kit_id, created_kit.id)
        self.assertEqual(kit.name, created_kit.name)
        self.assertEqual(kit.sku, created_kit.sku)
        self.assertEqual(kit.kit_products[0], created_kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], created_kit.kit_products[1])

    def test_get_by_id_should_raise_not_found_when_cant_find_kit(self):
        repository = MongoKitRepository(self.mongo_db)
        with self.assertRaises(NotFound):
            repository.get_by_id('5f566e9c1022bd08188d674b')

    def test_remove(self):
        repository = MongoKitRepository(self.mongo_db)
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        kit_id = repository.add(kit)
        repository.remove(kit_id)
        with self.assertRaises(NotFound):
            repository.get_by_id(kit_id)

    def test_remove_should_raise_not_found_when_cant_find_kit(self):
        repository = MongoKitRepository(self.mongo_db)
        with self.assertRaises(NotFound):
            repository.remove('5f566e9c1022bd08188d674b')

    def test_update(self):
        repository = MongoKitRepository(self.mongo_db)
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        kit_id = repository.add(kit)
        kit.define_id(kit_id)

        repository.add(Kit(
            name='Sony Gaming Pack II',
            sku='FASD-7894',
            kit_products=[
                KitProduct(
                    product_sku='FASD-4988',
                    quantity=9,
                    discount_percentage=10.5
                ),
                KitProduct(
                    product_sku='FASD-1489',
                    quantity=1,
                    discount_percentage=10.5
                )
            ]
        ))

        kit.update_infos(
            name='Sony Gaming Pack I',
            kit_products=[
                KitProduct(
                    product_sku='FASD-498',
                    quantity=7,
                    discount_percentage=80.5
                ),
                KitProduct(
                    product_sku='FASD-1429',
                    quantity=5,
                    discount_percentage=72.5
                )
            ]
        )
        repository.update(kit)

        kit = repository.get_by_id(kit_id)
        self.assertEqual(kit.name, 'Sony Gaming Pack I')
        self.assertEqual(kit.kit_products[0], kit.kit_products[0])
        self.assertEqual(kit.kit_products[1], kit.kit_products[1])

    def test_update_should_raise_not_found_when_cant_find_product(self):
        repository = MongoKitRepository(self.mongo_db)
        kit_products = [
            KitProduct(
                product_sku='FASD-498',
                quantity=2,
                discount_percentage=10.5
            ),
            KitProduct(
                product_sku='FASD-1489',
                quantity=1,
                discount_percentage=10.5
            )
        ]
        kit = Kit(
            id='5f566e9c1022bd08188d674b',
            name='Sony Gaming Pack',
            sku='FASD-789',
            kit_products=kit_products
        )
        with self.assertRaises(NotFound):
            repository.update(kit)

    def tearDown(self) -> None:
        self.mongo_db.drop_collection('kits')

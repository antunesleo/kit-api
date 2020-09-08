from abc import ABC
from copy import deepcopy
from typing import List, Union

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from src.exceptions import NotFound, SKUExistsError
from src.kitmanagement.domain import ProductRepository, KitRepository, Kit, Product, KitProduct


class InMemoryProductRepository(ProductRepository):

    def __init__(self):
        self.__products : List[Product] = []

    def add(self, product: Product) -> str:
        product = deepcopy(product)
        product.define_id(self.__next_id())
        self.__raise_if_SKU_already_exists(product.SKU)
        self.__products.append(product)
        return product.id

    def list(self, for_read=True) -> List[Product]:
        return self.__products

    def get_by_id(self, product_id: str) -> Product:
        for product in self.__products:
            if product.id == product_id:
                return product
        raise NotFound(f'product id: {product_id} not found')

    def get_by_SKU(self, sku: str) -> Product:
        for product in self.__products:
            if product.SKU == sku:
                return product
        raise NotFound(f'product sku: {sku} not found')

    def remove(self, product_id: str) -> None:
        index_to_remove = None

        for index, product in enumerate(self.__products):
            if product.id == product_id:
                index_to_remove = index
                break

        if index_to_remove is None:
            raise NotFound(f'product id: {product_id} not found')

        self.__products.pop(index_to_remove)

    def update(self, product_to_update: Product) -> None:
        index_to_update = None

        for index, product in enumerate(self.__products):
            if product.id == product_to_update.id:
                index_to_update = index
                break

        if index_to_update is None:
            raise NotFound(f'product id: {product_to_update.id} not found')

        self.__products[index_to_update] = product_to_update

    def list_with_SKUs(self, SKUs: List[str]) -> List[Product]:
        return[product for product in self.__products if product.SKU in SKUs]

    def __next_id(self) -> str:
        try:
            return str(int(max(self.__products, key=lambda p: int(p.id)).id) + 1)
        except ValueError:
            return '1'

    def __raise_if_SKU_already_exists(self, SKU: str) -> None:
        for product in self.__products:
            if product.SKU == SKU:
                raise SKUExistsError('you must provide an unique SKU')
        return None


class InMemoryKitRepository(KitRepository, ABC):

    def __init__(self):
        self.__kits : List[Kit] = []

    def add(self, kit: Kit) -> Union[int, str]:
        kit = deepcopy(kit)
        kit.define_id(self.__next_id())
        self.__raise_if_SKU_already_exists(kit.SKU)
        self.__kits.append(kit)
        return kit.id

    def list(self, for_read=True) -> List[Kit]:
        return self.__kits

    def list_with_product(self, product_SKU: str) -> List[Kit]:
        kits = []
        for kit in self.__kits:
            for kit_product in kit.kit_products:
                if kit_product.product_SKU == product_SKU:
                    kits.append(kit)
        return kits

    def get_by_id(self, kit_id) -> Kit:
        for kit in self.__kits:
            if kit.id == kit_id:
                return kit
        raise NotFound(f'kit id: {kit_id} not found')

    def remove(self, kit_id) -> None:
        index_to_remove = None

        for index, kid in enumerate(self.__kits):
            if kid.id == kit_id:
                index_to_remove = index
                break

        if index_to_remove is None:
            raise NotFound(f'kit id: {kit_id} not found')

        self.__kits.pop(index_to_remove)

    def update(self, kit_to_update: Kit) -> None:
        index_to_update = None

        for index, kit in enumerate(self.__kits):
            if kit.id == kit_to_update.id:
                index_to_update = index
                break

        if index_to_update is None:
            raise NotFound(f'kit id: {kit_to_update.id} not found')

        self.__kits[index_to_update] = kit_to_update

    def __next_id(self) -> str:
        try:
            return str(int(max(self.__kits, key=lambda k: int(k.id)).id) + 1)
        except ValueError:
            return '1'

    def __raise_if_SKU_already_exists(self, SKU: str) -> None:
        for kit in self.__kits:
            if kit.SKU == SKU:
                raise SKUExistsError('you must provide an unique SKU')
        return None


class MongoProductRepository(ProductRepository):

    def __init__(self, mongo_db):
        self.__mongo_db = mongo_db
        self.__collection = self.__mongo_db['products']

    def list(self) -> List[Product]:
        return [self.__create_product_from_mongo(mongo_product) for mongo_product in self.__collection.find()]

    def list_with_SKUs(self, SKUs: List[str]) -> List[Product]:
        return [
            self.__create_product_from_mongo(mongo_product)
            for mongo_product in self.__collection.find({'SKU': {'$in': SKUs}}).sort('_id')
        ]

    def add(self, product: Product) -> str:
        try:
            added_product = self.__collection.insert_one(self.__create_mongo_product_from_product(product))
        except DuplicateKeyError:
            raise SKUExistsError('you must provide an unique SKU')

        return str(added_product.inserted_id)

    def get_by_id(self, product_id: str) -> Product:
        mongo_product = self.__collection.find_one({'_id': ObjectId(product_id)})
        if not mongo_product:
            raise NotFound(f'product id: {product_id} not found')
        return self.__create_product_from_mongo(mongo_product)

    def get_by_SKU(self, SKU: str) -> Product:
        mongo_product = self.__collection.find_one({'SKU': SKU})
        if not mongo_product:
            raise NotFound(f'product SKU: {SKU} not found')
        return self.__create_product_from_mongo(mongo_product)

    def remove(self, product_id: str) -> None:
        result = self.__collection.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count < 1:
            raise NotFound(f'product id: {product_id} not found')

    def update(self, product: Product) -> None:
        mongo_product = self.__create_mongo_product_from_product(product)
        result = self.__collection.update_one(
            {'_id': ObjectId(product.id)},
            {'$set': mongo_product}
        )
        if result.matched_count < 1:
            raise NotFound(f'product id: {product.id} not found')

    def __create_product_from_mongo(self, mongo_product: dict) -> Product:
        return Product(
            id=str(mongo_product['_id']),
            name=mongo_product['name'],
            SKU=mongo_product['SKU'],
            cost=mongo_product['cost'],
            price=mongo_product['price'],
            inventory_quantity=mongo_product['inventoryQuantity']
        )

    def __create_mongo_product_from_product(self, product: Product) -> dict:
        return {
            'name': product.name,
            'SKU': product.SKU,
            'cost': product.cost,
            'price': product.price,
            'inventoryQuantity': product.inventory_quantity
        }


class MongoKitRepository(KitRepository):

    def __init__(self, mongo_db):
        self.__mongo_db = mongo_db
        self.__collection = self.__mongo_db['kits']

    def list(self) -> List[Kit]:
        return [self.__create_kit_from_mongo(mongo_kit) for mongo_kit in self.__collection.find()]

    def list_with_product(self, product_SKU: str) -> List[Kit]:
        return [self.__create_kit_from_mongo(mongo_kit) for mongo_kit in self.__collection.find({"kitProducts.productSKU": product_SKU})]

    def add(self, kit: Kit) -> str:
        try:
            added_kit = self.__collection.insert_one(self.__create_mongo_kit_from_kit(kit))
        except DuplicateKeyError:
            raise SKUExistsError('you must provide an unique SKU')

        return str(added_kit.inserted_id)

    def get_by_id(self, kit_id: str) -> Kit:
        mongo_product = self.__collection.find_one({'_id': ObjectId(kit_id)})
        if not mongo_product:
            raise NotFound(f'kit id: {kit_id} not found')
        return self.__create_kit_from_mongo(mongo_product)

    def remove(self, kit_id: str) -> None:
        result = self.__collection.delete_one({'_id': ObjectId(kit_id)})
        if result.deleted_count < 1:
            raise NotFound(f'kit id: {kit_id} not found')

    def update(self, kit: Kit) -> None:
        kit_mongo = self.__create_mongo_kit_from_kit(kit)
        result = self.__collection.update_one(
            {'_id': ObjectId(kit.id)},
            {'$set': kit_mongo}
        )
        if result.matched_count < 1:
            raise NotFound(f'product id: {kit.id} not found')

    @staticmethod
    def __create_kit_from_mongo(kit_mongo: dict) -> Kit:
        kit_products = [
            KitProduct(
                product_SKU=kit_product_mongo['productSKU'],
                quantity=kit_product_mongo['quantity'],
                discount_percentage=kit_product_mongo['discountPercentage']
            )
            for kit_product_mongo in kit_mongo.pop('kitProducts')
        ]
        return Kit(
            id=str(kit_mongo['_id']),
            name=kit_mongo['name'],
            SKU=kit_mongo['SKU'],
            kit_products=kit_products
        )

    def __create_mongo_kit_from_kit(self, kit: Kit) -> dict:
        kit_products_mongo = [
            {
                'productSKU': kit_product.product_SKU,
                'quantity': kit_product.quantity,
                'discountPercentage': kit_product.discount_percentage
            }
            for kit_product in kit.kit_products
        ]
        return {
            'name': kit.name,
            'SKU': kit.SKU,
            'kitProducts': kit_products_mongo
        }

import uuid
import re


class ShoppingCart:
    
    CATALOG = {"apple": 10, "banana": 15, "orange": 12} 

    def __init__(self, customerId):
        if not self._validate_customer_id(customerId):
            raise ValueError("Invalid Customer ID format")

        self._cartId = uuid.uuid4()
        self._customerId = customerId
        self._items = {}  

    @staticmethod
    def _validate_customer_id(customerId):
        pattern = r"^[A-Za-z]{3}\d{5}[A-Za-z]{2}-[AQ]$"
        return re.match(pattern, customerId) is not None

    @property
    def cartId(self):
        return self._cartId

    @property
    def customerId(self):
        return self._customerId

    def add_item(self, item, quantity):
        if not self._is_valid_item(item) or not self._is_valid_quantity(quantity):
            raise ValueError("Invalid item or quantity")
        if item not in self.CATALOG:
            raise ValueError("Item not in catalog")
        self._items[item] = self._items.get(item, 0) + quantity


    def update_item(self, item, quantity):
        if not self._is_valid_item(item) or not self._is_valid_quantity(quantity, allow_zero=True):
            raise ValueError("Invalid item or quantity")
        if quantity == 0:
            self.remove_item(item)
        else:
            self._items[item] = quantity

    def remove_item(self, item):
        if item in self._items:
            del self._items[item]

    def get_items(self):
        return dict(self._items)

    def get_total_cost(self):
        return sum(quantity * self.get_catalog_item_price(item) for item, quantity in self._items.items())


    @classmethod
    def get_catalog_item_price(cls, item):
        return cls.CATALOG.get(item, None)

    @staticmethod
    def _is_valid_item(item):
        return isinstance(item, str) and 1 <= len(item) <= 20

    @staticmethod
    def _is_valid_quantity(quantity, allow_zero=False):
        if allow_zero:
            return isinstance(quantity, int) and quantity >= 0
        else:
            return isinstance(quantity, int) and 1 <= quantity <= 100
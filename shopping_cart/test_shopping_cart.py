import unittest
import shoppingcart

class TestShoppingCart(unittest.TestCase):

    def test_cart_creation_with_valid_customer_id(self):
        valid_customer_id = "ABC12345DE-Q"
        cart = shoppingcart.ShoppingCart(valid_customer_id)
        self.assertIsNotNone(cart.cartId)
        self.assertEqual(cart.customerId, valid_customer_id)

    def test_cart_creation_with_invalid_customer_id(self):
        invalid_customer_ids = ["12345ABCDE", "AB12CDE34", "ABCD1234-E", "AB12345DE-1"]
        for id in invalid_customer_ids:
            with self.assertRaises(ValueError):
                shoppingcart.ShoppingCart(id)

    def test_immutability_of_cartId_and_customerId(self):
        cart = shoppingcart.ShoppingCart("ABC12345DE-A")
        with self.assertRaises(AttributeError):
            cart.cartId = "new_cart_id"
        with self.assertRaises(AttributeError):
            cart.customerId = "new_customer_id"
            
    def test_cart_id_is_valid_uuid4(self):
        cart = shoppingcart.ShoppingCart("ABC12345DE-A")
        try:
            uuid_obj = shoppingcart.uuid.UUID(str(cart.cartId), version=4)
            self.assertEqual(cart.cartId, uuid_obj)
        except ValueError:
            self.fail("cartId is not a valid UUID4")
    def setUp(self):
        self.cart = shoppingcart.ShoppingCart("ABC12345DE-A")

    def test_add_item(self):
        self.cart.add_item("apple", 5)
        self.assertEqual(self.cart.get_items(), {"apple": 5})
    
    def test_add_item_with_invalid_name(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("a"*21, 1) 
            
    def test_add_item_with_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("apple", -1)  
            
    def test_add_item_not_in_catalog(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("not_in_catalog", 1)

    def test_update_item(self):
        self.cart.add_item("apple", 5)
        self.cart.update_item("apple", 10)
        self.assertEqual(self.cart.get_items(), {"apple": 10})

    def test_remove_item(self):
        self.cart.add_item("apple", 5)
        self.cart.remove_item("apple")
        self.assertEqual(self.cart.get_items(), {})

    def test_get_total_cost(self):
        self.cart.add_item("apple", 10)   
        self.cart.add_item("banana", 15)  
        
        
        expected_cost = 10 * shoppingcart.ShoppingCart.CATALOG["apple"] + 15 * shoppingcart.ShoppingCart.CATALOG["banana"]
        self.assertEqual(self.cart.get_total_cost(), expected_cost)
 
            
    def test_defensive_copying_for_get_items(self):
        self.cart.add_item("apple", 5)
        items = self.cart.get_items()
        items["apple"] = 10
        self.assertNotEqual(self.cart.get_items(), items)
if __name__ == '__main__':
    unittest.main()

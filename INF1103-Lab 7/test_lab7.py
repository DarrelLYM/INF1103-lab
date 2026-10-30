"""Lab 7 tests (Section 7: Testing and review).

Run with:  python -m unittest -v test_lab7
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from file_handler import FileHandler


def captured_display(product):
    """Return what display_information() prints."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        product.display_information()
    return buffer.getvalue()


class TestPhysicalProduct(unittest.TestCase):
    def setUp(self):
        self.guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, 4.0)

    def test_stores_weight(self):
        self.assertEqual(self.guitar.get_weight(), 4.0)

    def test_display_includes_parent_and_child_info(self):
        output = captured_display(self.guitar)
        self.assertIn("ID: P100", output)       # from Product (parent)
        self.assertIn("Price: $350.00", output)  # from Product (parent)
        self.assertIn("Weight: 4.00 kg", output)  # from PhysicalProduct (child)

    def test_fulfilment_info(self):
        self.assertIn("physical shipping", self.guitar.get_fulfilment_info())

    def test_is_a_product_and_can_be_shipped(self):
        self.assertIsInstance(self.guitar, Product)
        self.assertIsInstance(self.guitar, CanBeShipped)

    def test_shipping_cost_for_different_weights(self):
        # $5.00 base fee + $2.00 per kg
        self.assertAlmostEqual(PhysicalProduct("A", "Pen", 1, 1, 0).calculate_shipping_cost(), 5.00)
        self.assertAlmostEqual(PhysicalProduct("B", "Laptop", 1, 1, 2.5).calculate_shipping_cost(), 10.00)
        self.assertAlmostEqual(PhysicalProduct("C", "Dumbbell", 1, 1, 20).calculate_shipping_cost(), 45.00)

    def test_negative_weight_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("X", "Bad", 1, 1, -1)


class TestDigitalProduct(unittest.TestCase):
    def setUp(self):
        self.os_product = DigitalProduct("D100", "Operating System", 199.99, 100, 5120)

    def test_stores_download_size(self):
        self.assertEqual(self.os_product.get_download_size(), 5120)

    def test_display_includes_parent_and_child_info(self):
        output = captured_display(self.os_product)
        self.assertIn("ID: D100", output)
        self.assertIn("Download Size: 5120.00 MB", output)

    def test_fulfilment_info(self):
        self.assertIn("delivered digitally", self.os_product.get_fulfilment_info())

    def test_not_shippable(self):
        self.assertNotIsInstance(self.os_product, CanBeShipped)
        self.assertFalse(hasattr(self.os_product, "calculate_shipping_cost"))


class TestAbstractClasses(unittest.TestCase):
    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("P1", "Generic", 10, 1)

    def test_can_be_shipped_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            CanBeShipped()


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_product(PhysicalProduct("P1", "Laptop", 1200, 15, 2.5))
        self.inventory.add_product(DigitalProduct("D1", "Game", 59.99, 50, 800))

    def test_add_and_search_both_types(self):
        self.assertIsInstance(self.inventory.search_product("P1"), PhysicalProduct)
        self.assertIsInstance(self.inventory.search_product("D1"), DigitalProduct)
        self.assertIsNone(self.inventory.search_product("ZZZ"))

    def test_duplicate_id_rejected(self):
        self.assertFalse(self.inventory.add_product(DigitalProduct("P1", "Dup", 1, 1, 1)))

    def test_update_stock(self):
        product = self.inventory.search_product("D1")
        product.update_stock(75)
        self.assertEqual(product.get_stock(), 75)
        with self.assertRaises(ValueError):
            product.update_stock(-5)


class TestJsonPersistence(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".json")
        os.close(handle)

    def tearDown(self):
        os.remove(self.path)

    def test_save_and_load_preserves_types(self):
        original = Inventory()
        original.add_product(PhysicalProduct("P1", "Guitar", 350, 5, 4.0))
        original.add_product(DigitalProduct("D1", "Operating System", 199.99, 100, 5120))
        FileHandler(self.path).save(original)

        restored = Inventory()  # simulates restarting the program
        FileHandler(self.path).load(restored)

        guitar = restored.search_product("P1")
        os_product = restored.search_product("D1")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertEqual(guitar.get_weight(), 4.0)
        self.assertEqual(guitar.get_stock(), 5)
        self.assertIsInstance(os_product, DigitalProduct)
        self.assertEqual(os_product.get_download_size(), 5120)
        self.assertEqual(os_product.get_price(), 199.99)

    def test_saved_json_has_type_identifier(self):
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P1", "Guitar", 350, 5, 4.0))
        inventory.add_product(DigitalProduct("D1", "Game", 59.99, 50, 800))
        FileHandler(self.path).save(inventory)
        with open(self.path) as file:
            content = file.read()
        self.assertIn('"type": "physical"', content)
        self.assertIn('"type": "digital"', content)


if __name__ == "__main__":
    unittest.main(verbosity=2)

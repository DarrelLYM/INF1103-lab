"""Lab 9 Section 3: Factory pattern for creating products."""
from __future__ import annotations

import ast
import inspect
import unittest

import file_handler
import inventory_manager
import product_loader
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10,
                                        self.supplier, 1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.weight, 1.2)
        self.assertIs(product.supplier, self.supplier)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100,
                                        self.supplier, 850)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.download_size, 850)

    def test_extra_value_is_optional(self):
        product = ProductFactory.create("physical", "P003", "Monitor Stand", 39.50, 7,
                                        self.supplier)
        self.assertEqual(product.weight, 0.0)

    def test_returns_product_type(self):
        hints = inspect.get_annotations(ProductFactory.create, eval_str=True)
        self.assertIs(hints["return"], Product)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_client_code_does_not_create_products_directly(self):
        """Only the factory calls the PhysicalProduct/DigitalProduct constructors."""
        for module in (inventory_manager, file_handler, product_loader):
            tree = ast.parse(inspect.getsource(module))
            direct_calls = [node.func.id for node in ast.walk(tree)
                            if isinstance(node, ast.Call)
                            and isinstance(node.func, ast.Name)
                            and node.func.id in ("PhysicalProduct", "DigitalProduct")]
            self.assertEqual(direct_calls, [], module.__name__)


if __name__ == "__main__":
    unittest.main(verbosity=2)

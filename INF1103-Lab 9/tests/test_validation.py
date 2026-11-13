"""Lab 9 Section 4: validation rules, each kept in the class that owns it."""
from __future__ import annotations

import unittest

from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from supplier import Supplier


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")
        self.lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10,
                                          self.supplier, 1.2)

    def test_price_must_be_greater_than_zero(self):
        for product_type in ("physical", "digital"):
            for price in (0, -5):
                with self.assertRaises(ValueError) as context:
                    ProductFactory.create(product_type, "X1", "Bad", price, 5, self.supplier, 1)
                self.assertEqual(str(context.exception), "Price must be greater than zero.")

    def test_price_must_be_a_number(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "X1", "Bad", "abc", 5, self.supplier, 1)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("physical", "X1", "Bad", 10, -1, self.supplier, 1)
        self.assertEqual(str(context.exception), "Stock quantity cannot be negative.")

    def test_digital_product_keeps_the_stock_rule(self):
        """LSP: a subclass must not skip the rule its parent promises."""
        app = ProductFactory.create("digital", "D1", "App", 10, 5, self.supplier, 1)
        with self.assertRaises(ValueError):
            app.update_stock(-3)
        self.assertEqual(app.stock_quantity, 5)          # unchanged
        app.update_stock(0)
        self.assertEqual(app.stock_quantity, 0)

    def test_valid_edge_values_accepted(self):
        product = ProductFactory.create("digital", "D2", "Cheap App", 0.01, 0, self.supplier, 1)
        self.assertEqual(product.stock_quantity, 0)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        for quantity in (0, -2):
            with self.assertRaises(ValueError) as context:
                OrderLine(self.lamp, quantity)
            self.assertEqual(str(context.exception), "Quantity must be greater than zero.")

    def test_rejected_line_is_not_added_to_order(self):
        order = Order("ORD001")
        with self.assertRaises(ValueError):
            order.add_order_line(self.lamp, 0)
        self.assertEqual(order.order_lines, ())


if __name__ == "__main__":
    unittest.main(verbosity=2)

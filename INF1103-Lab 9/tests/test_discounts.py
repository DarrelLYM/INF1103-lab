"""Lab 9 Section 2: Strategy pattern for order discounts."""
from __future__ import annotations

import ast
import inspect
import unittest

import order as order_module
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def make_order(total_quantity: int, discount: DiscountStrategy | None = None) -> Order:
    """An order of Desk Lamps at $25.00 each."""
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")
    lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 100, supplier, 1.2)
    order = Order("ORD001", discount)
    order.add_order_line(lamp, total_quantity)
    return order


class TestStrategies(unittest.TestCase):
    def test_discount_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_every_strategy_is_a_discount_strategy(self):
        for strategy in (NoDiscount(), PercentageDiscount(10),
                         BulkDiscount(200, 20), StudentDiscount()):
            self.assertIsInstance(strategy, DiscountStrategy)

    def test_no_discount(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)
        self.assertAlmostEqual(PercentageDiscount(100).apply(80), 0)

    def test_bulk_discount_at_and_below_threshold(self):
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(250), 230)
        self.assertEqual(bulk.apply(200), 180)       # "200 or more"
        self.assertEqual(bulk.apply(199.99), 199.99)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(250), 237.5)

    def test_invalid_strategy_values_rejected(self):
        for bad in (lambda: PercentageDiscount(0), lambda: PercentageDiscount(150),
                    lambda: BulkDiscount(200, 0), lambda: BulkDiscount(10, 20)):
            with self.assertRaises(ValueError):
                bad()


class TestOrderUsesStrategy(unittest.TestCase):
    def test_default_is_no_discount(self):
        order = make_order(10)
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250)

    def test_predict_first_250_order(self):
        order = make_order(10, BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)
        self.assertAlmostEqual(order.calculate_subtotal(), 250)

    def test_new_strategy_needs_no_change_to_order(self):
        class HalfPrice(DiscountStrategy):     # defined only inside this test
            def apply(self, total: float) -> float:
                return total / 2

        self.assertAlmostEqual(make_order(10, HalfPrice()).calculate_total(), 125)

    def test_two_orders_can_share_one_strategy(self):
        shared = PercentageDiscount(10)
        order_a, order_b = make_order(4, shared), make_order(8, shared)
        self.assertIs(order_a.discount, order_b.discount)
        self.assertAlmostEqual(order_a.calculate_total(), 90)
        self.assertAlmostEqual(order_b.calculate_total(), 180)

    def test_order_has_no_discount_if_elif_logic(self):
        tree = ast.parse(inspect.getsource(order_module))
        order_class = next(node for node in tree.body
                           if isinstance(node, ast.ClassDef) and node.name == "Order")
        method = next(node for node in order_class.body
                      if isinstance(node, ast.FunctionDef) and node.name == "calculate_total")
        self.assertFalse(any(isinstance(node, ast.If) for node in ast.walk(method)))
        # Order only knows the abstract type and the default
        for name in ("PercentageDiscount", "BulkDiscount", "StudentDiscount"):
            self.assertNotIn(name, inspect.getsource(order_module))


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""Lab 8 tests (Section 9: Testing and review).

Run with:  python -m unittest -v test_lab8
"""
from __future__ import annotations

import io
import os
import tempfile
import typing
import unittest
from contextlib import redirect_stdout

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order_line import OrderLine
from order import Order
from file_handler import FileHandler


def captured_output(function, *args) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        function(*args)
    return buffer.getvalue()


def make_supplier() -> Supplier:
    return Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")


class TestAssociation(unittest.TestCase):
    """Supplier and Product are associated and exist independently."""

    def test_product_stores_reference_to_same_supplier(self):
        supplier = make_supplier()
        laptop = PhysicalProduct("P1", "Laptop", 1200, 15, supplier, 2.5)
        game = DigitalProduct("D1", "Game", 59.99, 50, supplier, 800)
        self.assertIs(laptop.supplier, supplier)
        self.assertIs(game.supplier, supplier)

    def test_supplier_exists_without_products(self):
        supplier = make_supplier()
        self.assertIn("TechWorld", captured_output(supplier.display_information))

    def test_product_keeps_supplier_after_variable_deleted(self):
        supplier = make_supplier()
        laptop = PhysicalProduct("P1", "Laptop", 1200, 15, supplier, 2.5)
        del supplier
        self.assertEqual(laptop.supplier.name, "TechWorld Pte Ltd")

    def test_display_shows_supplier_name(self):
        laptop = PhysicalProduct("P1", "Laptop", 1200, 15, make_supplier(), 2.5)
        self.assertIn("Supplier: TechWorld Pte Ltd",
                      captured_output(laptop.display_information))


class TestAggregation(unittest.TestCase):
    """Inventory aggregates Products; removing does not destroy them."""

    def setUp(self):
        self.guitar = PhysicalProduct("P2", "Guitar", 350, 5, make_supplier(), 4.0)
        self.inventory_a = Inventory("A")
        self.inventory_b = Inventory("B")

    def test_product_moves_between_inventories(self):
        self.inventory_a.add_product(self.guitar)
        removed = self.inventory_a.remove_product("P2")
        self.assertIs(removed, self.guitar)
        self.assertIsNone(self.inventory_a.find_product("P2"))
        self.guitar.update_stock(7)               # still usable
        self.assertEqual(self.guitar.stock_quantity, 7)
        self.inventory_b.add_product(self.guitar)
        self.assertIs(self.inventory_b.find_product("P2"), self.guitar)

    def test_clearing_inventory_keeps_products(self):
        self.inventory_a.add_product(self.guitar)
        self.inventory_a.clear()
        self.assertEqual(self.inventory_a.count(), 0)
        self.assertEqual(self.guitar.name, "Guitar")

    def test_find_and_remove_missing_return_none(self):
        self.assertIsNone(self.inventory_a.find_product("ZZZ"))
        self.assertIsNone(self.inventory_a.remove_product("ZZZ"))

    def test_duplicate_id_rejected(self):
        self.assertTrue(self.inventory_a.add_product(self.guitar))
        copy = DigitalProduct("P2", "Dup", 1, 1, make_supplier(), 1)
        self.assertFalse(self.inventory_a.add_product(copy))

    def test_products_property_returns_copy(self):
        self.inventory_a.add_product(self.guitar)
        self.inventory_a.products.clear()
        self.assertEqual(self.inventory_a.count(), 1)


class TestComposition(unittest.TestCase):
    """Order creates and manages its own OrderLines."""

    def setUp(self):
        supplier = make_supplier()
        self.laptop = PhysicalProduct("P1", "Laptop", 1200, 15, supplier, 2.5)
        self.game = DigitalProduct("D1", "Game", 59.99, 50, supplier, 800)

    def test_order_creates_order_lines(self):
        order = Order("O1")
        order.add_order_line(self.laptop, 2)
        self.assertEqual(len(order.order_lines), 1)
        self.assertIsInstance(order.order_lines[0], OrderLine)
        self.assertIs(order.order_lines[0].product, self.laptop)

    def test_subtotal_and_total(self):
        order = Order("O1")
        order.add_order_line(self.laptop, 2)
        order.add_order_line(self.game, 3)
        self.assertAlmostEqual(order.order_lines[1].calculate_subtotal(), 179.97)
        self.assertAlmostEqual(order.calculate_total(), 2400 + 179.97)

    def test_same_product_in_two_orders(self):
        order_1, order_2 = Order("O1"), Order("O2")
        order_1.add_order_line(self.laptop, 1)
        order_2.add_order_line(self.laptop, 1)
        self.assertIsNot(order_1.order_lines[0], order_2.order_lines[0])
        self.assertIs(order_1.order_lines[0].product, order_2.order_lines[0].product)

    def test_order_lines_cannot_be_changed_from_outside(self):
        order = Order("O1")
        order.add_order_line(self.laptop, 1)
        self.assertIsInstance(order.order_lines, tuple)

    def test_remove_line_and_cancel(self):
        order = Order("O1")
        order.add_order_line(self.laptop, 1)
        order.add_order_line(self.game, 1)
        self.assertTrue(order.remove_order_line("P1"))
        self.assertFalse(order.remove_order_line("P1"))
        self.assertEqual(len(order.order_lines), 1)
        order.cancel()
        self.assertEqual(order.order_lines, ())
        self.assertEqual(order.calculate_total(), 0)
        self.assertEqual(self.laptop.name, "Laptop")   # Product not owned

    def test_invalid_quantity_rejected(self):
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(self.laptop, 0)


class TestTypeHints(unittest.TestCase):
    """Type hints are present and match the UML design."""

    def test_key_type_hints(self):
        self.assertIs(typing.get_type_hints(Product.__init__)["supplier"], Supplier)
        self.assertEqual(typing.get_type_hints(Inventory.find_product)["return"],
                         typing.Optional[Product])
        self.assertIs(typing.get_type_hints(Inventory.add_product)["product"], Product)
        self.assertIs(typing.get_type_hints(OrderLine.__init__)["quantity"], int)
        self.assertIs(typing.get_type_hints(OrderLine.calculate_subtotal)["return"], float)
        self.assertIs(typing.get_type_hints(Order.add_order_line)["return"], type(None))


class TestLiskovAndPolymorphism(unittest.TestCase):
    """Both subclasses can stand in for Product."""

    def setUp(self):
        supplier = make_supplier()
        self.products: list[Product] = [
            PhysicalProduct("P1", "Laptop", 1200, 15, supplier, 2.5),
            DigitalProduct("D1", "Game", 59.99, 50, supplier, 800),
        ]

    def test_update_stock_same_meaning_for_every_subclass(self):
        for product in self.products:
            product.update_stock(0)
            self.assertEqual(product.stock_quantity, 0)
            product.update_stock(42)
            self.assertEqual(product.stock_quantity, 42)
            with self.assertRaises(ValueError):
                product.update_stock(-1)

    def test_polymorphic_calls_through_product_references(self):
        inventory = Inventory()
        for product in self.products:
            self.assertTrue(inventory.add_product(product))
        results = [p.get_fulfilment_info() for p in inventory.products]
        self.assertIn("physical shipping", results[0])
        self.assertIn("delivered digitally", results[1])
        output = captured_output(inventory.display_all_products)
        self.assertIn("Weight: 2.50 kg", output)
        self.assertIn("Download Size: 800.00 MB", output)

    def test_every_product_can_be_ordered(self):
        order = Order("O1")
        for product in self.products:
            order.add_order_line(product, 1)
        self.assertAlmostEqual(order.calculate_total(), 1259.99)

    def test_product_is_abstract(self):
        with self.assertRaises(TypeError):
            Product("X", "Generic", 1, 1, make_supplier())


class TestJsonPersistence(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".json")
        os.close(handle)

    def tearDown(self):
        os.remove(self.path)

    def test_save_and_load_keeps_types_and_shared_supplier(self):
        supplier = make_supplier()
        spare = Supplier("S009", "Spare Supplier", "spare@example.com")
        original = Inventory()
        original.add_product(PhysicalProduct("P1", "Guitar", 350, 5, supplier, 4.0))
        original.add_product(DigitalProduct("D1", "OS", 199.99, 100, supplier, 5120))
        FileHandler(self.path).save(original, [supplier, spare])

        restored = Inventory()
        suppliers = FileHandler(self.path).load(restored)

        self.assertEqual(len(suppliers), 2)      # unused supplier still saved
        guitar = restored.find_product("P1")
        os_product = restored.find_product("D1")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertIsInstance(os_product, DigitalProduct)
        self.assertEqual(guitar.weight, 4.0)
        self.assertEqual(guitar.supplier.contact_email, "sales@techworld.example.com")
        self.assertIs(guitar.supplier, os_product.supplier)   # one shared Supplier


if __name__ == "__main__":
    unittest.main(verbosity=2)

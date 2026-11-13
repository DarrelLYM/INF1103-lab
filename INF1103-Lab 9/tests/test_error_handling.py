"""Lab 9 Section 5: exception handling for user input and files."""
from __future__ import annotations

import ast
import inspect
import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import input_helpers
import inventory_manager
import product_loader
from file_handler import FileHandler
from input_helpers import get_positive_float, get_non_negative_int, get_positive_int
from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

LAB_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "products.csv")


def run_with_input(function, entries: list[str], *args):
    """Call function with input() answered from entries; return (result, output)."""
    buffer = io.StringIO()
    with patch("builtins.input", side_effect=entries), redirect_stdout(buffer):
        result = function(*args)
    return result, buffer.getvalue()


class TestUserInput(unittest.TestCase):
    def test_predict_first_abc_then_minus_5_then_12_50(self):
        value, output = run_with_input(get_positive_float, ["abc", "-5", "12.50"], "Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_not_positive(self):
        value, output = run_with_input(get_positive_float, ["0", "3"], "Price: ")
        self.assertEqual(value, 3.0)
        self.assertIn("greater than zero", output)

    def test_integer_helpers_ask_again(self):
        value, output = run_with_input(get_non_negative_int, ["2.5", "-1", "0"], "Stock: ")
        self.assertEqual(value, 0)
        self.assertEqual(len(output.splitlines()), 2)
        value, _ = run_with_input(get_positive_int, ["x", "0", "4"], "Qty: ")
        self.assertEqual(value, 4)


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")
        self.inventory = Inventory()

    def tearDown(self):
        shutil.rmtree(self.folder)

    def load(self, path: str) -> str:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products(path, self.inventory, self.supplier)
        return buffer.getvalue()

    def test_lab_csv_skips_bad_rows_and_loads_the_rest(self):
        output = self.load(LAB_CSV)
        lines = output.splitlines()
        self.assertEqual(self.inventory.count(), 3)
        for product_id in ("P001", "D001", "P003"):
            self.assertIsNotNone(self.inventory.find_product(product_id))
        self.assertIsNone(self.inventory.find_product("S001"))
        self.assertIsNone(self.inventory.find_product("P002"))
        self.assertIn("Unknown product type: service", lines[0])
        self.assertIn("could not convert string to float: 'abc'", lines[1])
        self.assertEqual(lines[-2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_is_handled(self):
        output = self.load(os.path.join(self.folder, "missing.csv"))
        self.assertEqual(self.inventory.count(), 0)
        self.assertIn("Products file not found", output)
        self.assertNotIn("products loaded", output)          # else did not run
        self.assertTrue(output.rstrip().endswith("Load attempt finished."))

    def test_short_rows_blank_lines_and_duplicates(self):
        path = os.path.join(self.folder, "products.csv")
        with open(path, "w", newline="") as file:
            file.write("product_type,product_id,name,price,stock_quantity\n"
                       "physical,P1,Lamp,10,1\n"
                       "\n"
                       "digital,D1,App\n"
                       "physical,P1,Lamp again,12,1\n"
                       "digital,D2,Game,-4,1\n")
        output = self.load(path)
        self.assertEqual(self.inventory.count(), 1)
        self.assertIn("already exists", output)
        self.assertIn("Price must be greater than zero.", output)
        self.assertIn("1 products loaded.", output)


class TestInventoryFile(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".json")
        os.close(handle)

    def tearDown(self):
        os.remove(self.path)

    def start(self) -> tuple[Inventory, str]:
        inventory = Inventory()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            inventory_manager.load_inventory(inventory, FileHandler(self.path))
        return inventory, buffer.getvalue()

    def test_missing_inventory_file_starts_fresh(self):
        os.remove(self.path)
        inventory, output = self.start()
        self.assertIn("Starting fresh", output)
        self.assertEqual(inventory.count(), 3)
        open(self.path, "w").close()                      # so tearDown can remove it

    def test_damaged_inventory_file_starts_fresh(self):
        with open(self.path, "w") as file:
            file.write("{not valid json")
        inventory, output = self.start()
        self.assertIn("could not be read", output)
        self.assertEqual(inventory.count(), 3)

    def test_bad_product_record_is_skipped(self):
        data = {"suppliers": [{"id": "S1", "name": "A", "contact_email": "a@x.com"}],
                "products": [
                    {"id": "P1", "name": "Ok", "price": 5, "stock": 1,
                     "supplier_id": "S1", "type": "physical", "weight": 1},
                    {"id": "X1", "name": "Bad", "price": 5, "stock": 1,
                     "supplier_id": "S1", "type": "service"}]}
        with open(self.path, "w") as file:
            json.dump(data, file)
        inventory, output = self.start()
        self.assertEqual(inventory.count(), 1)
        self.assertIn("Skipping record X1: Unknown product type: service", output)


class TestSpecificExceptions(unittest.TestCase):
    def test_no_bare_or_broad_except(self):
        for module in (input_helpers, product_loader, inventory_manager):
            tree = ast.parse(inspect.getsource(module))
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    self.assertIsNotNone(node.type, f"bare except in {module.__name__}")
                    names = ast.unparse(node.type)
                    self.assertNotIn("Exception", names, module.__name__)


if __name__ == "__main__":
    unittest.main(verbosity=2)

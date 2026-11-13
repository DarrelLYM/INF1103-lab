"""Lab 9 demonstration: Strategy, Factory, validation and exception handling.
Each section matches a section of the lab sheet and is used to check the
"Predict first" answers.

Run with:  python lab9_demo.py
"""
from __future__ import annotations

import os
import traceback
from unittest.mock import patch

from supplier import Supplier
from product import Product
from product_factory import ProductFactory
from inventory import Inventory
from order import Order
from discount_strategy import (NoDiscount, PercentageDiscount, BulkDiscount,
                               StudentDiscount)
from input_helpers import get_positive_float
from product_loader import load_products


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


def make_supplier() -> Supplier:
    return Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")


def demo_strategy() -> None:
    heading("SECTION 2 - STRATEGY: order discounts")
    lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 50,
                                 make_supplier(), 1.2)

    order = Order("ORD001", BulkDiscount(200, 20))
    order.add_order_line(lamp, 10)                     # 10 x $25.00 = $250.00
    print(f"Order lines add up to:                      ${order.calculate_subtotal():.2f}")
    print(f"With BulkDiscount(200, 20):                 ${order.calculate_total():.2f}")

    order.set_discount(PercentageDiscount(10))
    print(f"After set_discount(PercentageDiscount(10)): ${order.calculate_total():.2f}")

    print("\nSection 2.4 - StudentDiscount added without changing Order:")
    order.set_discount(StudentDiscount())
    order.display_order()

    print("\nAn order created without a strategy uses NoDiscount():")
    plain = Order("ORD002")
    plain.add_order_line(lamp, 2)
    print(f"  discount = {type(plain.discount).__name__}, "
          f"total = ${plain.calculate_total():.2f}")

    print("\nOne PercentageDiscount object shared by two orders:")
    ten_percent = PercentageDiscount(10)
    order_a = Order("ORD003", ten_percent)
    order_b = Order("ORD004", ten_percent)
    order_a.add_order_line(lamp, 4)                    # $100 -> $90
    order_b.add_order_line(lamp, 8)                    # $200 -> $180
    print(f"  order_a.discount is order_b.discount -> "
          f"{order_a.discount is order_b.discount}")
    print(f"  ORD003 total ${order_a.calculate_total():.2f}, "
          f"ORD004 total ${order_b.calculate_total():.2f}")
    del order_a
    print(f"  After 'del order_a' the strategy still works: "
          f"{ten_percent.apply(50):.2f}")

    print("\nBulkDiscount below the threshold changes nothing:")
    small = Order("ORD005", BulkDiscount(200, 20))
    small.add_order_line(lamp, 7)                      # $175 < $200
    print(f"  $175.00 -> ${small.calculate_total():.2f}")
    print(f"  NoDiscount().apply(99.5) -> {NoDiscount().apply(99.5)}")


def demo_factory() -> None:
    heading("SECTION 3 - FACTORY: creating products")
    supplier = make_supplier()
    products: list[Product] = [
        ProductFactory.create("physical", "P010", "Office Chair", 89.00, 12, supplier, 7.5),
        ProductFactory.create("digital", "D010", "Photo Editor", 49.90, 100, supplier, 850),
    ]
    for product in products:                           # only the Product type is used
        print(f"{type(product).__name__:<16} -> {product.get_fulfilment_info()}")

    print('\nPredict first: ProductFactory.create("service", ...)')
    try:
        ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
    except ValueError:
        # Show where it was raised, as an uncaught exception would
        print(traceback.format_exc().rstrip())
        print("(Caught here for the demo. With no except, the program would stop "
              "with this traceback.)")


def demo_validation() -> None:
    heading("SECTION 4 - VALIDATION")
    supplier = make_supplier()
    lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier, 1.2)
    attempts = [
        ("price 0", lambda: ProductFactory.create("physical", "X1", "Free", 0, 5, supplier, 1)),
        ("price -5", lambda: ProductFactory.create("digital", "X2", "Bad", -5, 5, supplier, 1)),
        ("stock -1", lambda: ProductFactory.create("physical", "X3", "Bad", 10, -1, supplier, 1)),
        ("update_stock(-3) on a DigitalProduct",
         lambda: ProductFactory.create("digital", "X4", "App", 10, 5, supplier, 1).update_stock(-3)),
        ("order quantity 0", lambda: Order("ORD9").add_order_line(lamp, 0)),
    ]
    for label, attempt in attempts:
        try:
            attempt()
            print(f"{label:<38} -> accepted")
        except ValueError as error:
            print(f"{label:<38} -> ValueError: {error}")


def demo_user_input() -> None:
    heading("SECTION 5.1 - get_positive_float()")
    entries = ["abc", "-5", "12.50"]

    def fake_input(prompt: str) -> str:
        value = entries.pop(0)
        print(f"{prompt}{value}")
        return value

    with patch("builtins.input", fake_input):
        value = get_positive_float("Price: ")
    print(f"Returned value: {value!r}")


def demo_load_products() -> None:
    heading("SECTION 5.2 - load_products() with products.csv")
    supplier = make_supplier()
    inventory = Inventory("CSV Inventory")
    load_products("products.csv", inventory, supplier)
    inventory.display_all_products()

    heading("SECTION 5.2 - load_products() after renaming products.csv")
    os.rename("products.csv", "products_renamed.csv")
    try:
        load_products("products.csv", Inventory("Empty"), supplier)
    finally:
        os.rename("products_renamed.csv", "products.csv")


if __name__ == "__main__":
    demo_strategy()
    demo_factory()
    demo_validation()
    demo_user_input()
    demo_load_products()

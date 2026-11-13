from __future__ import annotations

import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Read products from a CSV file and add them to the inventory.

    Expected columns: product_type,product_id,name,price,stock_quantity

    - A missing file is reported and nothing is loaded (except).
    - Each row is created on its own, so one bad row (unknown type, a price
      that is not a number, a missing column) is reported and skipped and
      the rest still load (else).
    - "Load attempt finished." always prints (finally).
    """
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)                       # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue                         # ignore blank lines
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id,
                                                    name, price, stock, supplier)
                except ValueError as error:
                    print(f"Row {line_number} skipped ({','.join(row)}): {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Row {line_number} skipped: product ID "
                          f"{product_id} already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")

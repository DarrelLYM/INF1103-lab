from __future__ import annotations

import json
import os

from supplier import Supplier
from product import Product
from product_factory import ProductFactory
from inventory import Inventory


class FileHandler:
    """Loads and saves inventory data to a JSON file (SRP: persistence only).

    File layout:
        {"suppliers": [...], "products": [... each with a "supplier_id" ...]}

    Suppliers are saved once in their own list and products only store the
    supplier's ID. On loading, each product is linked back to the SAME
    Supplier object, so products from one supplier share one Supplier.

    Products are created through ProductFactory, so this class does not
    need to know about PhysicalProduct or DigitalProduct.
    """

    def __init__(self, filename: str = "inventory.json") -> None:
        self.__filename: str = filename

    def file_exists(self) -> bool:
        return os.path.exists(self.__filename)

    def load(self, inventory: Inventory) -> list[Supplier]:
        """Fill the inventory from the JSON file and return the suppliers.

        Raises FileNotFoundError if the file is missing and
        json.JSONDecodeError if it is not valid JSON. The caller decides
        what to do about those. A single bad product record is reported
        and skipped so the rest still load.
        """
        with open(self.__filename, "r") as file:
            data = json.load(file)

        suppliers: dict[str, Supplier] = {}
        for item in data.get("suppliers", []):
            supplier = Supplier(item["id"], item["name"], item["contact_email"])
            suppliers[supplier.supplier_id] = supplier

        for item in data.get("products", []):
            supplier = suppliers.get(item.get("supplier_id"))
            if supplier is None:
                print(f"Skipping record {item.get('id')}: unknown supplier "
                      f"'{item.get('supplier_id')}'.")
                continue
            product = self.__create_product(item, supplier)
            if product is not None:
                inventory.add_product(product)
        return list(suppliers.values())

    def save(self, inventory: Inventory, suppliers: list[Supplier]) -> None:
        """Write every supplier and every product (via to_dict()) to JSON.
        Suppliers used by a product are always saved, even if they are
        missing from the suppliers list."""
        all_suppliers: dict[str, Supplier] = {s.supplier_id: s for s in suppliers}
        for product in inventory.products:
            all_suppliers.setdefault(product.supplier.supplier_id, product.supplier)

        data = {
            "suppliers": [s.to_dict() for s in all_suppliers.values()],
            "products": [p.to_dict() for p in inventory.products],
        }
        with open(self.__filename, "w") as file:
            json.dump(data, file, indent=4)

    def __create_product(self, item: dict, supplier: Supplier) -> Product | None:
        # Physical records store "weight", digital records store "download_size"
        extra = item.get("weight", item.get("download_size", 0.0))
        try:
            return ProductFactory.create(item.get("type", ""), item["id"],
                                         item["name"], item["price"],
                                         item["stock"], supplier, extra)
        except KeyError as error:
            print(f"Skipping record {item.get('id')}: missing field {error}.")
        except ValueError as error:
            print(f"Skipping record {item.get('id')}: {error}")
        return None

from __future__ import annotations

import json
import os

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


class FileHandler:
    """Loads and saves inventory data to a JSON file (SRP: persistence only).

    File layout:
        {"suppliers": [...], "products": [... each with a "supplier_id" ...]}

    Suppliers are saved once in their own list and products only store the
    supplier's ID. On loading, each product is linked back to the SAME
    Supplier object, so products from one supplier share one Supplier.
    """

    def __init__(self, filename: str = "inventory.json") -> None:
        self.__filename: str = filename

    def file_exists(self) -> bool:
        return os.path.exists(self.__filename)

    def load(self, inventory: Inventory) -> list[Supplier]:
        """Fill the inventory from the JSON file and return the suppliers."""
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
        product_type = item.get("type")
        if product_type == "physical":
            return PhysicalProduct(item["id"], item["name"], item["price"],
                                   item["stock"], supplier, item["weight"])
        if product_type == "digital":
            return DigitalProduct(item["id"], item["name"], item["price"],
                                  item["stock"], supplier, item["download_size"])
        print(f"Skipping record {item.get('id')}: unknown product type '{product_type}'.")
        return None

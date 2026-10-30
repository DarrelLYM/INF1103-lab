import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class FileHandler:
    """Loads and saves inventory data to a JSON file (SRP: persistence only)."""

    def __init__(self, filename="inventory.json"):
        self.__filename = filename

    def file_exists(self):
        return os.path.exists(self.__filename)

    def load(self, inventory):
        """Read the JSON file and use each record's "type" to create the
        matching Product subclass, then add it to the inventory."""
        with open(self.__filename, "r") as file:
            data = json.load(file)
        for item in data:
            product = self.__create_product(item)
            if product is not None:
                inventory.add_product(product)

    def save(self, inventory):
        """Ask every Product for its dictionary form and write them to JSON."""
        data = [product.to_dict() for product in inventory.get_all_products()]
        with open(self.__filename, "w") as file:
            json.dump(data, file, indent=4)

    def __create_product(self, item):
        product_type = item.get("type")
        if product_type == "physical":
            return PhysicalProduct(item["id"], item["name"], item["price"],
                                   item["stock"], item["weight"])
        if product_type == "digital":
            return DigitalProduct(item["id"], item["name"], item["price"],
                                  item["stock"], item["download_size"])
        print(f"Skipping record {item.get('id')}: unknown product type '{product_type}'.")
        return None

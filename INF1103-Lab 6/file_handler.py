import json
import os

from product import Product


class FileHandler:
    """Loads and saves inventory data to a JSON file (SRP: persistence only)."""

    def __init__(self, filename="inventory.json"):
        self.__filename = filename

    def file_exists(self):
        return os.path.exists(self.__filename)

    def load(self, inventory):
        """Read the JSON file and add each record to the inventory as a Product."""
        with open(self.__filename, "r") as file:
            data = json.load(file)
        for item in data:
            inventory.add_product(
                Product(item["id"], item["name"], item["price"], item["stock"]))

    def save(self, inventory):
        """Convert every Product in the inventory to a dictionary and write to JSON."""
        data = []
        for product in inventory.get_all_products():
            data.append({
                "id": product.get_product_id(),
                "name": product.get_name(),
                "price": product.get_price(),
                "stock": product.get_stock(),
            })
        with open(self.__filename, "w") as file:
            json.dump(data, file, indent=4)

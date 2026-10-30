from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped (a PhysicalProduct is-a Product).

    Inherits from Product (single class inheritance) and implements the
    CanBeShipped interface.
    """

    BASE_SHIPPING_FEE = 5.00   # flat fee per shipment ($)
    RATE_PER_KG = 2.00         # extra cost per kilogram ($)

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        weight = float(weight)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    def get_fulfilment_info(self):
        return "This product requires physical shipping to the customer."

    def calculate_shipping_cost(self):
        """Shipping rule: $5.00 base fee + $2.00 per kg."""
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight

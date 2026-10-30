from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class for every product (SRP: one product only).

    A Product on its own cannot be created - every product must be either
    a PhysicalProduct or a DigitalProduct (see get_fulfilment_info()).
    """

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = 0
        self.update_stock(stock)

    # Read-only access to private attributes
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Set the stock to a new quantity. The Product decides what is valid."""
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        """Display the information common to every product.
        Subclasses override this and call super() to add their own details."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """Return the common product data as a dictionary (used for saving).
        Subclasses override this and call super() to add their own fields."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @abstractmethod
    def get_fulfilment_info(self):
        """Return how this product is delivered to the customer.
        Every subclass must provide its own implementation."""
        pass

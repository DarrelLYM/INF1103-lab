from __future__ import annotations

from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class for every product (SRP: one product only).

    A Product on its own cannot be created - every product must be either
    a PhysicalProduct or a DigitalProduct (see get_fulfilment_info()).

    Association: each Product stores a reference to the Supplier object
    that supplies it. The Supplier is created elsewhere and passed in.

    Expectations every subclass must keep (Liskov Substitution Principle):
      - update_stock(quantity) accepts any whole number >= 0 and afterwards
        stock_quantity equals that number. Negative numbers raise ValueError.
      - display_information() prints the product and returns None.
      - get_fulfilment_info() returns a non-empty str.
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier) -> None:
        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock_quantity: int = 0
        self.__supplier: Supplier = supplier
        self.update_stock(stock_quantity)

    # Read-only access to private attributes
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock_quantity(self) -> int:
        return self.__stock_quantity

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        """Set the stock to a new quantity. The Product decides what is valid."""
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock_quantity = quantity

    def display_information(self) -> None:
        """Display the information common to every product.
        Subclasses override this and call super() to add their own details."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock_quantity} | "
              f"Supplier: {self.__supplier.name}")

    def to_dict(self) -> dict[str, str | float | int]:
        """Return the common product data as a dictionary (used for saving).
        Only the supplier's ID is saved, because the Supplier is a separate
        object (association), not part of the product."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock_quantity,
            "supplier_id": self.__supplier.supplier_id,
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return how this product is delivered to the customer.
        Every subclass must provide its own implementation."""
        pass

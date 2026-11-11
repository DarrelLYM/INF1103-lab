from __future__ import annotations

from product import Product


class OrderLine:
    """One product and the quantity of it requested in an Order.

    Composition: an OrderLine is a PART of exactly one Order. Only
    Order.add_order_line() should create OrderLine objects - other code
    should not create them or move them to another Order.

    Association: the OrderLine refers to a Product but does NOT own it.
    The Product exists independently and may also be in an Inventory.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Order quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(f"  {self.__product.product_id:<6} {self.__product.name:<22} "
              f"x{self.__quantity:<4} @ ${self.__product.price:>9.2f} = "
              f"${self.calculate_subtotal():>10.2f}")

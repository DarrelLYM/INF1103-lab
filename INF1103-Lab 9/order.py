from __future__ import annotations

from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    """A customer order made up of OrderLine objects.

    Order and OrderLine have a COMPOSITION: the Order creates its own
    OrderLine objects inside add_order_line() and is the only thing that
    holds them. When a line is removed, or the whole Order is cancelled,
    those OrderLine objects go with it. They are never passed in from
    outside or moved to another Order.

    Order and DiscountStrategy have an ASSOCIATION (Strategy pattern): the
    order is given a strategy and uses it in calculate_total(). The strategy
    is not part of the order, can be swapped with set_discount(), and the
    same strategy object can be shared by many orders. Order has no if/elif
    logic about discount types.
    """

    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        # A read-only tuple: callers can look at the lines but cannot add,
        # remove or move them. Only the Order manages its lines.
        return tuple(self.__order_lines)

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap the discount strategy used by this order."""
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this product and add it to the order."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove (and discard) the line for this product. Returns True if
        a line was removed, False if the product was not in the order."""
        for order_line in self.__order_lines:
            if order_line.product.product_id == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def cancel(self) -> None:
        """Cancel the order. Its OrderLine objects are removed with it."""
        self.__order_lines.clear()

    def calculate_subtotal(self) -> float:
        """Total of every OrderLine before any discount."""
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        """Add up the order lines and let the strategy apply the discount."""
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        if not self.__order_lines:
            print("  (no order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"  {'SUBTOTAL':<50} ${self.calculate_subtotal():>10.2f}")
        print(f"  Discount: {self.__discount}")
        print(f"  {'TOTAL':<50} ${self.calculate_total():>10.2f}")

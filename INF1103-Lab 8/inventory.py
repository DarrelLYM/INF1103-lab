from __future__ import annotations

from product import Product


class Inventory:
    """Manages a collection of Product objects (SRP: the collection only).

    Inventory and Product have an AGGREGATION: the inventory groups products,
    but it does not create them or control their lifecycle. A Product exists
    before it is added, and still exists after it is removed, so it can be
    moved to another Inventory.

    The collection is typed with the base class Product, so it can hold any
    subclass (PhysicalProduct, DigitalProduct or a future one) and never
    needs to check which subclass it has (Liskov Substitution Principle).
    """

    def __init__(self, name: str = "Main Inventory") -> None:
        self.__name: str = name
        self.__products: list[Product] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def products(self) -> list[Product]:
        # Return a copy so outside code cannot modify the internal list
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID is already used."""
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the Product reference from this inventory and return it.
        The Product object itself is not destroyed. Returns None if not found."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with the given ID, or None if not found."""
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def clear(self) -> None:
        """Empty the inventory. Only the references are dropped; the
        products themselves still exist wherever else they are used."""
        self.__products.clear()

    def count(self) -> int:
        return len(self.__products)

    def display_all_products(self) -> None:
        """Ask every Product to display itself. Python runs the correct
        subclass version of display_information() (polymorphism)."""
        print(f"\n{self.__name}")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()

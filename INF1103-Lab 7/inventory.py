class Inventory:
    """Manages a collection of Product objects (SRP: the collection only)."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a Product. Returns False if a product with the same ID exists."""
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the Product with the given ID, or None if not found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_all_products(self):
        # Return a copy so outside code cannot modify the internal list
        return list(self.__products)

    def display_all(self):
        print("\nCurrent Inventory")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()

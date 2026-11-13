from __future__ import annotations

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """Factory pattern: the one place that decides which Product class to build.

    The rest of the program asks the factory for a Product and only works
    with the Product type, so it does not need to know about PhysicalProduct
    or DigitalProduct. Adding a new product type means changing this method
    only. That still breaks OCP inside the factory, but for a program this
    size one if/elif in one place is simpler than a registry of creators.
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               extra: float = 0.0) -> Product:
        """Create a product of the given type.

        extra is the weight in kg for a physical product, or the download
        size in MB for a digital product. Raises ValueError for an unknown
        type or any value the product itself rejects.
        """
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   supplier, extra)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  supplier, extra)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

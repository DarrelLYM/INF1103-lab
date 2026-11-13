from __future__ import annotations

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered by download (a DigitalProduct is-a Product).

    It does NOT implement CanBeShipped, as digital products are never shipped.
    It keeps the inherited update_stock() unchanged: for a digital product the
    stock is the number of licences available to sell, so "updating stock"
    still means exactly what Product promises (LSP).
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier,
                 download_size: float) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        download_size = float(download_size)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital  | Download Size: {self.__download_size:.2f} MB")

    def to_dict(self) -> dict[str, str | float | int]:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via a download link."

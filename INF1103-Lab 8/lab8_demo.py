"""Lab 8 demonstration: association, aggregation, composition, LSP and
polymorphism. Each section matches a section of the lab sheet and is used to
check the "Predict first" answers.

Run with:  python lab8_demo.py
"""
from __future__ import annotations

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


def show_product_details(product: Product) -> None:
    """Section 6.2: works with ANY Product - no subclass checks needed."""
    product.display_information()
    print(product.get_fulfilment_info())


def demo_association() -> None:
    heading("SECTION 2 - ASSOCIATION: Supplier and Product")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
    antivirus = DigitalProduct("D010", "Antivirus Licence", 49.90, 300, supplier, 350)

    print("Supplier information through each Product:")
    laptop.supplier.display_information()
    antivirus.supplier.display_information()

    print(f"\nlaptop.supplier is supplier    -> {laptop.supplier is supplier}")
    print(f"antivirus.supplier is supplier -> {antivirus.supplier is supplier}")
    print(f"Supplier and Product are separate objects -> {laptop is not supplier}")

    print("\nPredict first: running 'del supplier' ...")
    del supplier
    print("The variable 'supplier' is gone, but each Product still works:")
    laptop.supplier.display_information()
    antivirus.supplier.display_information()


def demo_aggregation() -> None:
    heading("SECTION 3 - AGGREGATION: Inventory and Product")
    supplier = Supplier("S002", "Melody Instruments", "orders@melody.example.com")
    guitar = PhysicalProduct("P002", "Guitar", 350.00, 5, supplier, 4.0)
    print("1. Product created BEFORE any inventory exists:")
    guitar.display_information()

    inventory_a = Inventory("Inventory A (Main Warehouse)")
    inventory_b = Inventory("Inventory B (Retail Store)")

    inventory_a.add_product(guitar)
    print(f"\n2. Added to Inventory A -> A has {inventory_a.count()} product(s)")

    removed = inventory_a.remove_product("P002")
    print(f"\n3. Removed from Inventory A -> A has {inventory_a.count()} product(s)")
    print(f"   Returned object is the same guitar -> {removed is guitar}")
    print("   Product still usable after removal:")
    guitar.update_stock(8)
    guitar.display_information()

    inventory_b.add_product(guitar)
    print(f"\n4. Same object added to Inventory B -> "
          f"{inventory_b.find_product('P002') is guitar}")
    inventory_b.display_all_products()

    inventory_b.clear()
    print(f"\n5. Inventory B emptied -> B has {inventory_b.count()} product(s)")
    print("   The guitar still exists:")
    guitar.display_information()


def demo_composition() -> None:
    heading("SECTION 4 - COMPOSITION: Order and OrderLine")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")
    soft = Supplier("S003", "SoftCore Licensing", "licences@softcore.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
    mouse = PhysicalProduct("P004", "Wireless Mouse", 25.50, 60, supplier, 0.1)
    office = DigitalProduct("D002", "Office Suite", 149.00, 500, soft, 3000)

    order_1 = Order("ORD001")
    order_1.add_order_line(laptop, 2)
    order_1.add_order_line(mouse, 3)
    order_1.add_order_line(office, 1)
    order_1.display_order()

    order_2 = Order("ORD002")
    order_2.add_order_line(laptop, 1)     # same Product in a second Order
    order_2.display_order()

    line_1 = order_1.order_lines[0]
    line_2 = order_2.order_lines[0]
    print("\nPredict first: same Product in two Orders")
    print(f"  OrderLine in ORD001 is OrderLine in ORD002 -> {line_1 is line_2}")
    print(f"  id(OrderLine 1) = {id(line_1)}")
    print(f"  id(OrderLine 2) = {id(line_2)}")
    print(f"  Both lines refer to the same Product   -> "
          f"{line_1.product is line_2.product is laptop}")
    print(f"  id(Product via line 1) = {id(line_1.product)}")
    print(f"  id(Product via line 2) = {id(line_2.product)}")
    print("  => 2 OrderLine objects, 1 Product object")

    print("\nRemove the Wireless Mouse line through the Order:")
    order_1.remove_order_line("P004")
    order_1.display_order()

    print("\nCancel ORD002 - its OrderLine goes with it:")
    order_2.cancel()
    order_2.display_order()
    print("The Laptop Product itself is unaffected:")
    laptop.display_information()


def demo_lsp_and_polymorphism() -> None:
    heading("SECTIONS 6 & 7 - LSP AND POLYMORPHISM")
    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")
    soft = Supplier("S003", "SoftCore Licensing", "licences@softcore.example.com")
    keyboard = PhysicalProduct("P005", "Mechanical Keyboard", 129.00, 25, supplier, 1.1)
    game = DigitalProduct("D005", "Space Game", 59.99, 1000, soft, 45000)

    print("show_product_details() with a PhysicalProduct:")
    show_product_details(keyboard)
    print("\nshow_product_details() with a DigitalProduct:")
    show_product_details(game)

    inventory = Inventory("Mixed Inventory")
    inventory.add_product(keyboard)
    inventory.add_product(game)

    print("\nOne loop over list[Product] - no isinstance(), no separate loops:")
    for product in inventory.products:
        product.display_information()
        print(product.get_fulfilment_info())

    print("\nupdate_stock() keeps the same meaning for both subclasses:")
    for product in inventory.products:
        product.update_stock(10)
        print(f"  {product.name}: stock is now {product.stock_quantity}")


if __name__ == "__main__":
    demo_association()
    demo_aggregation()
    demo_composition()
    demo_lsp_and_polymorphism()

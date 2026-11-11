from __future__ import annotations

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from file_handler import FileHandler


def choose_supplier(suppliers: list[Supplier]) -> Supplier | None:
    """Let the user pick one of the existing Supplier objects."""
    if not suppliers:
        print("No suppliers yet. Add a supplier first (option 7).")
        return None
    print("\nSuppliers")
    for number, supplier in enumerate(suppliers, start=1):
        print(f"{number}. {supplier.name} ({supplier.supplier_id})")
    choice = input("Choose supplier: ")
    if choice.isdigit() and 1 <= int(choice) <= len(suppliers):
        return suppliers[int(choice) - 1]
    print("Invalid supplier.")
    return None


def add_product(inventory: Inventory, suppliers: list[Supplier]) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type: ")
    if product_type not in ('1', '2'):
        print("Invalid product type.")
        return

    p_id = input("Product ID: ")
    if inventory.find_product(p_id) is not None:
        print(f"A product with ID {p_id} already exists.")
        return
    name = input("Product Name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == '1':
            extra = float(input("Weight (kg): "))
        else:
            extra = float(input("Download Size (MB): "))
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    try:
        product: Product
        if product_type == '1':
            product = PhysicalProduct(p_id, name, price, stock, supplier, extra)
        else:
            product = DigitalProduct(p_id, name, price, stock, supplier, extra)
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock_quantity}")
    try:
        product.update_stock(int(input("\nNew Stock Quantity: ")))
        print("\nStock updated successfully!")
    except ValueError as error:
        print(f"Invalid input: {error}")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("----------------------------------------")
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("Supplied by:")
    product.supplier.display_information()
    print("----------------------------------------")


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    removed = inventory.remove_product(input("Enter Product ID: "))
    if removed is None:
        print("Product not found.")
    else:
        print(f"{removed.name} removed from the inventory.")


def display_suppliers(suppliers: list[Supplier], inventory: Inventory) -> None:
    print("\nSuppliers")
    if not suppliers:
        print("No suppliers.")
    for supplier in suppliers:
        supplier.display_information()
        supplied = [p.name for p in inventory.products if p.supplier is supplier]
        print(f"    Supplies: {', '.join(supplied) if supplied else '(nothing in stock)'}")


def add_supplier(suppliers: list[Supplier]) -> None:
    print("\nAdd New Supplier")
    s_id = input("Supplier ID: ")
    if any(s.supplier_id == s_id for s in suppliers):
        print(f"A supplier with ID {s_id} already exists.")
        return
    name = input("Supplier Name: ")
    email = input("Contact Email: ")
    suppliers.append(Supplier(s_id, name, email))
    print("Supplier added successfully!")


def create_order(inventory: Inventory, order_number: int) -> None:
    print("\nCreate Order")
    order = Order(f"ORD{order_number:03d}")
    while True:
        p_id = input("Product ID to order (blank to finish): ")
        if p_id == "":
            break
        product = inventory.find_product(p_id)
        if product is None:
            print("Product not found.")
            continue
        try:
            quantity = int(input("Quantity: "))
            if quantity > product.stock_quantity:
                print(f"Only {product.stock_quantity} in stock.")
                continue
            order.add_order_line(product, quantity)   # Order creates the OrderLine
        except ValueError as error:
            print(f"Invalid input: {error}")
    order.display_order()


def load_inventory(inventory: Inventory, file_handler: FileHandler) -> list[Supplier]:
    if file_handler.file_exists():
        suppliers = file_handler.load(inventory)
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return suppliers

    print("No existing inventory found. Starting fresh.")
    tech = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example.com")
    music = Supplier("S002", "Melody Instruments", "orders@melody.example.com")
    soft = Supplier("S003", "SoftCore Licensing", "licences@softcore.example.com")
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, tech, 2.5))
    inventory.add_product(PhysicalProduct("P002", "Guitar", 350.00, 5, music, 4.0))
    inventory.add_product(DigitalProduct("D001", "Operating System", 199.99, 100, soft, 5120))
    return [tech, music, soft]


def save_inventory(inventory: Inventory, suppliers: list[Supplier],
                   file_handler: FileHandler) -> None:
    print("\nSaving inventory...")
    file_handler.save(inventory, suppliers)
    print("Inventory saved successfully to inventory.json.")


def main() -> None:
    inventory = Inventory("Main Inventory")
    file_handler = FileHandler("inventory.json")
    orders_created = 0

    print("INVENTORY MANAGEMENT SYSTEM (OOP)")
    suppliers = load_inventory(inventory, file_handler)

    while True:
        print("\nMENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Remove Product")
        print("6. Display Suppliers")
        print("7. Add Supplier")
        print("8. Create Order")
        print("9. Save Inventory")
        print("0. Exit")

        choice = input("Enter option: ")

        if choice == '1':
            inventory.display_all_products()
        elif choice == '2':
            add_product(inventory, suppliers)
        elif choice == '3':
            update_stock(inventory)
        elif choice == '4':
            search_product(inventory)
        elif choice == '5':
            remove_product(inventory)
        elif choice == '6':
            display_suppliers(suppliers, inventory)
        elif choice == '7':
            add_supplier(suppliers)
        elif choice == '8':
            orders_created += 1
            create_order(inventory, orders_created)
        elif choice == '9':
            save_inventory(inventory, suppliers, file_handler)
        elif choice == '0':
            print("\nSaving inventory before exit...")
            save_inventory(inventory, suppliers, file_handler)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

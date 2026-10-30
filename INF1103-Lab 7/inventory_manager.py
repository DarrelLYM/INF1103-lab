from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from file_handler import FileHandler


def add_product(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type: ")
    if product_type not in ('1', '2'):
        print("Invalid product type.")
        return

    p_id = input("Product ID: ")
    name = input("Product Name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == '1':
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(p_id, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            product = DigitalProduct(p_id, name, price, stock, download_size)
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print(f"A product with ID {p_id} already exists.")


def update_stock(inventory):
    print("\nUpdate Stock")
    p_id = input("Enter Product ID: ")
    product = inventory.search_product(p_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    try:
        product.update_stock(int(input("\nNew Stock Quantity: ")))
        print("\nStock updated successfully!")
    except ValueError as error:
        print(f"Invalid input: {error}")


def search_product(inventory):
    print("\nSearch Product")
    p_id = input("Enter Product ID: ")
    product = inventory.search_product(p_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("----------------------------------------")
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("----------------------------------------")


def load_inventory(inventory, file_handler):
    if file_handler.file_exists():
        file_handler.load(inventory)
        print("inventory.json found.")
        print("Inventory loaded successfully.")
    else:
        print("No existing inventory found. Starting fresh.")
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5))
        inventory.add_product(PhysicalProduct("P002", "Guitar", 350.00, 5, 4.0))
        inventory.add_product(DigitalProduct("D001", "Operating System", 199.99, 100, 5120))


def save_inventory(inventory, file_handler):
    print("\nSaving inventory...")
    file_handler.save(inventory)
    print("Inventory saved successfully to inventory.json.")


def main():
    inventory = Inventory()
    file_handler = FileHandler("inventory.json")

    print("INVENTORY MANAGEMENT SYSTEM (OOP)")
    load_inventory(inventory, file_handler)

    while True:
        print("\nMENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

        choice = input("Enter option: ")

        if choice == '1':
            inventory.display_all()
        elif choice == '2':
            add_product(inventory)
        elif choice == '3':
            update_stock(inventory)
        elif choice == '4':
            search_product(inventory)
        elif choice == '5':
            save_inventory(inventory, file_handler)
        elif choice == '6':
            print("\nSaving inventory before exit...")
            save_inventory(inventory, file_handler)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

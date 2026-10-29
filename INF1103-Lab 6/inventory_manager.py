from product import Product
from inventory import Inventory
from file_handler import FileHandler


def add_product(inventory):
    print("\nAdd New Product")
    p_id = input("Product ID: ")
    name = input("Product Name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        product = Product(p_id, name, price, stock)
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
    print("----------------------------------------")


def load_inventory(inventory, file_handler):
    if file_handler.file_exists():
        file_handler.load(inventory)
        print("inventory.json found.")
        print("Inventory loaded successfully.")
    else:
        print("No existing inventory found. Starting fresh.")
        inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
        inventory.add_product(Product("P002", "Mouse", 25.50, 40))
        inventory.add_product(Product("P003", "Keyboard", 45.00, 25))


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

import json
import os

# Global inventory list
inventory = []

def display_all():
    print("\nCurrent Inventory")
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")

def add_product():
    print("\nAdd New Product")
    p_id = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    inventory.append({"id": p_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")

def update_stock():
    print("\nUpdate Stock")
    p_id = input("Enter Product ID: ")
    for item in inventory:
        if item['id'] == p_id:
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}")
            new_stock = int(input("\nNew Stock Quantity: "))
            item['stock'] = new_stock
            print("\nStock updated successfully!")
            return
    print("Product not found.")

def search_product():
    print("\nSearch Product")
    p_id = input("Enter Product ID: ")
    for item in inventory:
        if item['id'] == p_id:
            print("\nProduct Found")
            print("----------------------------------------")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("----------------------------------------")
            return
    print("Product not found.")

def load_inventory():
    global inventory
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as file:
            inventory = json.load(file)
        print("inventory.json found.")
        print("Inventory loaded successfully.")
    else:
        print("No existing inventory found. Starting fresh.")
        # Pre-load with 3 products as required if empty
        inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
        ]

def save_inventory():
    print("\nSaving inventory...")
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    load_inventory()

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
            display_all()
        elif choice == '2':
            add_product()
        elif choice == '3':
            update_stock()
        elif choice == '4':
            search_product()
        elif choice == '5':
            save_inventory()
        elif choice == '6':
            print("\nSaving inventory before exit...")
            save_inventory()
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
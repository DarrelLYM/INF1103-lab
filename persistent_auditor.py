import os

def load_inventory(file_path="inventory.txt"):
    history = []
    if not os.path.exists(file_path):
        print(f"'{file_path}' not found. Starting with clean inventory.")
        return history

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    if len(parts) == 3:
                        order_id = int(parts[0])
                        product = parts[1]
                        qty = int(parts[2])
                        history.append((order_id, product, qty))
    except Exception as e:
        print(f"Error loading inventory: {e}")
    return history


def save_inventory(history, file_path="inventory.txt"):
    try:
        with open(file_path, "w") as f:
            for order in history:
                f.write(f"{order[0]}, {order[1]}, {order[2]}\n")
        print(f"Order successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving inventory: {e}")


def combine_orders(history, product_name, qty):
    for i, (order_id, name, existing_qty) in enumerate(history):
        if name.strip().lower() == product_name.strip().lower():
            history[i] = (order_id, name, existing_qty + qty)
            print(f"\nCombined with existing order {order_id}:")
            print(f"{order_id}, {name}, {history[i][2]}")
            return history

    next_id = history[-1][0] + 1 if history else 1001
    history.append((next_id, product_name, qty))
    print("\nNew Order Added:")
    print(f"{next_id}, {product_name}, {qty}")
    return history


def main():
    file_path = "inventory.txt"
    history = load_inventory(file_path)

    print("Current Orders:")
    if history:
        for order in history:
            print(f"{order[0]}, {order[1]}, {order[2]}")
    else:
        print("(No existing orders)")

    while True:
        product_name = input("\nEnter Product Name (or 'quit' to exit): ").strip()
        if product_name.lower() == 'quit':
            save_inventory(history, file_path)
            break

        if not product_name:
            print("Product name cannot be empty.")
            continue

        try:
            qty_input = input("Enter Quantity: ").strip()
            if qty_input.lower() == 'quit':
                save_inventory(history, file_path)
                break
                
            qty = int(qty_input)
            if qty <= 0:
                print("Quantity must be greater than 0.")
                continue
        except ValueError:
            print("Invalid quantity. Please enter a valid integer.")
            continue

        # Combine or append entry
        history = combine_orders(history, product_name, qty)


if __name__ == "__main__":
    main()

# def main():
#     inventory_total = 0  # 1) Initialize inventory to zero

#     failed_entries = 0  # Keep track of rejected entries

#     while True:  # 2) Continuously ask the user for stock quantities
#         stock = input("Enter stock quantity (OR type 'quit' to finish): ")

#         if stock.lower() == "quit":  # Check if the user wants to quit
#             break

#         if not stock.isdigit():  # 4) Rejecting invalid input
#             print("Error: Enter a valid integer.")
#             failed_entries += 1
#             continue

#         stock = int(stock)  # 3) Converting stock value input to an integer

#         if stock < 0:  # 5) Rejecting negative numbers
#             print("Error: Negative stock values are not allowed.")
#             failed_entries += 1
#             continue

#         inventory_total += stock  # 6) Add valid stock to the running inventory

#         print("Stock accepted.")
#         print("Current inventory:", inventory_total)

#         if inventory_total > 500:  # 7) Trigger Overstock Alert
#             print("ALERT: Inventory has exceeded 500 units!")
#             break

#     print("\n--- Final Report ---")  # 8) Reporting
#     print("Total Units Processed:", inventory_total)
#     print("Number of Failed/Rejected Entries:", failed_entries)


# if __name__ == "__main__":
#     main()
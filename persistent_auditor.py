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
    """
    Searches history for an existing product (case-insensitive).
    If found, adds qty to the existing order.
    If not found, creates a new order ID and adds the product.
    """
    for i, (order_id, name, existing_qty) in enumerate(history):
        if name.strip().lower() == product_name.strip().lower():
            # Update existing item in place
            history[i] = (order_id, name, existing_qty + qty)
            print(f"\nCombined with existing order {order_id}:")
            print(f"{order_id}, {name}, {existing_qty + qty}")
            return history

    # If product does not exist, assign a new order ID
    next_id = history[-1][0] + 1 if history else 1001
    history.append((next_id, product_name, qty))
    print("\nNew Order Added:")
    print(f"{next_id}, {product_name}, {qty}")
    return history

def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()

    if user_input.lower() == 'quit':
        return 'quit'

    try:
        val = int(user_input)
        if val < 0:
            print("Invalid entry: Stock quantity cannot be negative.")
            return 'invalid'
        return val
    except ValueError:
        print("Invalid entry: Please enter a valid integer.")
        return 'invalid'


def p_delivery(current_total, new_value):
    return current_total + new_value


def calc_tax(amount):
    return amount * 0.10


def gen_report(total_units, total_tax, failed_attempts, history):
    print("\n================ AUDIT REPORT ================")
    print(f"Transaction History        : {history}")
    print(f"Total Deliveries Processed : {total_units}")
    print(f"Total Tax Calculated       : ${total_tax:.2f}")
    print(f"Number of Failed Entries   : {failed_attempts}")
    print("==============================================")


def main():
    file_path = "inventory.txt"
    history = load_inventory(file_path)

    print("Current Orders:")
    if history:
        for order in history:
            print(f"{order[0]}, {order[1]}, {order[2]}")
    
    # Determine next order ID (starts at 1001 if history is empty)
    next_id = history[-1][0] + 1 if history else 1001

    product_name = input("Enter Product Name: ").strip()
    if product_name.lower() == 'quit':
        save_inventory(history, file_path)
        return

    try:
        qty = int(input("Enter Quantity: ").strip())
    except ValueError:
        print("Invalid quantity.")
        return

    # Add new order and save
    history.append((next_id, product_name, qty))
    print("\nNew Order Added:")
    print(f"{next_id}, {product_name}, {qty}")

    save_inventory(history, file_path)

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
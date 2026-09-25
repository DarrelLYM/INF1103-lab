import os

def load_inventory(file_path="inventory.txt"):
    """
    Loads previous transaction history from file into memory.
    If the file does not exist, starts with an empty list without error.
    """
    history = []
    if not os.path.exists(file_path):
        print(f"'{file_path}' not found. Starting with an empty inventory.")
        return history

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    history.append(float(line))
        print(f"Successfully loaded {len(history)} previous record(s) from '{file_path}'.")
    except Exception as e:
        print(f"Error loading inventory: {e}")

    return history


def save_inventory(history, file_path="inventory.txt"):
    """
    Saves the list of transaction amounts to the target file on program exit.
    """
    try:
        with open(file_path, "w") as f:
            for amount in history:
                f.write(f"{amount:.2f}\n")
        print(f"Order successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving inventory: {e}")


def display_summary(history):
    """
    Displays the history of transactions and current grand total.
    """
    print("\n--- Current Order History ---")
    if not history:
        print("No transactions recorded yet.")
    else:
        for idx, amount in enumerate(history, start=1):
            print(f"Order {idx}: ${amount:.2f}")
    
    total = sum(history)
    print(f"Total Amount: ${total:.2f}")
    print("-----------------------------\n")


def main():
    # Phase 1: Load existing inventory records into memory
    history = load_inventory("inventory.txt")

    print("=== Welcome to Persistent Auditor ===")
    
    # Show initial state upon program start
    display_summary(history)

    while True:
        user_input = input("Enter transaction amount (or type 'quit' to save & exit): ").strip()

        # Phase 3: Exit trigger
        if user_input.lower() == "quit":
            save_inventory(history, "inventory.txt")
            print("Exiting application. Goodbye!")
            break

        # Phase 2: Validate input and track history list
        try:
            amount = float(user_input)
            if amount < 0:
                print("Invalid entry: Transaction amount must be positive.")
                continue

            history.append(amount)
            print(f"Added transaction: ${amount:.2f}")
            display_summary(history)

        except ValueError:
            print("Invalid input: Please enter a valid number or 'quit'.")


if __name__ == "__main__":
    main()




# def get_valid_input():
    
#     user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()
    
#     if user_input.lower() == 'quit':
#         return 'quit'
    
#     try:
#         val = int(user_input)
#         if val < 0:
#             print("Invalid entry: Stock quantity cannot be negative.")
#             return 'invalid'
#         return val
#     except ValueError:
#         print("Invalid entry: Please enter a valid integer.")
#         return 'invalid'


# def p_delivery(current_total, new_value):
    
#     return current_total + new_value


# def calc_tax(amount):
    
#     return amount * 0.10


# def gen_report(total_units, total_tax, failed_attempts):
    
#     print("\n================ AUDIT REPORT ================")
#     print(f"Total Deliveries Processed : {total_units}")
#     print(f"Total Tax Calculated       : ${total_tax:.2f}")
#     print(f"Number of Failed/Rejected Entries : {failed_attempts}")
#     print("==============================================")


# def main():
#     running_total = 0
#     total_tax = 0.0
#     failed_attempts = 0

#     while True:
#         result = get_valid_input()

#         if result == 'quit':
#             break

#         if result == 'invalid':
#             failed_attempts += 1
#             continue

#         running_total = p_delivery(running_total, result)
#         delivery_tax = calc_tax(result)
#         total_tax += delivery_tax

#         print(f"-> Added {result} units (Tax: ${delivery_tax:.2f}). Current Total: {running_total}")

#     gen_report(running_total, total_tax, failed_attempts)


# if __name__ == "__main__":
#     main()

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
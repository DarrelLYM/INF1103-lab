def get_valid_input():
    """
    Prompts the user for input.
    Returns an integer delivery value or the string 'quit'.
    """
    while True:
        user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()
        if user_input.lower() == 'quit':
            return 'quit'
        try:
            val = int(user_input)
            if val < 0:
                print("Quantity cannot be negative.")
                continue
            return val
        except ValueError:
            print("Invalid entry. Please enter a valid integer.")

def p_delivery(current_total, new_value):
    """
    Calculates and returns the new running inventory total.
    """
    return current_total + new_value

def calculate_tax(amount):
    """
    Calculates and returns 10% tax for a given delivery amount.
    """
    return amount * 0.10

def main():
    total_inventory = 0
    failed_entries = 0

    while True:
        entry = get_valid_input()
        if entry == 'quit':
            break
        
        # Process input logic
        total_inventory = process_delivery(total_inventory, entry)
        tax = calculate_tax(entry)
        
    generate_report(total_inventory, failed_entries)

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
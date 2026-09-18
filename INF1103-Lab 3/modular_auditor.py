def main():
    inventory_total = 0  # 1) Initialize inventory to zero

    failed_entries = 0  # Keep track of rejected entries

    while True:  # 2) Continuously ask the user for stock quantities
        stock = input("Enter stock quantity (OR type 'quit' to finish): ")

        if stock.lower() == "quit":  # Check if the user wants to quit
            break

        if not stock.isdigit():  # 4) Rejecting invalid input
            print("Error: Enter a valid integer.")
            failed_entries += 1
            continue

        stock = int(stock)  # 3) Converting stock value input to an integer

        if stock < 0:  # 5) Rejecting negative numbers
            print("Error: Negative stock values are not allowed.")
            failed_entries += 1
            continue

        inventory_total += stock  # 6) Add valid stock to the running inventory

        print("Stock accepted.")
        print("Current inventory:", inventory_total)

        if inventory_total > 500:  # 7) Trigger Overstock Alert
            print("ALERT: Inventory has exceeded 500 units!")
            break

    print("\n--- Final Report ---")  # 8) Reporting
    print("Total Units Processed:", inventory_total)
    print("Number of Failed/Rejected Entries:", failed_entries)


if __name__ == "__main__":
    main()
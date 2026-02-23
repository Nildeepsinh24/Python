repair_orders = []
order_id_counter = 1

def book_repair_order():
    global order_id_counter
    print("\n--- New Repair Order Booking ---")
    
    customer_name = input("Enter customer name: ")
    device_type = input("Enter device type (e.g., Smartphone, Laptop): ")
    issue = input("Describe the issue: ")
    due_date = input("Enter the due date (e.g., 2025-10-15): ")
    
    new_order = {
        "id": order_id_counter,
        "customer": customer_name,
        "device": device_type,
        "issue": issue,
        "due_date": due_date,
        "status": "In Progress"
    }
    
    repair_orders.append(new_order)
    print(f"\n✅ Success! Repair Order #{order_id_counter} has been booked for {customer_name}.")
    order_id_counter += 1

def generate_invoice():
    print("\n--- Generate Repair Invoice ---")
    
    if not repair_orders:
        print("❌ No repair orders found in the system.")
        return

    print("Available Repair Orders:")
    for order in repair_orders:
        print(f"  ID: {order['id']} | Customer: {order['customer']} | Device: {order['device']} | Status: {order['status']}")

    try:
        order_id_to_bill = int(input("Enter the Order ID to generate an invoice for: "))
        
        target_order = None
        for order in repair_orders:
            if order['id'] == order_id_to_bill:
                target_order = order
                break
        
        if not target_order:
            print(f"❌ Error: Order ID {order_id_to_bill} not found.")
            return

        parts_cost = float(input("Enter cost of parts replaced ($): "))
        repair_fee = float(input("Enter repair fee ($): "))
        discount_input = input("Enter optional discount ($) (press Enter for none): ")
        discount = float(discount_input) if discount_input else 0.0

        subtotal = parts_cost + repair_fee
        tax_rate = 0.08
        tax_amount = subtotal * tax_rate
        final_total = subtotal + tax_amount - discount
        
        print("\n" + "="*35)
        print("      TechFix Solutions Invoice")
        print("="*35)
        print(f"Order ID:       {target_order['id']}")
        print(f"Customer:       {target_order['customer']}")
        print(f"Device:         {target_order['device']}")
        print(f"Issue:          {target_order['issue']}")
        print("-"*35)
        print(f"Parts Cost:    ${parts_cost:>10.2f}")
        print(f"Repair Fee:    ${repair_fee:>10.2f}")
        print(f"Subtotal:      ${subtotal:>10.2f}")
        print(f"Tax (8%):      ${tax_amount:>10.2f}")
        if discount > 0:
            print(f"Discount:      $-{discount:>9.2f}")
        print("-"*35)
        print(f"FINAL AMOUNT:  ${final_total:>10.2f}")
        print("="*35 + "\n")

        target_order['status'] = 'Completed & Billed'
        print(f"Invoice generated. Order #{target_order['id']} status updated.")

    except ValueError:
        print("Invalid input. Please enter valid numbers for IDs, costs, and fees.")

def main():
    print("Welcome to FixTrack - TechFix Solutions Repair Tracker")
    
    while True:
        print("\n-- Main Menu --")
        print("1. Book a New Repair Order")
        print("2. Generate an Invoice")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            book_repair_order()
        elif choice == '2':
            generate_invoice()
        elif choice == '3':
            print("Thank you for using FixTrack. Goodbye!")
            break
        else:
            print("Invalid choice. Please select an option from the menu.")
main()
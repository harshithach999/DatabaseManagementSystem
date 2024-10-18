import mysql.connector
from datetime import datetime

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000",
            database="northwind"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def add_customer(connection):
    while True:
        print("Adding a customer...")
        try:
            cursor = connection.cursor()

            # Take user input for customer details
            company = input("Enter Company: ")
            last_name = input("Enter Last Name: ")
            first_name = input("Enter First Name: ")
            email = input("Enter Email: ")
            job_title = input("Enter Job Title: ")
            business_phone = input("Enter Business Phone: ")
            address = input("Enter Address: ")
            city = input("Enter City: ")
            state = input("Enter State: ")
            zip_code = input("Enter ZIP Code: ")
            country = input("Enter Country: ")
            web = input("Enter Web: ")
            notes = input("Enter Notes: ")

            query = """
                INSERT INTO Customers 
                (Company, LastName, FirstName, Email, JobTitle, BusinessPhone, Address, City, State, ZIP, Country, Web, Notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (company, last_name, first_name, email, job_title, business_phone, address, city, state, zip_code, country, web, notes)

            cursor.execute(query, values)
            connection.commit()

            print("Customer added successfully!")

            # Ask if the user wants to add another customer
            add_another = input("Do you want to add another customer? (yes/no): ").lower()
            if add_another != 'yes':
                break  # Exit the loop if the user doesn't want to add another customer

        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error: {err}")

        finally:
            cursor.close()



def get_product_unit_price(connection, product_id):
    cursor = connection.cursor()
    query = "SELECT ListPrice FROM Products WHERE ID = %s"
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0]
    else:
        return None
def product_exists(connection, product_id):
    try:
        cursor = connection.cursor()
        query = "SELECT ID FROM Products WHERE ID = %s"
        cursor.execute(query, (product_id,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"Error in product_exists: {err}")
        return False
    finally:
        cursor.close()

def customer_exists(connection, customer_id):
    try:
        cursor = connection.cursor()
        query = "SELECT ID FROM Customers WHERE ID = %s"
        cursor.execute(query, (customer_id,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"Error in customer_exists: {err}")
        return False
    finally:
        cursor.close()


def add_order(connection, customer_id, product_quantities):
    print("Adding an order...")
    try:
        cursor = connection.cursor()

        # Check if the customer exists
        if not customer_exists(connection, customer_id):
            print(f"Customer with ID {customer_id} not found in the Customers table.")
            return

        # Populate information into the Orders table
        insert_order_query = """
            INSERT INTO Orders 
            (CustomerID, OrderDate, ShipName, ShipAddress, ShipCity, ShipState, ShipZIP, ShipCountry, ShippingFee)
            VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s)
        """

        # Hardcoding some values for simplicity
        ship_name = "Default Ship Name"
        ship_address = "Default Ship Address"
        ship_city = "Default Ship City"
        ship_state = "Default Ship State"
        ship_zip = "Default Ship ZIP"
        ship_country = "Default Ship Country"
        shipping_fee = 0  # Assuming initial shipping fee is 0

        # Insert into the Orders table
        cursor.execute(insert_order_query, (customer_id, ship_name, ship_address, ship_city, ship_state, ship_zip, ship_country, shipping_fee))
        connection.commit()

        # Get the last inserted OrderID
        order_id = cursor.lastrowid

        # Populate information into the order_details table
        insert_order_details_query = """
            INSERT INTO order_details (OrderID, ProductID, Quantity)
            VALUES (%s, %s, %s)
        """

        for product_id, quantity in product_quantities.items():
            # Check if the product exists
            if not product_exists(connection, product_id):
                print(f"Product with ID {product_id} not found in the Products table.")
                continue

            # Retrieve the UnitPrice of the product
            unit_price = get_product_unit_price(connection, product_id)

            # Insert into the order_details table
            cursor.execute(insert_order_details_query, (order_id, product_id, quantity))
            connection.commit()

        print("Order added successfully!")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")

    except ValueError as value_err:
        connection.rollback()
        print(f"ValueError: {value_err}")

    finally:
        cursor.close()



def remove_order(connection, order_id):
    print("Removing an order...")
    try:
        cursor = connection.cursor()

        # Delete entries in the order_details table
        delete_order_details_query = """
            DELETE FROM order_details
            WHERE OrderID = %s
        """

        cursor.execute(delete_order_details_query, (order_id,))
        connection.commit()

        # Delete entry in the Orders table
        delete_order_query = """
            DELETE FROM Orders
            WHERE OrderID = %s
        """

        cursor.execute(delete_order_query, (order_id,))
        connection.commit()

        print("Order removed successfully!")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")

    finally:
        cursor.close()


def ship_order(connection, order_id, shipper_id, shipping_fee):
    print("Shipping an order...")

    try:
        cursor = connection.cursor()

        # Check if there are enough units in stock for each product in the order
        if check_inventory(connection, order_id):
            # If there are enough units in stock, proceed with shipping

            # Update the orders table with ShippedDate, ShipperID, and ShippingFee
            shipped_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query_orders = """
                UPDATE orders
                SET ShippedDate = %s, ShipperID = %s, ShippingFee = %s
                WHERE OrderID = %s
            """
            values_orders = (shipped_date, shipper_id, shipping_fee, order_id)
            cursor.execute(query_orders, values_orders)

            # Update the inventory_transactions table with Sold transactions
            update_inventory(connection, order_id)

            # Insert inventory transactions for sold products
            insert_inventory_transaction_query = """
                INSERT INTO InventoryTransactions(TransactionType, TransactionDate, ProductID, Quantity)
                SELECT 'Sold', NOW(), od.ProductID, od.Quantity
                FROM order_details od
                WHERE od.OrderID = %s
            """
            cursor.execute(insert_inventory_transaction_query, (order_id,))
            connection.commit()

            print("Order shipped successfully!")

        else:
            print("Not enough units in stock. Order cannot be shipped.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")

    finally:
        cursor.close()



def check_inventory(connection, order_id):
    try:
        cursor = connection.cursor()

        # Get the products and quantities from the order
        query_order_details = """
            SELECT od.ProductID, od.Quantity
            FROM order_details od
            WHERE od.OrderID = %s
        """
        cursor.execute(query_order_details, (order_id,))
        order_details = cursor.fetchall()

        for product_id, quantity in order_details:
            # Check if there are enough units in stock for each product in the order
            if not enough_units_in_stock(connection, product_id, quantity):
                return False

        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

    finally:
        cursor.close()

def enough_units_in_stock(connection, product_id, required_quantity):
    try:
        cursor = connection.cursor()

        # Get the total quantity purchased for the product
        query_total_purchased = """
            SELECT SUM(it.Quantity) AS total_purchased
            FROM inventory_transactions it
            WHERE it.ProductID = %s
              AND it.TransactionType = 'Purchased'
        """
        cursor.execute(query_total_purchased, (product_id,))
        total_purchased = cursor.fetchone()[0] or 0

        # Get the total quantity sold/on hold for the product
        query_total_sold_on_hold = """
            SELECT SUM(it.Quantity) AS total_sold_on_hold
            FROM inventory_transactions it
            WHERE it.ProductID = %s
              AND it.TransactionType IN ('Sold', 'On Hold')
        """
        cursor.execute(query_total_sold_on_hold, (product_id,))
        total_sold_on_hold = cursor.fetchone()[0] or 0

        # Calculate the available quantity in stock
        available_quantity = total_purchased - total_sold_on_hold

        # Check if there are enough units in stock
        return available_quantity >= required_quantity

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

    finally:
        cursor.close()

def update_inventory(connection, order_id):
    try:
        cursor = connection.cursor()

        # Get the products and quantities from the order
        query_order_details = """
            SELECT od.ProductID, od.Quantity
            FROM order_details od
            WHERE od.OrderID = %s
        """
        cursor.execute(query_order_details, (order_id,))
        order_details = cursor.fetchall()

        for product_id, quantity in order_details:
            # Insert rows into the inventory_transactions table for each product in the order
            # with TransactionType="Sold"
            query_insert_transaction = """
                INSERT INTO inventory_transactions 
                (TransactionType, TransactionCreatedDate, ProductID, Quantity, CustomerOrderID, Comments)
                VALUES ('Sold', NOW(), %s, %s, %s, 'Order Shipped')
            """
            values_insert_transaction = (product_id, quantity, order_id)
            cursor.execute(query_insert_transaction, values_insert_transaction)

        connection.commit()

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")

    finally:
        cursor.close()



def print_pending_orders(connection):
    try:
        cursor = connection.cursor()

        # Query pending orders with NULL ShippedDate, ordered by OrderDate
        query_pending_orders = """
            SELECT OrderID, OrderDate, ShipName, ShipAddress, ShipCity, ShipState, ShipZIP, ShipCountry
            FROM orders
            WHERE ShippedDate IS NULL
            ORDER BY OrderDate
        """
        cursor.execute(query_pending_orders)
        pending_orders = cursor.fetchall()

        if not pending_orders:
            print("No pending orders.")
        else:
            print("\nPending Orders:")
            print("{:<10} {:<20} {:<30} {:<50} {:<20} {:<20} {:<10} {:<20}".format(
                "OrderID", "OrderDate", "ShipName", "ShipAddress", "ShipCity", "ShipState", "ShipZIP", "ShipCountry"
            ))
            for order in pending_orders:
                formatted_order = ["None" if value is None else value for value in order]
                print("{:<10} {:<20} {:<30} {:<50} {:<20} {:<20} {:<10} {:<20}".format(*formatted_order))

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def more_options_menu(connection):
    while True:
        print("\nMore Options Menu:")
        print("1. Print Orders for a Customer")
        print("2. Print Number of Order Details for a Customer")
        print("3. Back to Main Menu")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            customer_id = input("Enter Customer ID: ")
            print_orders_for_customer(connection, customer_id)

        elif choice == '2':
            customer_id = input("Enter Customer ID: ")
            print_number_of_order_details(connection, customer_id)

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def print_orders_for_customer(connection, customer_id):
    try:
        cursor = connection.cursor()

        query = """
            SELECT OrderID, OrderDate, ShipName, ShipAddress
            FROM orders
            WHERE CustomerID = %s
        """
        cursor.execute(query, (customer_id,))
        orders = cursor.fetchall()

        if not orders:
            print(f"No orders found for Customer ID {customer_id}.")
        else:
            print("\nOrders for Customer ID", customer_id)
            for order in orders:
                print("{:<10} {:<20} {:<30} {:<50}".format(*order))

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()

def print_number_of_order_details(connection, customer_id):
    try:
        cursor = connection.cursor()

        query = """
            SELECT COUNT(*) AS num_order_details
            FROM order_details od
            JOIN orders o ON od.OrderID = o.OrderID
            WHERE o.CustomerID = %s
        """
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()

        num_order_details = result[0] if result else 0
        print(f"\nNumber of Order Details for Customer ID {customer_id}: {num_order_details}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()

def main():
    while True:
        print("\nMain Menu:")
        print("1. Add a customer")
        print("2. Add an order")
        print("3. Remove an order")
        print("4. Ship an order")
        print("5. Print pending orders")
        print("6. More options")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            add_customer(db_connection)

        elif choice == '2':
            # Take user input for adding an order
            customer_id = input("Enter Customer ID (choose from 1 to 29): ")

            # Initialize an empty dictionary for product quantities
            product_quantities = {}

            while True:
                product_id_input = input("Enter Product ID (enter 'done' to finish): ")
                if product_id_input.lower() == 'done':
                    break

                quantity_input = input("Enter Quantity: ")
                product_quantities[int(product_id_input)] = int(quantity_input)

            # Call the add_order function with the provided inputs
            add_order(db_connection, customer_id, product_quantities)

            

        elif choice == '3':
            # Take user input for removing an order
            order_id_to_remove = input("Enter Order ID to remove: ")
            remove_order(db_connection, order_id_to_remove)

        elif choice == '4':
            # Take user input for shipping an order
            order_id = input("Enter Order ID to ship: ")
            shipper_id = input("Enter Shipper ID: ")
            shipping_fee = input("Enter Shipping Fee: ")
            ship_order(db_connection, order_id, shipper_id, shipping_fee)


        elif choice == '5':
            print_pending_orders(db_connection)
        elif choice == '6':
            # Call the function to handle more options
            more_options_menu(db_connection)
        elif choice == '7':
            print("Concluding the program. Thank you for your interaction!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    db_connection = connect_to_database()

    if db_connection:
        main()
        db_connection.close()

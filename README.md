# Northwind Database Management System

## Description

This project demonstrates a database application built on the **Northwind** database, which stores sales information for a fictional company, **Northwind Traders**. Northwind Traders imports and exports exotic delicacies worldwide. The Northwind database is widely used for technical instruction and is available in **Microsoft Access**.

In this project, we use the MySQL version of the Northwind database. The application allows users to interact with the database via a command-line interface, enabling operations like adding customers, placing orders, shipping orders, and more.

## Installation

1. **Set up the MySQL Database**:
    - Download the Northwind database in SQL format and upload it to your local MySQL instance.
    - Ensure the MySQL server is running, and update the connection parameters in the code if needed.
   
2. **Install Python and Dependencies**:
    - Install Python 3.x if not already installed.
    - Install the necessary Python dependencies:
      ```bash
      pip install mysql-connector-python
      ```

## Usage

1. **Connect to the Database**:
    - Use the `connect_to_database()` function to establish a connection to the MySQL database. This function returns a connection object that is used in subsequent operations.
   
2. **Add a Customer**:
    - Call `add_customer(connection)` to interactively add a customer to the `Customers` table. You'll be prompted to enter customer details (name, address, etc.). The function inserts the new customer into the database.

3. **Add an Order**:
    - Call `add_order(connection, customer_id, product_quantities)` to place an order for a customer. Provide the customer ID and a dictionary containing product quantities. This function adds both the order and the order details to the database.

4. **Remove an Order**:
    - Use `remove_order(connection, order_id)` to delete an order from the `Orders` table, including its related entries in `Order_Details`.

5. **Ship an Order**:
    - Use `ship_order(connection, order_id, shipper_id, shipping_fee)` to process an order shipment. This function verifies inventory, updates the `Orders` table with shipment details, and adjusts inventory levels.

6. **Print Pending Orders**:
    - Call `print_pending_orders(connection)` to display orders that have not yet been shipped.

7. **More Options**:
    - Access additional features via the "More Options" menu:
      - Print all orders for a customer.
      - View the number of order details associated with a customer.

8. **Error Handling**:
    - The code includes robust error handling for database transactions, including rollbacks in case of errors during operations.

9. **Exiting the Program**:
    - To exit, choose option 7 from the main menu, which will automatically close the database connection.

## Extra Features

- **Print Orders for a Customer**: Fetch and display all orders placed by a specific customer.
- **Order Details Count**: Retrieve and display the number of order details associated with a specific customer.

## Running the Program

To run the program, execute:

```bash
python run.py
```

This will start the command-line interface where you can interact with the database, add customers, manage orders, and more.


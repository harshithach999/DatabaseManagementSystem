# DatabaseManagementSystem

# Database Application Development

## Description

The sales information for a fictional business named Northwind Traders, which imports and exports exotic delicacies from all over the world, is stored in the Northwind database. Microsoft had it ready for technological instruction.
In Microsoft Access, you can find the latest version of the database by entering, In the Search for Online Templates box, type "Northwind." The sales information for a fictional business named Northwind Traders is contained in the Northwind database. 
This brings in and sends out specialty meals from across the globe. Microsoft had it ready for technological instruction.

## Installation

1. Upload the required file into Mysql and install python.
2. Install dependencies with `pip install `.

## Usage

1. Connect to Database:
Use connect_to_database() to establish a connection to the MySQL database. This function returns a connection object.

2. Add a Customer:
Utilize add_customer(connection) to interactively add a customer to the "Customers" table. The user is prompted to enter customer details, and the information is inserted into the database.

2. Add an Order:
Call add_order(connection, customer_id, product_quantities) to add an order to the "Orders" table. The user provides the customer ID and a dictionary of product quantities. The function handles the insertion of order details into the database.

3. Remove an Order:
Use remove_order(connection, order_id) to remove an order. The user provides the order ID to be deleted, and the function deletes the corresponding entries from the "Orders" and "Order_Details" tables.

4. Ship an Order:
Call ship_order(connection, order_id, shipper_id, shipping_fee) to ship an order. The user provides the order ID, shipper ID, and shipping fee. The function checks if there are enough units in stock for each product in the order before updating the database.

5. Print Pending Orders:
Use print_pending_orders(connection) to display a list of pending orders. The function queries the "Orders" table for orders with a NULL "ShippedDate" and prints relevant information.

6. More Options:
Access additional functionalities through the "More Options" menu. Options include printing orders for a customer, printing the number of order details for a customer, or returning to the main menu.

7. Handling Connection:
The database connection is automatically closed when the program concludes.

8. Error Handling:
The code incorporates error handling for database-related operations, including rollbacks in case of errors during transactions.

9. Exiting the Program:
To exit the program, choose option 7 in the main menu.

## Extra Features

- Feature 1: printing orders for a customer.
- Feature 2: printing the number of order details for a customer or returning to the main menu.

## Code Compilation

To run the program, execute the following command:

python run.py



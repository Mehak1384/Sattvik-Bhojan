from login import login
from authorization import User

from menu import FoodMenu
from customers import Customer
from orders import Order
from sales import Sales

import psycopg2


def get_connection():

    connection = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="411008@Pd",
        database="sattvik_bhojan"
    )

    return connection


def admin_dashboard(user, connection):

    food_menu = FoodMenu(connection)
    customer = Customer(connection)
    order = Order(connection)
    sales = Sales(connection)

    while True:

        print("\n========== Admin Dashboard ==========")
        print("1. Manage Food Menu")
        print("2. Manage Customers")
        print("3. Manage Orders")
        print("4. View Sales Dashboard")
        print("5. Logout")

        choice = input("Enter your choice: ")

        # Food Menu
        if choice == "1":

            while True:

                print("\n------- Food Menu -------")
                print("1. Add Food")
                print("2. View Food")
                print("3. Update Food")
                print("4. Delete Food")
                print("5. Back")

                menu_choice = input("Enter your choice: ")

                if menu_choice == "1":
                    food_menu.add_food()

                elif menu_choice == "2":
                    food_menu.view_food()

                elif menu_choice == "3":
                    food_menu.update_food()

                elif menu_choice == "4":
                    food_menu.delete_food()

                elif menu_choice == "5":
                    break

                else:
                    print("Invalid choice.")

        # Customers
        elif choice == "2":

            while True:

                print("\n------- Customer Management -------")
                print("1. Add Customer")
                print("2. View Customers")
                print("3. Search Customer")
                print("4. Update Customer")
                print("5. Back")

                customer_choice = input("Enter your choice: ")

                if customer_choice == "1":
                    customer.add_customer()

                elif customer_choice == "2":
                    customer.view_customers()

                elif customer_choice == "3":
                    customer.search_customer()

                elif customer_choice == "4":
                    customer.update_customer()

                elif customer_choice == "5":
                    break

                else:
                    print("Invalid choice.")

        # Orders
        elif choice == "3":

            while True:

                print("\n------- Order Management -------")
                print("1. Create Order")
                print("2. View Orders")
                print("3. Update Order Status")
                print("4. Back")

                order_choice = input("Enter your choice: ")

                if order_choice == "1":
                    order.create_order()

                elif order_choice == "2":
                    order.view_orders()

                elif order_choice == "3":
                    order.update_status()

                elif order_choice == "4":
                    break

                else:
                    print("Invalid choice.")

        # Sales Dashboard
        elif choice == "4":

            sales.show_dashboard()

        # Logout
        elif choice == "5":

            print("Logging out...")
            break

        else:

            print("Invalid choice. Please try again.")


def staff_dashboard(user, connection):

    food_menu = FoodMenu(connection)
    customer = Customer(connection)
    order = Order(connection)

    while True:

        print("\n========== Staff Dashboard ==========")
        print("1. View Food Menu")
        print("2. Manage Customers")
        print("3. Manage Orders")
        print("4. Logout")

        choice = input("Enter your choice: ")

        # View Food Menu
        if choice == "1":

            food_menu.view_food()

        # Customers
        elif choice == "2":

            while True:

                print("\n------- Customer Management -------")
                print("1. Add Customer")
                print("2. View Customers")
                print("3. Search Customer")
                print("4. Update Customer")
                print("5. Back")

                customer_choice = input("Enter your choice: ")

                if customer_choice == "1":
                    customer.add_customer()

                elif customer_choice == "2":
                    customer.view_customers()

                elif customer_choice == "3":
                    customer.search_customer()

                elif customer_choice == "4":
                    customer.update_customer()

                elif customer_choice == "5":
                    break

                else:
                    print("Invalid choice.")

        # Orders
        elif choice == "3":

            while True:

                print("\n------- Order Management -------")
                print("1. Create Order")
                print("2. View Orders")
                print("3. Update Order Status")
                print("4. Back")

                order_choice = input("Enter your choice: ")

                if order_choice == "1":
                    order.create_order()

                elif order_choice == "2":
                    order.view_orders()

                elif order_choice == "3":
                    order.update_status()

                elif order_choice == "4":
                    break

                else:
                    print("Invalid choice.")

        # Logout
        elif choice == "4":

            print("Logging out...")
            break

        else:

            print("Invalid choice. Please try again.")


def main():

    role = login()

    if not role:
        print("Login failed.")
        return

    connection = None

    try:

        connection = get_connection()

        user = User(role)

        print("\nAuthorization successful.")

        if user.role == "Admin":

            admin_dashboard(user, connection)

        elif user.role == "Staff":

            staff_dashboard(user, connection)

        else:

            print("Invalid role.")

    except psycopg2.Error as e:

        print(f"Database connection error: {e}")

    finally:

        if connection:
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
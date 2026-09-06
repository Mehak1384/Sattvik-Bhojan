import psycopg2
from psycopg2 import Error, IntegrityError
class Customer:

    def __init__(self, connection):
        self.connection = connection

    def add_customer(self):
        try:
            name = input("Enter customer name: ")
            phone = input("Enter customer phone: ")

            if not name or not phone:
                print("Name and phone cannot be empty.")
                return

            query = """
            insert into customers (name, phone)
            values (%s, %s);
            """

            cursor = self.connection.cursor()
            cursor.execute(query, (name, phone))
            self.connection.commit()

            print("Customer added successfully!")

            cursor.close()

        except IntegrityError:
            self.connection.rollback()
            print("This phone number already exists.")

        except Error as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def view_customers(self):
        try:
            cursor = self.connection.cursor()

            query = """
            select id, name, phone
            from customers
            order by id;
            """

            cursor.execute(query)
            customers = cursor.fetchall()

            if not customers:
                print("No customers found.")
                cursor.close()
                return

            print("\n---------- Customers ----------")
            print("ID | Name | Phone")
            print("-------------------------------")

            for customer in customers:
                print(
                    f"{customer[0]} | "
                    f"{customer[1]} | "
                    f"{customer[2]}"
                )

            cursor.close()

        except Error as e:
            print(f"Error: {e}")

    def search_customer(self):
        try:
            phone = input("Enter customer phone: ")

            cursor = self.connection.cursor()

            query = """
            select id, name, phone
            from customers
            where phone = %s;
            """

            cursor.execute(query, (phone,))
            customer = cursor.fetchone()

            if customer:
                print("\nCustomer Found!")
                print(f"ID: {customer[0]}")
                print(f"Name: {customer[1]}")
                print(f"Phone: {customer[2]}")
            else:
                print("Customer not found.")

            cursor.close()

        except Error as e:
            print(f"Error: {e}")

    def update_customer(self):
        try:
            customer_id = int(
                input("Enter customer ID to update: ")
            )

            cursor = self.connection.cursor()

            check_query = """
            select id
            from customers
            where id = %s;
            """

            cursor.execute(check_query, (customer_id,))
            customer = cursor.fetchone()

            if customer is None:
                print("Customer not found.")
                cursor.close()
                return

            name = input("Enter new customer name: ")
            phone = input("Enter new phone number: ")

            query = """
            update customers
            set name = %s,
                phone = %s
            where id = %s;
            """

            cursor.execute(
                query,
                (name, phone, customer_id)
            )

            self.connection.commit()

            print("Customer updated successfully!")

            cursor.close()

        except ValueError:
            print("Please enter a valid customer ID.")

        except IntegrityError:
            self.connection.rollback()
            print("This phone number already exists.")

        except Error as e:
            self.connection.rollback()
            print(f"Error: {e}")
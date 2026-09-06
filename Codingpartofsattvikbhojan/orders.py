from psycopg2 import Error


class Order:

    def __init__(self, connection):
        self.connection = connection

    # Create a new order
    def create_order(self):

        cursor = None

        try:
            customer_id = int(input("Enter customer ID: "))

            cursor = self.connection.cursor()

            # Check customer exists
            customer_query = """
            select id, name
            from customers
            where id = %s;
            """

            cursor.execute(customer_query, (customer_id,))
            customer = cursor.fetchone()

            if customer is None:
                print("Customer not found.")
                return

            print(f"Customer: {customer[1]}")

            # Show available food
            food_query = """
            select id, name, price
            from food_items
            where available = true
            order by id;
            """

            cursor.execute(food_query)
            foods = cursor.fetchall()

            if not foods:
                print("No food items available.")
                return

            print("\n---------- Food Menu ----------")
            print("ID | Name | Price")
            print("-------------------------------")

            for food in foods:
                print(
                    f"{food[0]} | {food[1]} | ₹{food[2]}"
                )

            # Create order first
            order_query = """
            insert into orders (customer_id)
            values (%s)
            returning id;
            """

            cursor.execute(order_query, (customer_id,))

            order_id = cursor.fetchone()[0]

            total_amount = 0

            while True:

                food_id = int(
                    input("Enter food ID: ")
                )

                # Check food exists and is available
                food_check_query = """
                select id, name, price
                from food_items
                where id = %s
                and available = true;
                """

                cursor.execute(
                    food_check_query,
                    (food_id,)
                )

                food = cursor.fetchone()

                if food is None:
                    print("Food item not found or unavailable.")
                    continue

                quantity = int(
                    input("Enter quantity: ")
                )

                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                    continue

                food_price = food[2]

                item_total = food_price * quantity

                # Add item to order_items
                item_query = """
                insert into order_items
                (order_id, food_id, quantity, price)
                values (%s, %s, %s, %s);
                """

                cursor.execute(
                    item_query,
                    (
                        order_id,
                        food_id,
                        quantity,
                        food_price
                    )
                )

                total_amount += item_total

                print(
                    f"{food[1]} added. "
                    f"Item total: ₹{item_total}"
                )

                more = input(
                    "Add another food item? (yes/no): "
                )

                if more.lower() != "yes":
                    break

            # Update total amount
            update_query = """
            update orders
            set total_amount = %s
            where id = %s;
            """

            cursor.execute(
                update_query,
                (total_amount, order_id)
            )

            self.connection.commit()

            print("\nOrder created successfully!")
            print(f"Order ID: {order_id}")
            print(f"Total Amount: ₹{total_amount}")
            print("Status: Pending")

        except ValueError:
            self.connection.rollback()
            print("Please enter valid numeric values.")

        except Error as e:
            self.connection.rollback()
            print(f"Error creating order: {e}")

        finally:
            if cursor:
                cursor.close()

    # View all orders
    def view_orders(self):

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
            select
                o.id,
                c.name,
                o.order_date,
                o.total_amount,
                o.status
            from orders o
            join customers c
                on o.customer_id = c.id
            order by o.id;
            """

            cursor.execute(query)

            orders = cursor.fetchall()

            if not orders:
                print("No orders found.")
                return

            print("\n---------------- Orders ----------------")
            print(
                "ID | Customer | Date | Amount | Status"
            )
            print("-----------------------------------------")

            for order in orders:

                print(
                    f"{order[0]} | "
                    f"{order[1]} | "
                    f"{order[2]} | "
                    f"₹{order[3]} | "
                    f"{order[4]}"
                )

        except Error as e:
            print(f"Error viewing orders: {e}")

        finally:
            if cursor:
                cursor.close()

    # Update order status
    def update_status(self):

        cursor = None

        try:
            order_id = int(
                input("Enter order ID: ")
            )

            cursor = self.connection.cursor()

            # Check order exists
            check_query = """
            select id, status
            from orders
            where id = %s;
            """

            cursor.execute(
                check_query,
                (order_id,)
            )

            order = cursor.fetchone()

            if order is None:
                print("Order not found.")
                return

            print(f"Current status: {order[1]}")

            print("\nAvailable statuses:")
            print("1. Pending")
            print("2. Preparing")
            print("3. Ready")
            print("4. Delivered")
            print("5. Cancelled")

            choice = input(
                "Enter new status: "
            )

            statuses = {
                "1": "Pending",
                "2": "Preparing",
                "3": "Ready",
                "4": "Delivered",
                "5": "Cancelled"
            }

            if choice not in statuses:
                print("Invalid status.")
                return

            new_status = statuses[choice]

            query = """
            update orders
            set status = %s
            where id = %s;
            """

            cursor.execute(
                query,
                (new_status, order_id)
            )

            self.connection.commit()

            print(
                f"Order status updated to: {new_status}"
            )

        except ValueError:
            self.connection.rollback()
            print("Please enter a valid order ID.")

        except Error as e:
            self.connection.rollback()
            print(f"Error updating order: {e}")

        finally:
            if cursor:
                cursor.close()
import psycopg2
from psycopg2 import Error

class FoodMenu:

    def __init__(self, connection):
        self.connection = connection

    # Add a new food item
    def add_food(self):

        try:
            name = input("Enter food name: ")
            category = input("Enter food category: ")
            price = float(input("Enter food price: "))

            if price <= 0:
                print("Price must be greater than 0.")
                return

            query = """
            insert into food_items (name, category, price)
            values (%s, %s, %s);
            """

            cursor = self.connection.cursor()

            cursor.execute(
                query,
                (name, category, price)
            )

            self.connection.commit()

            print("Food item added successfully!")

            cursor.close()

        except ValueError:
            print("Please enter a valid price.")

        except Error as e:
            self.connection.rollback()
            print(f"Error adding food: {e}")

    # View all food items
    def view_food(self):

        try:
            cursor = self.connection.cursor()

            query = """
            select id, name, category, price, available
            from food_items
            order by id;
            """

            cursor.execute(query)

            foods = cursor.fetchall()

            if not foods:
                print("No food items found.")
                cursor.close()
                return

            print("\n---------- Food Menu ----------")
            print("ID | Name | Category | Price | Available")
            print("-----------------------------------------")

            for food in foods:
                print(
                    f"{food[0]} | {food[1]} | {food[2]} | "
                    f"₹{food[3]} | {food[4]}"
                )

            cursor.close()

        except Error as e:
            print(f"Error viewing food menu: {e}")

    # Update an existing food item
    def update_food(self):

        try:
            food_id = int(input("Enter food ID to update: "))

            cursor = self.connection.cursor()

            check_query = """
            select id
            from food_items
            where id = %s;
            """

            cursor.execute(check_query, (food_id,))

            food = cursor.fetchone()

            if food is None:
                print("Food item not found.")
                cursor.close()
                return

            name = input("Enter new food name: ")
            category = input("Enter new category: ")
            price = float(input("Enter new price: "))

            if price <= 0:
                print("Price must be greater than 0.")
                cursor.close()
                return

            query = """
            update food_items
            set name = %s,
                category = %s,
                price = %s
            where id = %s;
            """

            cursor.execute(
                query,
                (name, category, price, food_id)
            )

            self.connection.commit()

            print("Food item updated successfully!")

            cursor.close()

        except ValueError:
            print("Please enter valid values.")

        except Error as e:
            self.connection.rollback()
            print(f"Error updating food: {e}")

    # Delete a food item
    def delete_food(self):

        try:
            food_id = int(input("Enter food ID to delete: "))

            cursor = self.connection.cursor()

            check_query = """
            select id
            from food_items
            where id = %s;
            """

            cursor.execute(check_query, (food_id,))

            food = cursor.fetchone()

            if food is None:
                print("Food item not found.")
                cursor.close()
                return

            confirmation = input(
                "Are you sure you want to delete this food? (yes/no): "
            )

            if confirmation.lower() != "yes":
                print("Delete operation cancelled.")
                cursor.close()
                return

            query = """
            delete from food_items
            where id = %s;
            """

            cursor.execute(query, (food_id,))

            self.connection.commit()

            print("Food item deleted successfully!")

            cursor.close()

        except ValueError:
            print("Please enter a valid food ID.")

        except Error as e:
            self.connection.rollback()
            print(f"Error deleting food: {e}")
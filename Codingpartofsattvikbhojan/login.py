import psycopg2
import bcrypt
from psycopg2 import OperationalError


def login():

    connection = None

    try:
        connection = psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            user="postgres",
            password="411008@Pd",
            database="sattvik_bhojan"
        )

        print("Database connection successful!")

        username = input("Enter username: ")
        password = input("Enter password: ")

        cursor = connection.cursor()

        query = """
        select username, password, role
        from users
        where username = %s;
        """

        cursor.execute(query, (username,))

        user = cursor.fetchone()

        if user is None:
            print("Username not found.")
            return

        stored_username = user[0]
        stored_password = user[1]
        role = user[2]

        password_is_correct = bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        )

        if password_is_correct:
                print("Login successful!")
                print(f"Welcome, {stored_username}!")
                print(f"Role: {role}")

                return role

        else:
         print("Incorrect password.")

        cursor.close()

    except OperationalError as e:
        print(f"Database connection error: {e}")

    finally:
        if connection:
            connection.close()
            print("Database connection closed.")


login()


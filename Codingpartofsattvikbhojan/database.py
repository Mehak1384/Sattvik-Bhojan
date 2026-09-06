import psycopg2
from psycopg2 import OperationalError, IntegrityError
import bcrypt

def create_connection_psql():
    connection=None
    try:
        connection=psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            user="postgres",
            password="411008@Pd",
            database="sattvik_bhojan"
        )
        print("Database connection successful!")

        cursor = connection.cursor()

        query = """
        create table if not exists users (
            id serial primary key,
            username varchar(50) unique not null,
            password varchar(255) unique not null,
            role varchar(20) not null
        );
        """

        cursor.execute(query)
        connection.commit()

        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (Admin/Staff): ")

        if role not in ["Admin", "Staff"]:
            print("Invalid role. Please enter Admin or Staff.")
            return

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        query_table = """
        insert into users (username, password, role)
        VALUES (%s, %s, %s);
        """

        values = (
            username,
            hashed_password.decode("utf-8"),
            role
        )

        try:
            cursor.execute(query_table, values)
            connection.commit()
            print("User registered successfully!")

        except IntegrityError:
            connection.rollback()
            print("Username already exists.")

        cursor.close()

    except OperationalError as e:
        print(f"The error occurred is: {e}")
        
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

conn = create_connection_psql()
    
    
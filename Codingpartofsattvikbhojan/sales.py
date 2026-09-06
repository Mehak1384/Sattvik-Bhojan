import tkinter as tk
from tkinter import ttk
from psycopg2 import Error

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Sales:

    def __init__(self, connection):
        self.connection = connection

    def get_total_sales(self):

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
            select coalesce(sum(total_amount), 0)
            from orders
            where status != 'Cancelled';
            """

            cursor.execute(query)

            return cursor.fetchone()[0]

        except Error as e:
            print(f"Error getting total sales: {e}")
            return 0

        finally:
            if cursor:
                cursor.close()

    def get_total_orders(self):

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
            select count(*)
            from orders
            where status != 'Cancelled';
            """

            cursor.execute(query)

            return cursor.fetchone()[0]

        except Error as e:
            print(f"Error getting total orders: {e}")
            return 0

        finally:
            if cursor:
                cursor.close()

    def get_average_order(self):

        total_sales = self.get_total_sales()
        total_orders = self.get_total_orders()

        if total_orders == 0:
            return 0

        return total_sales / total_orders

    def get_sales_by_date(self):

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
            select
                date(order_date),
                sum(total_amount)
            from orders
            where status != 'Cancelled'
            group by date(order_date)
            order by date(order_date);
            """

            cursor.execute(query)

            return cursor.fetchall()

        except Error as e:
            print(f"Error getting sales data: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

    def get_top_foods(self):

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
            select
                f.name,
                sum(oi.quantity) as total_quantity
            from order_items oi
            join food_items f
                on oi.food_id = f.id
            join orders o
                on oi.order_id = o.id
            where o.status != 'Cancelled'
            group by f.name
            order by total_quantity desc
            limit 5;
            """

            cursor.execute(query)

            return cursor.fetchall()

        except Error as e:
            print(f"Error getting food data: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

    def show_dashboard(self):

        window = tk.Tk()

        window.title("Sattvik Bhojan - Sales Dashboard")
        window.geometry("1000x700")

        title = tk.Label(
            window,
            text="Sattvik Bhojan Sales Dashboard",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=15)

        # -------------------------
        # Dashboard cards
        # -------------------------

        card_frame = tk.Frame(window)

        card_frame.pack(pady=10)

        total_sales = self.get_total_sales()
        total_orders = self.get_total_orders()
        average_order = self.get_average_order()

        sales_label = tk.Label(
            card_frame,
            text=f"Total Sales\n₹{total_sales:.2f}",
            font=("Arial", 16, "bold"),
            width=20,
            height=4,
            relief="ridge"
        )

        sales_label.grid(row=0, column=0, padx=10)

        orders_label = tk.Label(
            card_frame,
            text=f"Total Orders\n{total_orders}",
            font=("Arial", 16, "bold"),
            width=20,
            height=4,
            relief="ridge"
        )

        orders_label.grid(row=0, column=1, padx=10)

        average_label = tk.Label(
            card_frame,
            text=f"Average Order\n₹{average_order:.2f}",
            font=("Arial", 16, "bold"),
            width=20,
            height=4,
            relief="ridge"
        )

        average_label.grid(row=0, column=2, padx=10)

        # -------------------------
        # Sales chart
        # -------------------------

        sales_data = self.get_sales_by_date()

        figure = Figure(figsize=(9, 4))

        chart = figure.add_subplot(111)

        if sales_data:

            dates = [str(row[0]) for row in sales_data]
            amounts = [float(row[1]) for row in sales_data]

            chart.plot(
                dates,
                amounts,
                marker="o"
            )

            chart.set_title("Sales by Date")
            chart.set_xlabel("Date")
            chart.set_ylabel("Sales (₹)")

            chart.tick_params(axis="x", rotation=45)

        else:

            chart.text(
                0.5,
                0.5,
                "No sales data available",
                ha="center",
                va="center"
            )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=window
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=20
        )

        # -------------------------
        # Top food items
        # -------------------------

        top_foods = self.get_top_foods()

        food_frame = tk.Frame(window)

        food_frame.pack(pady=10)

        food_title = tk.Label(
            food_frame,
            text="Top Selling Food Items",
            font=("Arial", 16, "bold")
        )

        food_title.pack()

        for food in top_foods:

            food_label = tk.Label(
                food_frame,
                text=f"{food[0]} - {food[1]} sold",
                font=("Arial", 12)
            )

            food_label.pack()

        window.mainloop()
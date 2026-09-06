from login import login
class User:

    def __init__(self, role):
        self.role = role

    def display_dashboard(self):

        if self.role == "Admin":
            print("\n--- Admin Dashboard ---")
            print("1. Manage Users")
            print("2. Manage Food Menu")
            print("3. Manage Customers")
            print("4. Manage Orders")
            print("5. View Sales Summary")
            print("6. Logout")

        elif self.role == "Staff":
            print("\n--- Staff Dashboard ---")
            print("1. View Food Menu")
            print("2. Manage Customers")
            print("3. Manage Orders")
            print("4. Logout")

        else:
            print("Invalid role.")


role = login()

if role:
    user = User(role)
    user.display_dashboard()
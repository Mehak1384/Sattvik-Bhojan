class User:

    def __init__(self, role):
        self.role = role

    def display_dashboard(self):

        while True:

            if self.role == "Admin":
                print("\n--- Admin Dashboard ---")
                print("1. Manage Users")
                print("2. Manage Food Menu")
                print("3. Manage Customers")
                print("4. Manage Orders")
                print("5. View Sales Summary")
                print("6. Logout")

                choice = input("Enter your choice: ")

                if choice == "1":
                    print("User Management selected.")

                elif choice == "2":
                    print("Food Menu Management selected.")

                elif choice == "3":
                    print("Customer Management selected.")

                elif choice == "4":
                    print("Order Management selected.")

                elif choice == "5":
                    print("Sales Summary selected.")

                elif choice == "6":
                    print("Logging out...")
                    break

                else:
                    print("Invalid choice. Please try again.")

            elif self.role == "Staff":
                print("\n--- Staff Dashboard ---")
                print("1. View Food Menu")
                print("2. Manage Customers")
                print("3. Manage Orders")
                print("4. Logout")

                choice = input("Enter your choice: ")

                if choice == "1":
                    print("Food Menu selected.")

                elif choice == "2":
                    print("Customer Management selected.")

                elif choice == "3":
                    print("Order Management selected.")

                elif choice == "4":
                    print("Logging out...")
                    break

                else:
                    print("Invalid choice. Please try again.")

            else:
                print("Invalid role.")
                break
from login import login
from authorization import User
role = login()
if role:
    user = User(role)
    user.display_dashboard()
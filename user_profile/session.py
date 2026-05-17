# session.py
# Holds the currently logged-in user across all screens.
# Import this anywhere: import session

current_user = None  # dict set on login, cleared on logout


def set_user(user_row):
    """Call this after a successful login. user_row is a tuple from DB."""
    global current_user
    current_user = {
        "user_id":     user_row[0],
        "name":        user_row[1]  or "",
        "email":       user_row[2]  or "",
        "role":        user_row[4]  or "Admin",
        "contact":     user_row[5]  or "",
        "date_joined": user_row[7].strftime("%B %d, %Y") if user_row[7] else "",
    }


def clear():
    global current_user
    current_user = None


def get():
    return current_user
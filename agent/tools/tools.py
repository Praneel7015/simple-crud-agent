# agent/tools/tools.py

import sqlite3
from typing import List, Dict, Any, Optional

DB_FILE = "users.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Creates the 'users' table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def create_user(name: str, email: str) -> Dict[str, Any]:
    """
    Creates a new user in the database. Use this when asked to add or create a new user.

    Args:
        name: The full name of the user.
        email: The unique email address for the user.

    Returns:
        A dictionary containing the details of the newly created user or an error.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {"status": "Success", "user": {"id": user_id, "name": name, "email": email}}
    except sqlite3.IntegrityError:
        return {"status": "Error", "message": f"A user with the email '{email}' already exists."}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

def read_user(user_id: int) -> Dict[str, Any]:
    """
    Retrieves a single user's details using their unique ID. Use this when asked to find or get a specific user.

    Args:
        user_id: The unique ID of the user to find.

    Returns:
        A dictionary containing the user's data or an error message if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"status": "Success", "user": dict(user)}
    return {"status": "Not Found", "message": f"User with ID {user_id} was not found."}

def update_user(user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
    """
    Updates the name and/or email for an existing user based on their ID. Use this when asked to change or update a user's details.
    You can update just the name, just the email, or both.

    Args:
        user_id: The unique ID of the user to update.
        name: The new name for the user (optional - only updated if provided).
        email: The new email address for the user (optional - only updated if provided).

    Returns:
        A dictionary containing the updated user's data or an error message.
    """
    if name is None and email is None:
        return {"status": "Error", "message": "At least one field (name or email) must be provided for update."}
    
    # First, get the current user data
    current_user = read_user(user_id)
    if current_user.get("status") != "Success":
        return current_user  # Return the error from read_user
    
    # Use current values if new ones aren't provided
    current_data = current_user["user"]
    new_name = name if name is not None else current_data["name"]
    new_email = email if email is not None else current_data["email"]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (new_name, new_email, user_id))
        conn.commit()
        conn.close()
        if cursor.rowcount > 0:
            return {"status": "Success", "updated_user": {"id": user_id, "name": new_name, "email": new_email}}
        return {"status": "Not Found", "message": f"User with ID {user_id} not found, so nothing was updated."}
    except sqlite3.IntegrityError:
        return {"status": "Error", "message": f"A user with the email '{new_email}' already exists."}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

def delete_user(user_id: int) -> Dict[str, str]:
    """
    Deletes a user from the database using their unique ID. Use this when asked to delete or remove a user.

    Args:
        user_id: The unique ID of the user to delete.

    Returns:
        A success or error message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return {"status": "Success", "message": f"User with ID {user_id} was deleted successfully."}
    return {"status": "Not Found", "message": f"User with ID {user_id} not found, so nothing was deleted."}

def list_users() -> List[Dict[str, Any]]:
    """
    Retrieves a list of all users in the database. Use this when asked to list, show, or get all users.

    Returns:
        A list of dictionaries, where each dictionary represents a user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

def delete_all_users() -> Dict[str, Any]:
    """
    Deletes all users from the database. Use this when asked to clear or delete all users.
    WARNING: This operation cannot be undone.

    Returns:
        A dictionary containing the number of users deleted and a success message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()["count"]
    
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    
    return {
        "status": "Success", 
        "message": f"All {user_count} users have been deleted from the database.",
        "deleted_count": user_count
    }

def populate_database() -> Dict[str, Any]:
    """
    Populates the database with sample users if it's empty. Use this to add initial test data.

    Returns:
        A dictionary containing information about the population process.
    """
    existing_users = list_users()
    if existing_users:
        return {
            "status": "Skipped", 
            "message": f"Database already contains {len(existing_users)} users. No sample data added.",
            "existing_count": len(existing_users)
        }
    
    sample_users = [
        ("Alice Smith", "alice@example.com"),
        ("Bob Johnson", "bob@example.com"),
        ("Charlie Lee", "charlie@example.com"),
        ("Dana White", "dana@example.com"),
        ("Eve Black", "eve@example.com")
    ]
    
    created_users = []
    for name, email in sample_users:
        result = create_user(name, email)
        if result.get("status") == "Success":
            created_users.append(result["user"])
    
    return {
        "status": "Success",
        "message": f"Database populated with {len(created_users)} sample users.",
        "created_users": created_users,
        "created_count": len(created_users)
    }

# Initialize the database and table when this module is imported
create_table()

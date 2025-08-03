# tools/tools.py

import sqlite3
from typing import List, Dict, Any

DB_FILE = "users.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

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

def update_user(user_id: int, name: str, email: str) -> Dict[str, Any]:
    """
    Updates the name and email for an existing user based on their ID. Use this when asked to change or update a user's details.

    Args:
        user_id: The unique ID of the user to update.
        name: The new name for the user.
        email: The new email address for the user.

    Returns:
        A dictionary containing the updated user's data or an error message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return {"status": "Success", "updated_user": {"id": user_id, "name": name, "email": email}}
    return {"status": "Not Found", "message": f"User with ID {user_id} not found, so nothing was updated."}

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

# src/database.py

import sqlite3
from typing import List, Dict, Any

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
    Creates a new user in the database.

    Args:
        name: The name of the user.
        email: The email of the user.

    Returns:
        A dictionary containing the ID of the newly created user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "name": name, "email": email}
    except sqlite3.IntegrityError:
        return {"error": f"User with email {email} already exists."}
    finally:
        conn.close()

def read_user(user_id: int) -> Dict[str, Any]:
    """
    Reads a user from the database by their ID.

    Args:
        user_id: The ID of the user to retrieve.

    Returns:
        A dictionary containing the user's data or an error message if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    return {"error": f"User with ID {user_id} not found."}

def update_user(user_id: int, name: str, email: str) -> Dict[str, Any]:
    """
    Updates a user's information in the database.

    Args:
        user_id: The ID of the user to update.
        name: The new name for the user.
        email: The new email for the user.

    Returns:
        A dictionary containing the updated user's data or an error message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return {"id": user_id, "name": name, "email": email}
    return {"error": f"User with ID {user_id} not found."}

def delete_user(user_id: int) -> Dict[str, str]:
    """
    Deletes a user from the database.

    Args:
        user_id: The ID of the user to delete.

    Returns:
        A success or error message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return {"message": f"User with ID {user_id} deleted successfully."}
    return {"error": f"User with ID {user_id} not found."}

def list_users() -> List[Dict[str, Any]]:
    """
    Lists all users in the database.

    Returns:
        A list of dictionaries, where each dictionary represents a user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

# Initialize the database and table when this module is imported
create_table()

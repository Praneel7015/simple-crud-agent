import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

# Import the CRUD tools
from agent.tools.tools import (
    create_user,
    read_user,
    update_user,
    delete_user,
    list_users,
    delete_all_users,
    populate_database
)

# Load environment variables from .env file
load_dotenv()

# Check for Google API Key
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Define the agent
db_agent = Agent(
    name="db_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a database management assistant.
    You can perform CRUD operations (Create, Read, Update, Delete) on a user database.
    When a user asks to perform an action, call the appropriate tool.
    When you get the result from the tool, present it to the user in a clear and friendly manner.
    
    Available operations:
    - Create User: Add a new user with name and email
    - Read User: Retrieve a specific user by their ID
    - Update User: Modify an existing user's name and email
    - Delete User: Remove a user from the database
    - List Users: Show all users in the database
    - Delete All Users: Remove all users from the database (WARNING: Cannot be undone)
    - Populate Database: Add sample users to an empty database
    """,
    tools=[
        FunctionTool(fn) for fn in [
            create_user,
            read_user,
            update_user,
            delete_user,
            list_users,
            delete_all_users,
            populate_database
        ]
    ]
)

# Required for ADK: expose the root agent
root_agent = db_agent

# --- Populate the database with sample users if empty ---
def _populate_db():
    """Initialize the database with sample users if it's empty."""
    result = populate_database()
    print(f"Database initialization: {result['message']}")

_populate_db()

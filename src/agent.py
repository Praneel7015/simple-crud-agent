import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

# Import the database functions
from src import database

# Load environment variables from .env file
load_dotenv()

# Check for Google API Key
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Define the agent
db_agent = Agent(
    name="db_agent", # Added the required name parameter
    model="gemini-2.0-flash",
    instruction="""
    You are a database management assistant.
    You can perform CRUD operations (Create, Read, Update, Delete) on a user database.
    When a user asks to perform an action, call the appropriate tool.
    When you get the result from the tool, present it to the user in a clear and friendly manner.
    """,
    tools=[
        FunctionTool(fn) for fn in [
            database.create_user,
            database.read_user,
            database.update_user,
            database.delete_user,
            database.list_users
        ]
    ]
)

# Required for ADK: expose the root agent
root_agent = db_agent

# --- Populate the database with sample users if empty ---
def _populate_db():
    if not database.list_users():
        database.create_user("Alice Smith", "alice@example.com")
        database.create_user("Bob Johnson", "bob@example.com")
        database.create_user("Charlie Lee", "charlie@example.com")
        database.create_user("Dana White", "dana@example.com")
        database.create_user("Eve Black", "eve@example.com")

_populate_db()

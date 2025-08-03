# Google ADK Database Agent

A simple Google ADK agent using the Gemini 2.0 Flash model to perform CRUD operations on a SQLite user database. Interact with the agent via the ADK Dev UI (`adk web`).

## Project Structure

```
your_project/
│
├── src/
│   ├── __init__.py
│   ├── agent.py         # The ADK agent definition
│   └── database.py      # SQLite CRUD logic
│
├── requirements.txt
├── .env                 # For GOOGLE_API_KEY
├── README.md
└── users.db             # SQLite database (auto-created)
```

## Setup

1. **Create a virtual environment:**
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Set up your `.env` file:**
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
4. **Run the ADK Dev UI:**
   ```
   adk web
   ```
   This will open the agent chat interface in your browser.

## Usage
- Interact with the agent in the web UI to create, read, update, delete, and list users.
- The agent uses a local SQLite database (`users.db`) for persistent storage.


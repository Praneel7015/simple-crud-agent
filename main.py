#!/usr/bin/env python3
"""
Main entry point for the CRUD Agent following Google Agent Development Kit format.
"""

from agent import root_agent

if __name__ == "__main__":
    # The agent is now ready to be used
    print("CRUD Agent initialized and ready!")
    print("Available operations: Create, Read, Update, Delete, List, Delete All, and Populate Database")
    print("Agent structure follows Google ADK format:")
    print("  /agent/agent.py - Contains agent definition")
    print("  /agent/tools/tools.py - Contains all CRUD operations")

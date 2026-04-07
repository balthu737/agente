# notion_api.py

"""Tool to interact with the Notion API.

This module defines a small wrapper around the Notion HTTP API.  It provides
three main functions:

1. ``get_page`` – Retrieve a single page by its ID.
2. ``query_database`` – Execute a database query.
3. ``create_page`` – Create a new page in a database.

All functions return a tuple ``(status, messages)`` similar to the other
tools in the workspace.

The module expects a global environment variable ``NOTION_TOKEN`` with a
valid integration token.  It also uses the ``NOTION_VERSION`` header
(2022-06-28 by default) to keep compatibility with the API.
"""

import os
import json
import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

# Tool definition for the API

tool_definition = {
    "type": "function",
    "function": {
        "name": "notion_query",
        "description": "Execute a query against a Notion database or retrieve a page.",
        "parameters": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["page", "database"],
                    "description": "What you want to query: a page or a database.",
                },
                "id": {
                    "type": "string",
                    "description": "The Notion page or database ID.",
                },
                "payload": {
                    "type": "object",
                    "description": "Optional JSON payload for database query or page creation.",
                },
            },
            "required": ["type", "id"],
        },
    },
}

# Implementation

def notion_query(type: str, id: str, payload: dict | None = None) -> str:
    """Dispatches the request to the Notion API.

    Parameters
    ----------
    type: str
        ``"page"`` to retrieve a page, ``"database"`` to query a database.
    id: str
        The unique ID of the page or database.
    payload: dict | None
        Payload for database query or page creation.  Ignored for page retrieval.
    """
    print("⚙️ Llamada a notion_query")
    if type == "page":
        url = f"https://api.notion.com/v1/pages/{id}"
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            return json.dumps({"status": 200, "messages": response.json()})
        except requests.HTTPError as e:
            return json.dumps({"status": 400, "messages": str(e)})
    elif type == "database":
        url = f"https://api.notion.com/v1/databases/{id}/query"
        try:
            response = requests.post(url, headers=HEADERS, json=payload or {})
            response.raise_for_status()
            return json.dumps({"status": 200, "messages": response.json()})
        except requests.HTTPError as e:
            return json.dumps({"status": 400, "messages": str(e)})
    else:
        return json.dumps({"status": 400, "messages": "Unsupported type."})

# Optional helpers for page creation

def create_page(database_id: str, properties: dict, content: list | None = None) -> str:
    """Create a new page in a database.

    Parameters
    ----------
    database_id: str
        The ID of the database where the page should be created.
    properties: dict
        Properties to set on the new page.
    content: list | None
        Optional array of blocks (children) for the page.
    """
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }
    if content:
        payload["children"] = content
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return json.dumps({"status": 200, "messages": response.json()})
    except requests.HTTPError as e:
        return json.dumps({"status": 400, "messages": str(e)})

# End of module


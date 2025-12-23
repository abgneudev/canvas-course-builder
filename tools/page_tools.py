"""Page management function tools for Groq."""
from typing import List, Dict, Any


def get_page_tools() -> List[Dict[str, Any]]:
    """Get function declarations for page operations.
    
    Returns:
        List of function declarations in OpenAI-compatible format
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "list_pages",
                "description": "List all pages in a course. Use this when user asks about pages.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "search_term": {"type": "string", "description": "Search pages by title"},
                        "published": {"type": "boolean", "description": "Filter by published status"}
                    },
                    "required": ["course_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_page",
                "description": "Get details about a specific page including its content. Use this when user asks about a specific page.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "page_url": {"type": "string", "description": "The page URL (slug)"}
                    },
                    "required": ["course_id", "page_url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_page",
                "description": "Create a new page in a course. Use this when user wants to add or create a page.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "title": {"type": "string", "description": "The page title"},
                        "body": {"type": "string", "description": "The page content (HTML allowed)"},
                        "published": {"type": "boolean", "description": "Whether the page should be published immediately"},
                        "front_page": {"type": "boolean", "description": "Set as course front page"},
                        "editing_roles": {"type": "string", "description": "Who can edit: teachers, students, members, or public"}
                    },
                    "required": ["course_id", "title", "body"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_page",
                "description": "Update page content or settings. Use this when user wants to modify or change a page.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "page_url": {"type": "string", "description": "The page URL (slug)"},
                        "title": {"type": "string", "description": "New page title"},
                        "body": {"type": "string", "description": "New page content (HTML allowed)"},
                        "published": {"type": "boolean", "description": "Whether the page should be published"}
                    },
                    "required": ["course_id", "page_url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_page",
                "description": "Delete a page. DESTRUCTIVE ACTION - requires confirmation. Use this when user explicitly wants to delete a page.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "page_url": {"type": "string", "description": "The page URL (slug) to delete"}
                    },
                    "required": ["course_id", "page_url"]
                }
            }
        }
    ]

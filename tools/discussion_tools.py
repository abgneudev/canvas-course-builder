"""Discussion management function tools for Groq."""
from typing import List, Dict, Any


def get_discussion_tools() -> List[Dict[str, Any]]:
    """Get function declarations for discussion operations.
    
    Returns:
        List of function declarations in OpenAI-compatible format
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "list_discussions",
                "description": "List all discussion topics in a course. Use this when user asks about discussions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "search_term": {"type": "string", "description": "Search discussions by title"}
                    },
                    "required": ["course_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_discussion",
                "description": "Get details about a specific discussion. Use this when user asks about a specific discussion.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "topic_id": {"type": "integer", "description": "The discussion topic ID"}
                    },
                    "required": ["course_id", "topic_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_discussion",
                "description": "Create a new discussion topic. Use this when user wants to start a discussion.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "title": {"type": "string", "description": "The discussion title"},
                        "message": {"type": "string", "description": "The discussion message (HTML allowed)"},
                        "discussion_type": {"type": "string", "description": "Type: side_comment or threaded"},
                        "published": {"type": "boolean", "description": "Publish immediately"},
                        "is_announcement": {"type": "boolean", "description": "Create as announcement"},
                        "pinned": {"type": "boolean", "description": "Pin at the top"},
                        "require_initial_post": {"type": "boolean", "description": "Require post before viewing replies"}
                    },
                    "required": ["course_id", "title", "message"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_announcement",
                "description": "Create an announcement. Use this when user wants to post an announcement.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "title": {"type": "string", "description": "The announcement title"},
                        "message": {"type": "string", "description": "The announcement message (HTML allowed)"},
                        "published": {"type": "boolean", "description": "Publish immediately"}
                    },
                    "required": ["course_id", "title", "message"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_discussion",
                "description": "Update an existing discussion. Use this when user wants to modify a discussion.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "topic_id": {"type": "integer", "description": "The discussion topic ID"},
                        "title": {"type": "string", "description": "New discussion title"},
                        "message": {"type": "string", "description": "New message (HTML allowed)"},
                        "published": {"type": "boolean", "description": "Published status"}
                    },
                    "required": ["course_id", "topic_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_discussion",
                "description": "Delete a discussion. DESTRUCTIVE ACTION - requires confirmation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "topic_id": {"type": "integer", "description": "The discussion topic ID to delete"}
                    },
                    "required": ["course_id", "topic_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "post_discussion_entry",
                "description": "Post a reply to a discussion. Use this when user wants to post or reply to a discussion.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "topic_id": {"type": "integer", "description": "The discussion topic ID"},
                        "message": {"type": "string", "description": "The reply message (HTML allowed)"}
                    },
                    "required": ["course_id", "topic_id", "message"]
                }
            }
        }
    ]

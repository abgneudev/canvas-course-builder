"""Module management function tools for Groq."""
from typing import List, Dict, Any


def get_module_tools() -> List[Dict[str, Any]]:
    """Get function declarations for module operations.
    
    Returns:
        List of function declarations in OpenAI-compatible format
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "list_modules",
                "description": "List all modules in a course. Use this when user asks about modules in a course.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "include_items": {"type": "boolean", "description": "Include module items in the response"}
                    },
                    "required": ["course_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_module",
                "description": "Get details about a specific module. Use this when user asks about a specific module.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "module_id": {"type": "integer", "description": "The module ID"}
                    },
                    "required": ["course_id", "module_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_module",
                "description": "Create a new module in a course. Use this when user wants to add or create a module.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "name": {"type": "string", "description": "The module name"},
                        "position": {"type": "integer", "description": "The position of the module in the course (1-based)"},
                        "require_sequential_progress": {"type": "boolean", "description": "Whether students must complete items in order"},
                        "unlock_at": {"type": "string", "description": "Date when module unlocks (ISO 8601 format)"}
                    },
                    "required": ["course_id", "name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_module",
                "description": "Update module information. Use this when user wants to modify or change a module.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "module_id": {"type": "integer", "description": "The module ID"},
                        "name": {"type": "string", "description": "New module name"},
                        "published": {"type": "boolean", "description": "Whether the module should be published"}
                    },
                    "required": ["course_id", "module_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_module",
                "description": "Delete a module. DESTRUCTIVE ACTION - requires confirmation. Use this when user explicitly wants to delete a module.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "module_id": {"type": "integer", "description": "The module ID to delete"}
                    },
                    "required": ["course_id", "module_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_module_item",
                "description": "Add an item to a module (page, assignment, quiz, discussion, file, etc.). Use this when user wants to add content to a module.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "module_id": {"type": "integer", "description": "The module ID"},
                        "title": {"type": "string", "description": "The item title"},
                        "type": {"type": "string", "description": "The type of item: Page, Assignment, Quiz, Discussion, File, SubHeader, ExternalUrl, or ExternalTool"},
                        "content_id": {"type": "integer", "description": "The ID of the content object (assignment ID, page ID, etc.)"},
                        "page_url": {"type": "string", "description": "The URL of the page (for Page type items)"},
                        "external_url": {"type": "string", "description": "The external URL (for ExternalUrl type items)"},
                        "position": {"type": "integer", "description": "The position in the module"},
                        "indent": {"type": "integer", "description": "Indentation level (0-3)"}
                    },
                    "required": ["course_id", "module_id", "title", "type"]
                }
            }
        }
        ,
        {
            "type": "function",
            "function": {
                "name": "create_module_with_items",
                "description": "Create a module and populate it with a list of items in order (subheaders, pages, assignments, quizzes, discussions, external links). Use this when the user provides a whole module outline in one request.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "name": {"type": "string", "description": "The module name"},
                        "position": {"type": "integer", "description": "Position of the module in the course (1-based)"},
                        "unlock_at": {"type": "string", "description": "Date when module unlocks (ISO 8601 format)"},
                        "require_sequential_progress": {"type": "boolean", "description": "Whether students must complete items in order"},
                        "items": {
                            "type": "array",
                            "description": "Ordered list of items to add to the module",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string", "description": "Item type: SubHeader, Page, Assignment, Quiz, Discussion, ExternalUrl"},
                                    "title": {"type": "string", "description": "Item title as shown in the module"},
                                    "body": {"type": "string", "description": "Page or discussion body (HTML allowed)"},
                                    "message": {"type": "string", "description": "Discussion message/body (HTML allowed)"},
                                    "description": {"type": "string", "description": "Assignment or quiz description (HTML allowed)"},
                                    "due_at": {"type": "string", "description": "Due date in ISO 8601 format"},
                                    "points_possible": {"type": "number", "description": "Points for assignment"},
                                    "submission_types": {"type": "array", "items": {"type": "string"}, "description": "Allowed submission types for assignment"},
                                    "discussion_type": {"type": "string", "description": "Discussion type: side_comment or threaded"},
                                    "external_url": {"type": "string", "description": "External URL for ExternalUrl items"},
                                    "published": {"type": "boolean", "description": "Publish the created resource"},
                                    "position": {"type": "integer", "description": "Explicit position override inside the module"}
                                },
                                "required": ["type", "title"]
                            }
                        }
                    },
                    "required": ["course_id", "name", "items"]
                }
            }
        }
    ]

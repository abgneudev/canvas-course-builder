"""Assignment management function tools for Groq."""
from typing import List, Dict, Any


def get_assignment_tools() -> List[Dict[str, Any]]:
    """Get function declarations for assignment operations.
    
    Returns:
        List of function declarations in OpenAI-compatible format
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "list_assignments",
                "description": "List all assignments in a course. Use this when user asks about assignments.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "search_term": {"type": "string", "description": "Search assignments by name"},
                        "bucket": {"type": "string", "description": "Filter: past, overdue, undated, ungraded, upcoming, future"}
                    },
                    "required": ["course_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_assignment",
                "description": "Get details about a specific assignment. Use this when user asks about a specific assignment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "assignment_id": {"type": "integer", "description": "The assignment ID"}
                    },
                    "required": ["course_id", "assignment_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_assignment",
                "description": "Create a new assignment. Use this when user wants to create or add an assignment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "name": {"type": "string", "description": "The assignment name"},
                        "description": {"type": "string", "description": "Assignment description (HTML allowed)"},
                        "points_possible": {"type": "number", "description": "Maximum points"},
                        "due_at": {"type": "string", "description": "Due date in ISO 8601 format"},
                        "submission_types": {"type": "array", "items": {"type": "string"}, "description": "Allowed submission types"},
                        "published": {"type": "boolean", "description": "Publish immediately"},
                        "grading_type": {"type": "string", "description": "Grading method: points, pass_fail, percent, letter_grade, gpa_scale, not_graded"}
                    },
                    "required": ["course_id", "name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_assignment",
                "description": "Update an existing assignment. Use this when user wants to modify an assignment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "assignment_id": {"type": "integer", "description": "The assignment ID"},
                        "name": {"type": "string", "description": "New assignment name"},
                        "description": {"type": "string", "description": "New description (HTML allowed)"},
                        "points_possible": {"type": "number", "description": "New maximum points"},
                        "due_at": {"type": "string", "description": "New due date in ISO 8601 format"},
                        "published": {"type": "boolean", "description": "Published status"}
                    },
                    "required": ["course_id", "assignment_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_assignment",
                "description": "Delete an assignment. DESTRUCTIVE ACTION - requires confirmation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "assignment_id": {"type": "integer", "description": "The assignment ID to delete"}
                    },
                    "required": ["course_id", "assignment_id"]
                }
            }
        }
    ]
    return [
        {
            "name": "list_assignments",
            "description": "List all assignments in a course. Use this when user asks about assignments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "search_term": {
                        "type": "string",
                        "description": "Search assignments by name"
                    },
                    "bucket": {
                        "type": "string",
                        "description": "Filter assignments by bucket",
                        "enum": ["past", "overdue", "undated", "ungraded", "upcoming", "future"]
                    }
                },
                "required": ["course_id"]
            }
        },
        {
            "name": "get_assignment",
            "description": "Get details about a specific assignment. Use this when user asks about a specific assignment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "assignment_id": {
                        "type": "integer",
                        "description": "The assignment ID"
                    }
                },
                "required": ["course_id", "assignment_id"]
            }
        },
        {
            "name": "create_assignment",
            "description": "Create a new assignment. Use this when user wants to create, add, or make a new assignment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "The assignment name"
                    },
                    "description": {
                        "type": "string",
                        "description": "The assignment description in HTML format"
                    },
                    "points_possible": {
                        "type": "number",
                        "description": "Maximum points for the assignment"
                    },
                    "due_at": {
                        "type": "string",
                        "description": "Due date in ISO 8601 format (e.g., '2024-03-15T23:59:00Z')"
                    },
                    "submission_types": {
                        "type": "array",
                        "description": "Types of submissions allowed",
                        "items": {
                            "type": "string",
                            "enum": ["online_text_entry", "online_url", "online_upload", "media_recording", "on_paper", "external_tool", "none"]
                        }
                    },
                    "published": {
                        "type": "boolean",
                        "description": "Whether to publish immediately",
                        "default": False
                    },
                    "grading_type": {
                        "type": "string",
                        "description": "How the assignment is graded",
                        "enum": ["points", "pass_fail", "percent", "letter_grade", "gpa_scale", "not_graded"],
                        "default": "points"
                    }
                },
                "required": ["course_id", "name"]
            }
        },
        {
            "name": "update_assignment",
            "description": "Update an existing assignment. Use this when user wants to modify, edit, or change an assignment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "assignment_id": {
                        "type": "integer",
                        "description": "The assignment ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "New assignment name"
                    },
                    "description": {
                        "type": "string",
                        "description": "New assignment description in HTML"
                    },
                    "points_possible": {
                        "type": "number",
                        "description": "New maximum points"
                    },
                    "due_at": {
                        "type": "string",
                        "description": "New due date in ISO 8601 format"
                    },
                    "published": {
                        "type": "boolean",
                        "description": "Whether the assignment should be published"
                    }
                },
                "required": ["course_id", "assignment_id"]
            }
        },
        {
            "name": "delete_assignment",
            "description": "Delete an assignment. DESTRUCTIVE ACTION - requires confirmation. Use this when user explicitly wants to delete or remove an assignment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "assignment_id": {
                        "type": "integer",
                        "description": "The assignment ID to delete"
                    }
                },
                "required": ["course_id", "assignment_id"]
            }
        }
    ]

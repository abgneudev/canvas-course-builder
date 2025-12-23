"""Course management function tools for Groq."""
from typing import List, Dict, Any


def get_course_tools() -> List[Dict[str, Any]]:
    """Get function declarations for course operations.
    
    Returns:
        List of function declarations in OpenAI-compatible format
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "list_courses",
                "description": "List all courses for the current user. Use this when user asks about their courses, what courses they have, or wants to see their course list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "enrollment_type": {
                            "type": "string",
                            "description": "Filter by enrollment type: teacher, student, ta, observer, designer"
                        },
                        "enrollment_state": {
                            "type": "string",
                            "description": "Filter by enrollment state: active, invited_or_pending, completed"
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_course",
                "description": "Get details about a specific course. Use this when user asks about a specific course's information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {
                            "type": "integer",
                            "description": "The Canvas course ID"
                        }
                    },
                    "required": ["course_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_course",
                "description": "Create a new course. Use this when user wants to create or add a new course.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "integer",
                            "description": "The account ID to create the course in (usually 1 for main account)"
                        },
                        "name": {
                            "type": "string",
                            "description": "The course name"
                        },
                        "course_code": {
                            "type": "string",
                            "description": "The course code (e.g., 'CS101', 'MATH201')"
                        },
                        "start_at": {
                            "type": "string",
                            "description": "Course start date in ISO 8601 format (e.g., '2024-01-15T00:00:00Z')"
                        },
                        "end_at": {
                            "type": "string",
                            "description": "Course end date in ISO 8601 format"
                        }
                    },
                    "required": ["account_id", "name", "course_code"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_course",
                "description": "Update course information or publish/unpublish a course. Use this when user wants to change course details or publish/unpublish it.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {
                            "type": "integer",
                            "description": "The Canvas course ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "New course name"
                        },
                        "course_code": {
                            "type": "string",
                            "description": "New course code"
                        },
                        "event": {
                            "type": "string",
                            "description": "Course event: 'offer' to publish, 'claim' to unpublish, 'conclude' to end, 'delete' to delete, 'undelete' to restore"
                        }
                    },
                    "required": ["course_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_course",
                "description": "Delete or conclude a course. DESTRUCTIVE ACTION - requires confirmation. Use this when user explicitly wants to delete or conclude a course.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {
                            "type": "integer",
                            "description": "The Canvas course ID"
                        },
                        "event": {
                            "type": "string",
                            "description": "'delete' to permanently delete, 'conclude' to end the course"
                        }
                    },
                    "required": ["course_id", "event"]
                }
            }
        }
    ]

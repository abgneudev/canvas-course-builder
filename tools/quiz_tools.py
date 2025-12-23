"""Quiz management function tools for Groq."""
from typing import List, Dict, Any


def get_quiz_tools() -> List[Dict[str, Any]]:
    """Get function declarations for quiz operations.
    
    Returns:
        List of function declarations in OpenAI-compatible format
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "list_quizzes",
                "description": "List all quizzes in a course. Use this when user asks about quizzes or tests.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "search_term": {"type": "string", "description": "Search quizzes by title"}
                    },
                    "required": ["course_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_quiz",
                "description": "Get details about a specific quiz. Use this when user asks about a specific quiz.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "quiz_id": {"type": "integer", "description": "The quiz ID"}
                    },
                    "required": ["course_id", "quiz_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_quiz",
                "description": "Create a new quiz. Use this when user wants to create a quiz or test.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "title": {"type": "string", "description": "The quiz title"},
                        "description": {"type": "string", "description": "Quiz description (HTML allowed)"},
                        "quiz_type": {"type": "string", "description": "Quiz type: practice_quiz, assignment, graded_survey, survey"},
                        "time_limit": {"type": "integer", "description": "Time limit in minutes"},
                        "shuffle_answers": {"type": "boolean", "description": "Shuffle answer order"},
                        "allowed_attempts": {"type": "integer", "description": "Attempts allowed (-1 for unlimited)"},
                        "scoring_policy": {"type": "string", "description": "Scoring: keep_highest, keep_latest, keep_average"},
                        "due_at": {"type": "string", "description": "Due date in ISO 8601 format"},
                        "published": {"type": "boolean", "description": "Publish immediately"}
                    },
                    "required": ["course_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_quiz",
                "description": "Update an existing quiz. Use this when user wants to modify a quiz.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "quiz_id": {"type": "integer", "description": "The quiz ID"},
                        "title": {"type": "string", "description": "New quiz title"},
                        "description": {"type": "string", "description": "New description (HTML allowed)"},
                        "time_limit": {"type": "integer", "description": "New time limit in minutes"},
                        "published": {"type": "boolean", "description": "Published status"}
                    },
                    "required": ["course_id", "quiz_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_quiz",
                "description": "Delete a quiz. DESTRUCTIVE ACTION - requires confirmation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {"type": "integer", "description": "The Canvas course ID"},
                        "quiz_id": {"type": "integer", "description": "The quiz ID to delete"}
                    },
                    "required": ["course_id", "quiz_id"]
                }
            }
        }
    ]
    return [
        {
            "name": "list_quizzes",
            "description": "List all quizzes in a course. Use this when user asks about quizzes or tests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "search_term": {
                        "type": "string",
                        "description": "Search quizzes by title"
                    }
                },
                "required": ["course_id"]
            }
        },
        {
            "name": "get_quiz",
            "description": "Get details about a specific quiz. Use this when user asks about a specific quiz.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "quiz_id": {
                        "type": "integer",
                        "description": "The quiz ID"
                    }
                },
                "required": ["course_id", "quiz_id"]
            }
        },
        {
            "name": "create_quiz",
            "description": "Create a new quiz. Use this when user wants to create, add, or make a new quiz or test.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "The quiz title"
                    },
                    "description": {
                        "type": "string",
                        "description": "The quiz description in HTML format"
                    },
                    "quiz_type": {
                        "type": "string",
                        "description": "The type of quiz",
                        "enum": ["practice_quiz", "assignment", "graded_survey", "survey"],
                        "default": "assignment"
                    },
                    "time_limit": {
                        "type": "integer",
                        "description": "Time limit in minutes"
                    },
                    "shuffle_answers": {
                        "type": "boolean",
                        "description": "Whether to shuffle answer order",
                        "default": False
                    },
                    "allowed_attempts": {
                        "type": "integer",
                        "description": "Number of attempts allowed (-1 for unlimited)",
                        "default": 1
                    },
                    "scoring_policy": {
                        "type": "string",
                        "description": "How to score multiple attempts",
                        "enum": ["keep_highest", "keep_latest", "keep_average"],
                        "default": "keep_highest"
                    },
                    "due_at": {
                        "type": "string",
                        "description": "Due date in ISO 8601 format"
                    },
                    "published": {
                        "type": "boolean",
                        "description": "Whether to publish immediately",
                        "default": False
                    }
                },
                "required": ["course_id", "title"]
            }
        },
        {
            "name": "update_quiz",
            "description": "Update an existing quiz. Use this when user wants to modify, edit, or change a quiz.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "quiz_id": {
                        "type": "integer",
                        "description": "The quiz ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "New quiz title"
                    },
                    "description": {
                        "type": "string",
                        "description": "New quiz description in HTML"
                    },
                    "time_limit": {
                        "type": "integer",
                        "description": "New time limit in minutes"
                    },
                    "published": {
                        "type": "boolean",
                        "description": "Whether the quiz should be published"
                    }
                },
                "required": ["course_id", "quiz_id"]
            }
        },
        {
            "name": "delete_quiz",
            "description": "Delete a quiz. DESTRUCTIVE ACTION - requires confirmation. Use this when user explicitly wants to delete or remove a quiz.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The Canvas course ID"
                    },
                    "quiz_id": {
                        "type": "integer",
                        "description": "The quiz ID to delete"
                    }
                },
                "required": ["course_id", "quiz_id"]
            }
        }
    ]

"""Utility to gather all Canvas tools for the AI assistant"""
from tools.course_tools import get_course_tools
from tools.module_tools import get_module_tools
from tools.page_tools import get_page_tools
from tools.assignment_tools import get_assignment_tools
from tools.quiz_tools import get_quiz_tools
from tools.discussion_tools import get_discussion_tools


def get_all_canvas_tools(canvas_client):
    """Get all available Canvas tools with their functions.
    
    Args:
        canvas_client: The Canvas API client
        
    Returns:
        List of tool dictionaries with name, description, and function
    """
    all_tools = []
    
    # Get all tool modules
    tool_modules = [
        get_course_tools,
        get_module_tools,
        get_page_tools,
        get_assignment_tools,
        get_quiz_tools,
        get_discussion_tools
    ]
    
    # Collect tools from each module
    for get_tools_func in tool_modules:
        tools = get_tools_func()  # Call without arguments
        all_tools.extend(tools)
    
    # Create a mapping of tool names to canvas_client methods
    tool_map = {}
    for tool in all_tools:
        function_def = tool.get('function', {})
        tool_name = function_def.get('name')
        if tool_name and hasattr(canvas_client, tool_name):
            tool_map[tool_name] = {
                'name': tool_name,
                'description': function_def.get('description', ''),
                'parameters': function_def.get('parameters', {}),
                'function': getattr(canvas_client, tool_name)
            }
    
    return list(tool_map.values())


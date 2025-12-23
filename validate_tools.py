import inspect
from canvas_client import CanvasClient
from convert_tools import get_all_canvas_tools


def validate_tools():
    """Validate tool definitions against CanvasClient methods."""
    client = CanvasClient("https://example.com", "dummy")
    tools = get_all_canvas_tools(client)

    errors = []
    for tool in tools:
        name = tool['name']

        # Check method exists
        if not hasattr(client, name):
            errors.append(f"❌ {name}: Method not found in CanvasClient")
            continue

        method = getattr(client, name)
        sig = inspect.signature(method)
        method_params = set(sig.parameters.keys()) - {'self'}

        # Get tool params
        tool_params = tool.get('parameters', {})
        tool_props = tool_params.get('properties', {}) if isinstance(tool_params, dict) else {}
        defined_params = set(tool_props.keys())

        # Compare
        missing_in_method = defined_params - method_params
        missing_in_tool = method_params - defined_params

        if missing_in_method:
            errors.append(f"⚠️ {name}: Tool defines {missing_in_method} but method doesn't accept them")
        if missing_in_tool:
            errors.append(f"ℹ️ {name}: Method accepts {missing_in_tool} but tool doesn't define them")

    if errors:
        print("VALIDATION ERRORS:")
        for err in errors:
            print(err)
    else:
        print("✅ All tools validated successfully!")


if __name__ == "__main__":
    validate_tools()

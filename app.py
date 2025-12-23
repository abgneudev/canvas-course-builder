"""Canvas LMS AI Assistant - Streamlit Chat Application
Allows instructors to manage Canvas LMS through natural language using Groq.
"""
import streamlit as st
import os
import json
import logging
from dotenv import load_dotenv
from canvas_client import CanvasClient
from groq_service import GroqService
from convert_tools import get_all_canvas_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Canvas AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #E13C2D;
        text-align: center;
        padding: 1rem 0;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
    }
    .user-message {
        background-color: #f0f2f6;
    }
    .assistant-message {
        background-color: #ffffff;
    }
    .sidebar-info {
        padding: 1rem;
        background-color: #f0f8ff;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'groq_service' not in st.session_state:
        try:
            # Get API credentials from environment
            canvas_token = os.getenv('CANVAS_API_TOKEN')
            canvas_url = os.getenv('CANVAS_BASE_URL', 'https://canvas.instructure.com')
            groq_key = os.getenv('GROQ_API_KEY')
            
            if not canvas_token:
                st.error("⚠️ Missing Canvas API credentials! Please check your .env file.")
                st.stop()
            if not groq_key:
                st.error("⚠️ Missing GROQ_API_KEY! Please add it to your .env file.")
                st.stop()
            
            # Initialize clients
            canvas_client = CanvasClient(canvas_url, canvas_token)
            groq_service = GroqService(model="llama-3.1-8b-instant")
            
            st.session_state.groq_service = groq_service
            st.session_state.canvas_client = canvas_client
            st.session_state.available_tools = get_all_canvas_tools(canvas_client)
            
            logger.info(f"Initialized {len(st.session_state.available_tools)} Canvas tools")
            # Log first few tools for debugging
            for tool in st.session_state.available_tools[:5]:
                params = tool.get('parameters', {})
                props = params.get('properties', {}) if isinstance(params, dict) else {}
                logger.info(f"Tool: {tool['name']}, params: {list(props.keys())}")
            
        except Exception as e:
            st.error(f"❌ Failed to initialize services: {str(e)}")
            st.stop()
    
    if 'current_course_id' not in st.session_state:
        st.session_state.current_course_id = None
    
    if 'pending_confirmation' not in st.session_state:
        st.session_state.pending_confirmation = None


def convert_argument_types(arguments, tool_props):
    """Convert argument types based on tool schema."""
    converted = {}
    for key, value in arguments.items():
        if key not in tool_props:
            converted[key] = value
            continue

        expected_type = tool_props[key].get('type', 'string') if isinstance(tool_props[key], dict) else 'string'

        if expected_type == 'integer' and isinstance(value, str):
            try:
                converted[key] = int(value)
            except ValueError:
                converted[key] = value
        elif expected_type == 'boolean':
            if isinstance(value, str):
                converted[key] = value.lower() in ('true', '1', 'yes')
            else:
                converted[key] = bool(value)
        elif expected_type == 'number' and isinstance(value, str):
            try:
                converted[key] = float(value)
            except ValueError:
                converted[key] = value
        else:
            converted[key] = value

    return converted


def detect_placeholders(arguments):
    """Raise if any placeholder-like values are detected."""
    placeholder_patterns = ['<YOUR_', '<HTML_', '<INSERT_', '<COURSE_', '<PAGE_', '<MODULE_']
    for key, value in arguments.items():
        if isinstance(value, str):
            upper_val = value.upper()
            if any(pat in upper_val for pat in placeholder_patterns):
                raise ValueError(f"Invalid placeholder value for '{key}': {value}. Please provide an actual value.")
            # Treat single-tag style <PLACEHOLDER> as invalid, but allow real HTML content
            stripped = value.strip()
            if stripped.startswith('<') and stripped.endswith('>') and '</' not in stripped:
                raise ValueError(f"Placeholder detected in '{key}': {value}")


def render_sidebar():
    """Render sidebar with configuration and course context."""
    with st.sidebar:
        st.markdown('<div class="main-header">🎓 Canvas AI</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Course context selector
        st.subheader("📚 Course Context")
        
        try:
            # Fetch user's courses
            courses = st.session_state.canvas_client.list_courses(
                enrollment_type='teacher',
                enrollment_state='active'
            )
            
            if courses:
                course_options = {
                    "None - Ask me each time": None
                }
                
                for course in courses:
                    course_name = course.get('name', 'Unnamed Course')
                    course_id = course.get('id')
                    course_options[f"{course_name} (ID: {course_id})"] = course_id
                
                selected = st.selectbox(
                    "Set default course:",
                    options=list(course_options.keys()),
                    index=0,
                    help="Set a default course for operations, or let the AI ask when needed"
                )
                
                st.session_state.current_course_id = course_options[selected]
                
                if st.session_state.current_course_id:
                    st.success(f"✅ Course context set to ID: {st.session_state.current_course_id}")
            else:
                st.info("No active courses found")
                
        except Exception as e:
            st.warning(f"Could not load courses: {str(e)}")
        
        st.markdown("---")
        
        # Information section
        st.subheader("ℹ️ How to Use")
        st.markdown("""
        **Example Commands:**
        - "List my courses"
        - "Show modules in course 12345"
        - "Create a page called 'Welcome'"
        - "List all assignments"
        - "Create a quiz for next week"
        - "Post an announcement"
        
        **Tips:**
        - Be specific with course IDs when needed
        - Use natural language
        - Confirm destructive operations
        """)
        
        st.markdown("---")
        
        # Connection status
        st.subheader("🔌 Status")
        canvas_url = os.getenv('CANVAS_BASE_URL', 'https://canvas.instructure.com')
        st.markdown(f"""
        <div class="sidebar-info">
            <strong>Canvas:</strong> ✅ Connected<br>
            <strong>URL:</strong> {canvas_url}<br>
            <strong>AI Model:</strong> Llama 3.3 70B Versatile (Groq Cloud)<br>
            <strong>Function Tools:</strong> 33+ operations
        </div>
        """, unsafe_allow_html=True)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pending_confirmation = None
            st.rerun()


def render_chat():
    """Render chat interface."""
    st.markdown('<div class="main-header">Canvas LMS AI Assistant</div>', unsafe_allow_html=True)
    st.markdown("### Ask me anything about your Canvas courses! 💬")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Check if we're responding to a confirmation request
        if st.session_state.pending_confirmation:
            if prompt.lower() in ['yes', 'y', 'confirm', 'ok']:
                # User confirmed - execute the pending function
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("Processing..."):
                        try:
                            # Execute the pending function call
                            function_name = st.session_state.pending_confirmation['function_name']
                            arguments = st.session_state.pending_confirmation['arguments']
                            print(f"[INFO] Executing tool: {function_name} with args: {arguments}")
                            
                            # Validate tool exists
                            tool_names = [t['name'] for t in st.session_state.available_tools]
                            if function_name not in tool_names:
                                response_text = f"❌ Invalid tool '{function_name}'. Available tools: {', '.join(tool_names[:10])}..."
                                print(f"[ERROR] Invalid tool name: {function_name}")
                                st.markdown(response_text)
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response_text
                                })
                                st.session_state.pending_confirmation = None
                                st.rerun()
                            
                            # Find and execute the tool
                            for tool in st.session_state.available_tools:
                                if tool['name'] == function_name:
                                    print(f"[INFO] Found tool: {tool['name']}")
                                    # Log expected parameters
                                    params = tool.get('parameters', {})
                                    props = params.get('properties', {}) if isinstance(params, dict) else {}
                                    expected_params = list(props.keys())
                                    received_params = list(arguments.keys())
                                    print(f"[INFO] Expected parameters: {expected_params}")
                                    print(f"[INFO] Received parameters: {received_params}")

                                    # Auto-inject course_id from sidebar context
                                    if st.session_state.current_course_id and 'course_id' in expected_params:
                                        if not arguments.get('course_id'):
                                            arguments['course_id'] = st.session_state.current_course_id
                                            print(f"[INFO] Auto-injected course_id: {st.session_state.current_course_id}")
                                    
                                    # Map common parameter mismatches
                                    param_aliases = {
                                        'content': 'body',           # pages use body
                                        'subject': 'title',          # announcements use title
                                        'body': 'message',           # announcements/discussions use message
                                        'is_published': 'published'  # some tools expect published
                                    }
                                    for incoming, target in param_aliases.items():
                                        if incoming in arguments and incoming not in expected_params and target in expected_params:
                                            print(f"[INFO] Mapping '{incoming}' to '{target}'")
                                            arguments[target] = arguments.pop(incoming)

                                    # Special handling: include_items -> include=["items"] for list_modules
                                    if 'include_items' in arguments:
                                        include_items_value = arguments.pop('include_items')
                                        if include_items_value in [True, 'true', 'True', '1']:
                                            print("[INFO] Mapping 'include_items' to include=['items']")
                                            arguments['include'] = ['items']

                                    # Convert argument types based on schema
                                    arguments = convert_argument_types(arguments, props)

                                    # Filter out unexpected parameters
                                    filtered_args = {k: v for k, v in arguments.items() if k in expected_params}
                                    removed = set(arguments.keys()) - set(filtered_args.keys())
                                    if removed:
                                        print(f"[INFO] Filtered args: {filtered_args} (removed: {removed})")
                                    else:
                                        print(f"[INFO] Filtered args: {filtered_args}")

                                    # Validate placeholder-like inputs
                                    detect_placeholders(filtered_args)
                                    
                                    # Validate update_course events
                                    if function_name == 'update_course' and 'event' in filtered_args:
                                        valid_events = ['offer', 'claim', 'conclude', 'delete', 'undelete']
                                        if filtered_args['event'] not in valid_events:
                                            response_text = f"❌ Invalid event '{filtered_args['event']}' for update_course. Valid events: {', '.join(valid_events)}"
                                            print(f"[ERROR] Invalid update_course event: {filtered_args['event']}")
                                            break
                                    
                                    result = tool['function'](**filtered_args)
                                    print(f"[DEBUG] Raw tool result: {result}")

                                    # Render friendly output for lists of courses or generic lists
                                    if isinstance(result, list):
                                        if not result:
                                            response_text = "No results returned. If you expected courses, check enrollment type/state (e.g., try enrollment_type='teacher', enrollment_state='active')."
                                        else:
                                            # Try to format list of dicts with name/id
                                            lines = []
                                            for item in result[:20]:  # cap output
                                                if isinstance(item, dict):
                                                    name = item.get('name') or item.get('title') or item.get('short_name') or 'Unnamed'
                                                    cid = item.get('id') or item.get('course_id') or item.get('uuid')
                                                    lines.append(f"- {name} (ID: {cid})")
                                                else:
                                                    lines.append(f"- {item}")
                                            more = "\n…" if len(result) > 20 else ""
                                            response_text = "✅ Operation completed successfully!\n\n" + "\n".join(lines) + more
                                    else:
                                        response_text = f"✅ Operation completed successfully!\n\n{result}"
                                    break
                            else:
                                response_text = f"❌ Tool '{function_name}' not found."
                                print(f"[ERROR] Tool '{function_name}' not found in available tools")
                            
                            st.markdown(response_text)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response_text
                            })
                        except Exception as e:
                            error_msg = f"❌ Error: {str(e)}"
                            print(f"[ERROR] Error executing tool: {str(e)}")
                            import traceback
                            traceback.print_exc()
                            st.error(error_msg)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": error_msg
                            })
                
                # Clear pending confirmation
                st.session_state.pending_confirmation = None
                
            elif prompt.lower() in ['no', 'n', 'cancel']:
                # User cancelled
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                cancel_msg = "✅ Operation cancelled. No changes were made."
                
                with st.chat_message("assistant"):
                    st.markdown(cancel_msg)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": cancel_msg
                })
                
                # Clear pending confirmation
                st.session_state.pending_confirmation = None
            else:
                # Invalid response to confirmation
                with st.chat_message("assistant"):
                    st.warning("Please respond with 'yes' or 'no' to the confirmation request.")
        
        else:
            # Normal message processing
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Prepare messages for Groq
                        chat_messages = [
                            {"role": msg["role"], "content": msg["content"]}
                            for msg in st.session_state.messages[-10:]  # Keep last 10 messages for context
                        ]
                        
                        # Get response from Groq
                        response_text = st.session_state.groq_service.chat(
                            chat_messages,
                            st.session_state.available_tools
                        )
                        
                        # Check if response contains a tool call (support multiple JSON blocks)
                        pending_confirmation = None
                        tool_call_found = False
                        if "{" in response_text and "tool" in response_text:
                            try:
                                # Scan all brace ranges to find the first valid tool call JSON
                                text_len = len(response_text)
                                found = None
                                for start_idx in [i for i, ch in enumerate(response_text) if ch == "{"]:
                                    for end_idx in range(text_len, start_idx, -1):
                                        if response_text[end_idx - 1] == "}":
                                            snippet = response_text[start_idx:end_idx]
                                            try:
                                                obj = json.loads(snippet)
                                            except json.JSONDecodeError:
                                                continue
                                            if isinstance(obj, dict) and "tool" in obj and "parameters" in obj:
                                                found = obj
                                                break
                                    if found:
                                        break
                                if found:
                                    tool_call = found
                                    print(f"[INFO] Parsed tool call: {tool_call}")
                                    pending_confirmation = {
                                        "function_name": tool_call["tool"],
                                        "arguments": tool_call["parameters"]
                                    }
                                    tool_call_found = True
                                    response_text = f"I want to call '{tool_call['tool']}' with these parameters:\n\n{json.dumps(tool_call['parameters'], indent=2)}\n\nDo you want to proceed? (yes/no)"
                            except Exception as e:
                                print(f"[ERROR] Tool call parse error: {e}")
                        
                        # Detect if model is claiming to have performed actions without tool calls
                        action_phrases = ['has been', 'successfully', 'created', 'updated', 'added', 'deleted', 'i have', 'i will', "i've"]
                        if not tool_call_found and any(phrase in response_text.lower() for phrase in action_phrases):
                            if 'course' in prompt.lower() or 'page' in prompt.lower() or 'module' in prompt.lower() or 'announcement' in prompt.lower():
                                print("[WARNING] Model may be hallucinating an action without calling a tool")
                                response_text += "\n\n⚠️ Note: No Canvas action was executed because no tool call was issued. Please provide a clear request so I can call the correct tool."
                        
                        # If no tool call was parsed and user asked to list courses, fall back to real API call to avoid hallucinations
                        if not pending_confirmation and 'list' in prompt.lower() and 'course' in prompt.lower():
                            try:
                                result = st.session_state.canvas_client.list_courses(
                                    enrollment_type='teacher',
                                    enrollment_state='active'
                                )
                                if result:
                                    lines = []
                                    for item in result[:20]:
                                        if isinstance(item, dict):
                                            name = item.get('name') or item.get('title') or item.get('short_name') or 'Unnamed'
                                            cid = item.get('id') or item.get('course_id') or item.get('uuid')
                                            lines.append(f"- {name} (ID: {cid})")
                                        else:
                                            lines.append(f"- {item}")
                                    more = "\n…" if len(result) > 20 else ""
                                    response_text = "✅ Courses:\n\n" + "\n".join(lines) + more
                                else:
                                    response_text = "No courses found for your teacher enrollments. Try changing enrollment_type/state."
                            except Exception as e:
                                response_text = f"❌ Error listing courses: {e}"

                        st.markdown(response_text)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text
                        })

                        # Store pending confirmation if there is one
                        if pending_confirmation:
                            st.session_state.pending_confirmation = pending_confirmation
                            
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}\n\nPlease check your API credentials and try again."
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })
        
        st.rerun()


def main():
    """Main application entry point."""
    # Initialize session
    initialize_session()
    
    # Render UI
    render_sidebar()
    render_chat()
    
    # Welcome message
    if not st.session_state.messages:
        welcome_msg = """
        👋 **Welcome to Canvas AI Assistant!**
        
        I can help you manage your Canvas LMS courses through natural language. Here are some things I can do:
        
        **📚 Courses**
        - List and view your courses
        - Create, update, or manage courses
        
        **📖 Modules & Pages**
        - Create and organize course modules
        - Add pages with rich content
        
        **📝 Assignments & Quizzes**
        - Create assignments with due dates
        - Set up quizzes and tests
        
        **💬 Discussions & Announcements**
        - Start discussion topics
        - Post announcements to your courses
        
        Just type your request in natural language, and I'll handle the rest! 
        
        **Example:** "List my courses" or "Create a welcome page for course 12345"
        """
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg
        })
        
        with st.chat_message("assistant"):
            st.markdown(welcome_msg)


if __name__ == "__main__":
    main()

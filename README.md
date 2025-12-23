# Canvas LMS AI Assistant

A complete Streamlit chat application that allows instructors to manage Canvas LMS through natural language using Groq's Llama 3.3 70B with function calling.

## ✨ Features

### 🎯 Core Capabilities
- **Natural Language Interface**: Interact with Canvas using conversational language
- **AI-Powered Function Calling**: Llama 3.3 70B automatically selects and executes the right Canvas API operations
- **33+ Canvas Operations**: Comprehensive support for courses, modules, pages, assignments, quizzes, and discussions
- **Smart Course Context**: Set a default course or let the AI infer context from your requests
- **Confirmation for Destructive Actions**: Safety mechanism for delete operations
- **Rich Content Support**: Create pages, assignments, and discussions with HTML formatting

### 📚 Supported Operations

#### Courses
- List courses with filters (enrollment type, state)
- Get course details
- Create new courses
- Update course settings
- Publish/unpublish courses
- Delete or conclude courses

#### Modules
- List all modules in a course
- Create modules with prerequisites
- Add items to modules (pages, assignments, quizzes, etc.)
- Update module settings
- Delete modules

#### Pages
- List and search pages
- Create pages with HTML content
- Update existing pages
- Set front page
- Delete pages

#### Assignments
- List assignments with filters
- Create assignments with submission types, due dates, and points
- Update assignment settings
- Delete assignments

#### Quizzes
- List quizzes
- Create quizzes with time limits, attempts, and scoring policies
- Update quiz settings
- Delete quizzes

#### Discussions & Announcements
- List discussion topics
- Create discussions (threaded or side comments)
- Post announcements
- Reply to discussions
- Delete discussions

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com/keys))
- Canvas LMS API token ([Generate from Canvas Account Settings](https://canvas.instructure.com/profile/settings))
- Canvas instance URL

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the project root:
```env
# Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# Canvas LMS Configuration
CANVAS_API_TOKEN=your_canvas_api_token_here
CANVAS_BASE_URL=https://canvas.instructure.com

# For institution-specific Canvas instances, use your institution's URL:
# CANVAS_BASE_URL=https://canvas.youruniversity.edu
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 💬 Usage Examples

### Getting Started
- "List my courses"
- "Show me my active courses"
- "What courses am I teaching?"

### Working with Modules
- "Show modules in course 12345"
- "Create a module called 'Week 1: Introduction'"
- "Add a page to module 456"

### Creating Content
- "Create a page called 'Welcome to the Course' with some introductory content"
- "Make an assignment called 'Essay 1' worth 100 points due next Friday"
- "Create a practice quiz with 10 attempts allowed"

### Announcements & Discussions
- "Post an announcement about the upcoming exam"
- "Create a discussion topic about climate change"
- "Start a threaded discussion for group projects"

### Managing Content
- "Update the due date for assignment 789"
- "Publish the module called 'Week 2'"
- "Delete the page named 'Old Syllabus'"

## 🏗️ Project Structure

```
canvas-mcp/
├── app.py                      # Main Streamlit application
├── canvas_client.py            # Canvas API client with all endpoints
├── groq_service.py             # Groq service with function calling
├── convert_tools.py            # Utility to aggregate all Canvas tools
├── validate_tools.py           # Tool validation utilities
├── tools/
│   ├── __init__.py
│   ├── course_tools.py         # Course function declarations
│   ├── module_tools.py         # Module function declarations
│   ├── page_tools.py           # Page function declarations
│   ├── assignment_tools.py     # Assignment function declarations
│   ├── quiz_tools.py           # Quiz function declarations
│   └── discussion_tools.py     # Discussion function declarations
├── utils/
│   ├── __init__.py
│   └── html_helpers.py         # HTML formatting utilities
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── OLLAMA_SETUP.md             # Guide for using Ollama (local LLM)
└── README.md                   # This file
```

## 🔒 Security Notes

- **Never commit your `.env` file** - it contains sensitive API keys
- Keep your Canvas API token secure - it has full access to your Canvas account
- Use a dedicated Canvas account for testing if possible
- The app includes confirmation prompts for all destructive operations (delete, conclude)

## 🎨 Customization

### Adding New Functions
1. Add the function to `canvas_client.py`
2. Create function declaration in the appropriate tool file (e.g., `tools/course_tools.py`)
3. The function will be automatically picked up by `convert_tools.py`

### Styling
- Modify CSS in `app.py` to change the appearance
- Update HTML helpers in `utils/html_helpers.py` for rich content formatting

### System Prompt
- Edit the system instruction in `groq_service.py` `_create_system_prompt()` to change AI behavior

### Switching AI Models
- **Groq Models**: Change model in `groq_service.py` (llama-3.3-70b-versatile, llama-3.1-8b-instant, etc.)
- **Local LLM**: See `OLLAMA_SETUP.md` for instructions on using Ollama

## 📋 Technical Details

### Architecture
- **Frontend**: Streamlit (chat interface, sidebar, session state)
- **AI Model**: Groq Cloud with Llama 3.3 70B Versatile
- **API Client**: Custom Canvas REST API client using `requests`
- **Tool System**: Modular tool declarations with OpenAI-compatible format
- **Function Calling Flow**:
  1. User sends natural language message
  2. Groq/Llama interprets intent and selects appropriate function
  3. Function call is confirmed by user (for safety)
  4. Function is executed against Canvas API
  5. Result is formatted and displayed to user

### Tool Architecture
- **6 Tool Modules**: Organized by Canvas resource type (courses, modules, pages, assignments, quizzes, discussions)
- **33+ Operations**: Comprehensive CRUD operations for Canvas LMS
- **Auto-Discovery**: Tools are automatically aggregated from modules via `convert_tools.py`
- **Type Conversion**: Automatic parameter type conversion and validation

### Error Handling
- API errors are caught and translated to user-friendly messages
- Invalid inputs are validated before API calls
- Placeholder detection prevents common mistakes
- Destructive operations require explicit user confirmation

### Session Management
- Chat history is maintained in Streamlit session state (last 10 messages for context)
- Course context can be set globally or per-request
- Pending confirmations tracked across user interactions

### Dependencies
```
streamlit>=1.28.0       # Web UI framework
requests>=2.31.0        # HTTP client for Canvas API
python-dotenv>=1.0.0    # Environment variable management
groq>=0.5.0             # Groq API client for LLM inference
```

### Key Features Implementation
- **Automatic Type Conversion**: Arguments are automatically converted to expected types (integers, booleans, etc.)
- **Parameter Aliasing**: Common parameter variations are automatically mapped (e.g., 'content' → 'body')
- **Placeholder Detection**: Prevents execution of functions with placeholder values like `<YOUR_ID>`
- **Course Context Injection**: Automatically injects course_id from sidebar context when needed
- **Smart Fallbacks**: Automatic fallback for common queries (e.g., listing courses) when LLM doesn't generate tool calls

## 🐛 Troubleshooting

### "Missing API credentials" error
- Check that your `.env` file exists and contains `GROQ_API_KEY` and `CANVAS_API_TOKEN`
- Verify the API keys are correct and active
- Groq API keys can be obtained from https://console.groq.com/keys

### "Canvas API error: 401 Unauthorized"
- Your Canvas API token may be invalid or expired
- Generate a new token from Canvas Account Settings
- Ensure the token has not been revoked

### "Could not load courses"
- Check that `CANVAS_BASE_URL` is correct for your institution
- Verify your Canvas token has the necessary permissions
- Try specifying enrollment_type='teacher' and enrollment_state='active'

### "Error communicating with Groq"
- Verify `GROQ_API_KEY` is set correctly in your `.env` file
- Check your internet connection
- Verify Groq service is operational at https://status.groq.com

### Function not working
- Check if you have proper permissions in Canvas
- Some operations require specific Canvas roles (teacher, admin)
- Review the console logs for detailed error messages

## 📝 API Documentation

### Canvas API
- [Canvas REST API Documentation](https://canvas.instructure.com/doc/api/)
- [Canvas Developer Portal](https://canvas.instructure.com/doc/api/all_resources.html)
- [Canvas API Live Documentation](https://canvas.instructure.com/doc/api/live)

### Groq
- [Groq Cloud Documentation](https://console.groq.com/docs)
- [Groq API Reference](https://console.groq.com/docs/api-reference)
- [Groq Models](https://console.groq.com/docs/models)

## 🙏 Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web application framework
- [Groq](https://groq.com/) - Fast AI inference platform
- [Llama 3.3 70B](https://www.llama.com/) - Meta's open-source LLM
- [Canvas LMS](https://www.instructure.com/canvas) - Learning management system
- [Requests](https://requests.readthedocs.io/) - HTTP library
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management

## 📄 License

This project is provided as-is for educational and productivity purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 🔄 Alternative AI Providers

### Using Ollama (Local LLM)
Want to run the AI model locally for privacy and cost savings? See the [OLLAMA_SETUP.md](OLLAMA_SETUP.md) guide for instructions on:
- Installing Ollama
- Running local Llama models
- Configuring the app for offline use
- Benefits: Privacy, no API costs, offline operation

---

**Happy Teaching! 🎓**

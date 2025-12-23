"""Groq Service for Canvas LMS AI Assistant
Uses Groq chat completions to power tool-based interactions.
"""
import os
import json
import logging
from typing import List, Dict, Any
from groq import Groq

logger = logging.getLogger(__name__)


class GroqService:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY environment variable")
        self.client = Groq(api_key=api_key)
        self.model = model
        logger.info("GroqService initialized with model: %s", self.model)

    def _create_system_prompt(self, available_tools: List[Dict[str, Any]]) -> str:
        """Create a system prompt listing tools and parameters."""
        tools_list = []
        for tool in available_tools[:20]:  # limit to reduce tokens
            params = tool.get("parameters", {})
            properties = params.get("properties", {}) if isinstance(params, dict) else {}
            required = params.get("required", []) if isinstance(params, dict) else []

            param_strs = []
            for name, schema in properties.items():
                req_marker = "*" if name in required else ""
                param_strs.append(f"{name}{req_marker}")

            param_list = ", ".join(param_strs)
            desc = tool.get('description', '')[:100]
            tools_list.append(f"- {tool['name']}({param_list}): {desc}")

        tools_description = "\n".join(tools_list)

        return f"""You are a Canvas LMS assistant that helps instructors manage courses.

AVAILABLE TOOLS (* = required parameter):
{tools_description}

RULES:
1. To call a tool, output ONLY this JSON: {{"tool": "name", "parameters": {{...}}}}
2. Use EXACT parameter names shown above.
3. NEVER use placeholder values like <YOUR_COURSE_ID>. Ask for missing required values.
4. If you cannot find a suitable tool, say so; do not invent actions.
5. Do NOT claim an action was done unless you output a tool call JSON.
6. For HTML content, provide the actual HTML.

EXAMPLE:
User: "Create a page called Welcome in course 123"
Response: {{"tool": "create_page", "parameters": {{"course_id": 123, "title": "Welcome", "body": "<h1>Welcome</h1>"}}}}
"""

    def chat(self, messages: List[Dict[str, str]], available_tools: List[Dict[str, Any]] = None) -> str:
        """Send a chat completion request to Groq."""
        chat_messages = list(messages)
        if available_tools:
            system_prompt = self._create_system_prompt(available_tools)
            chat_messages.insert(0, {"role": "system", "content": system_prompt})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": m["role"], "content": m["content"]} for m in chat_messages],
                temperature=0.2,
            )
            content = completion.choices[0].message.content or ""
            logger.info("Groq response length: %s chars", len(content))
            logger.debug("Groq response: %s", content)
            return content
        except Exception as exc:  # noqa: BLE001
            logger.exception("Groq API error")
            return f"Error communicating with Groq: {exc}\n\nMake sure GROQ_API_KEY is set."

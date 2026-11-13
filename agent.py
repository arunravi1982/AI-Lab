import json
import os

from openai import OpenAI

from tools import (
    check_service,
    check_database,
    get_system_logs,
    check_disk_space
)

client = OpenAI()

MODEL = os.getenv("MODEL_NAME", "gpt-5-mini")

SYSTEM_INSTRUCTIONS = """
You are an intelligent IT Support AI Agent.

Your responsibilities:

1. Understand the user's request.
2. Decide which tool is required.
3. Call the appropriate tool.
4. Analyze the tool output.
5. Provide a clear and simple response.

Available services:
- payment
- database
- authentication
- notification

Rules:
- Use tools when the user asks for actual system information.
- Never invent service status or log information.
- If information is unavailable, clearly say so.
- Do not claim to have fixed an issue.
- Explain results in simple language.
"""

# Define tools available to the LLM

TOOLS = [
    {
        "type": "function",
        "name": "check_service",
        "description": "Check the health and status of an application service.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "Name of the service."
                }
            },
            "required": ["service_name"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "check_database",
        "description": "Check database connectivity and performance.",
        "parameters": {
            "type": "object",
            "properties": {
                "database_name": {
                    "type": "string",
                    "description": "Name of the database."
                }
            },
            "required": ["database_name"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_system_logs",
        "description": "Retrieve recent application logs.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "Name of the application service."
                }
            },
            "required": ["service_name"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "check_disk_space",
        "description": "Retrieve available disk space.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "Name of the application service."
                }
            },
            "required": ["service_name"],
            "additionalProperties": False
        },
        "strict": True
    }
]


# Execute the selected Python tool

def execute_tool(tool_name, arguments):

    if tool_name == "check_service":
        return check_service(**arguments)

    elif tool_name == "check_database":
        return check_database(**arguments)

    elif tool_name == "get_system_logs":
        return get_system_logs(**arguments)

        elif tool_name == "check_disk_space":
        return check_disk_space(**arguments)    

    return {"error": "Unknown tool."}


# Main agent execution loop

def run_agent(user_command):

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_INSTRUCTIONS,
        input=user_command,
        tools=TOOLS
    )

    # Maximum five tool execution rounds
    for iteration in range(5):

        function_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # No more tools required
        if not function_calls:
            return response.output_text

        tool_outputs = []

        for call in function_calls:

            arguments = json.loads(call.arguments)

            print("\n[AGENT ACTION]")
            print(f"Selected Tool: {call.name}")
            print(f"Tool Input: {arguments}")

            try:
                result = execute_tool(
                    call.name,
                    arguments
                )
            except Exception as error:
                result = {
                    "error": str(error)
                }

            print(f"Tool Result: {result}")

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result)
            })

        # Send tool results back to the LLM
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS
        )

    return "Agent stopped: maximum tool execution limit reached."
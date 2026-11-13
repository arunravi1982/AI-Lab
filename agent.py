import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools import (
    check_service,
    check_database,
    get_system_logs
)


# Load environment variables
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-mini")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY not found. Check your .env file."
    )


# Initialize the language model
llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0
)


# Define the agent's behavior
SYSTEM_PROMPT = """
You are an intelligent IT support investigation agent.

Your job is to investigate IT application problems using
the tools available to you.

Available tools:

1. check_service:
   Checks whether an application service is UP or DOWN.

2. check_database:
   Checks whether a database is AVAILABLE or UNAVAILABLE.

3. get_system_logs:
   Retrieves recent logs for an application service.

Instructions:

- Understand the user's request before taking action.
- Use the available tools when investigation is requested.
- For an application outage, check the relevant service.
- If the service is DOWN, inspect its logs.
- If the logs indicate a database problem, check the relevant database.
- Use tool results as evidence for your conclusions.
- Do not claim that an operation was performed unless a tool returned its result.
- Do not invent infrastructure details or confirmed root causes.
- Clearly distinguish observed facts from possible causes.
- If information is unavailable, say so.
- Provide a clear final investigation report.

You may use more than one tool when necessary.
Do not call tools unnecessarily for general questions.
"""


# Register tools with the agent
tools = [
    check_service,
    check_database,
    get_system_logs
]


# Create the agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


def run_agent(user_request):

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_request
            }
        ]
    })

    return response

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv()


@tool
def check_service(service_name: str) -> str:
    """Check the health status of an IT service."""

    return f"{service_name} service is running."


llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)

llm_with_tools = llm.bind_tools([check_service])

response = llm_with_tools.invoke(
    "Check whether the payment service is running."
)

print("Model response:")
print(response)

print("\nTool calls:")
print(response.tool_calls)

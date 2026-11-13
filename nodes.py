import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from tools import tools

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-mini")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env")


llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0
)

# Make the tools available to the model
llm_with_tools = llm.bind_tools(tools)


def llm_call(state):

    print("\n[GRAPH NODE] LLM is processing the request...")

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI

from langchain_core.messages import (
    SystemMessage,
    ToolMessage
)

from langchain_core.runnables import RunnableConfig

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode

from langgraph.checkpoint.memory import InMemorySaver

from langgraph.types import interrupt, Command

from app.config import (
    OPENAI_API_KEY,
    MODEL_NAME
)

from app.tools import ALL_TOOLS


# --------------------------------------------------
# 1. MODEL
# --------------------------------------------------

llm = ChatOpenAI(

    model=MODEL_NAME,

    temperature=0,

    api_key=OPENAI_API_KEY

)

llm_with_tools = llm.bind_tools(ALL_TOOLS)


# --------------------------------------------------
# 2. SYSTEM PROMPT
# --------------------------------------------------

SYSTEM_PROMPT = """
You are an enterprise IT Helpdesk Assistant.

Your responsibilities:

1. Answer IT questions using the knowledge base.
2. Check existing support tickets.
3. Create support tickets when requested.
4. Ask for missing information when required.

Rules:

- Use the appropriate tools.
- Never invent ticket information.
- Do not claim that a ticket was created unless
  the ticket creation tool returns success.
- Before creating a ticket, explain the proposed
  ticket details.
- The application will request human approval
  before executing ticket creation.
- Never bypass human approval.
- Be polite and concise.
"""


# --------------------------------------------------
# 3. GRAPH STATE
# --------------------------------------------------

class HelpdeskState(TypedDict):

    messages: Annotated[list, add_messages]

    approval_decision: str


# --------------------------------------------------
# 4. ASSISTANT NODE
# --------------------------------------------------

def assistant_node(
    state: HelpdeskState,
    config: RunnableConfig
):

    response = llm_with_tools.invoke(

        [
            SystemMessage(
                content=SYSTEM_PROMPT
            )
        ] + state["messages"],

        config=config

    )

    return {

        "messages": [response]

    }


# --------------------------------------------------
# 5. ROUTING
# --------------------------------------------------

def route_after_assistant(state):

    last_message = state["messages"][-1]

    tool_calls = getattr(
        last_message,
        "tool_calls",
        []
    )

    if not tool_calls:

        return END

    if any(

        call["name"] == "create_support_ticket"

        for call in tool_calls

    ):

        return "human_approval"

    return "tools"


# --------------------------------------------------
# 6. HUMAN APPROVAL
# --------------------------------------------------

def human_approval_node(state):

    last_message = state["messages"][-1]

    ticket_calls = [

        call

        for call in last_message.tool_calls

        if call["name"] == "create_support_ticket"

    ]

    approval_request = {

        "message": (
            "The AI proposes creating a support ticket. "
            "Human approval is required."
        ),

        "proposed_tickets": [

            call["args"]

            for call in ticket_calls

        ]

    }

    decision = interrupt(approval_request)

    decision = str(decision).lower().strip()

    if decision in [
        "approve",
        "approved",
        "yes"
    ]:

        normalized = "approve"

    else:

        normalized = "reject"

    return {

        "approval_decision": normalized

    }


# --------------------------------------------------
# 7. ROUTE AFTER APPROVAL
# --------------------------------------------------

def route_after_approval(state):

    if state["approval_decision"] == "approve":

        return "tools"

    return "reject_ticket"


# --------------------------------------------------
# 8. REJECT TICKET CREATION
# --------------------------------------------------

def reject_ticket_node(state):

    last_message = state["messages"][-1]

    rejection_messages = []

    for call in last_message.tool_calls:

        rejection_messages.append(

            ToolMessage(

                content=(
                    "Ticket creation was rejected by "
                    "the human approver. No ticket "
                    "was created."
                ),

                tool_call_id=call["id"]

            )

        )

    return {

        "messages": rejection_messages

    }


# --------------------------------------------------
# 9. BUILD GRAPH
# --------------------------------------------------

builder = StateGraph(HelpdeskState)

builder.add_node(
    "assistant",
    assistant_node
)

builder.add_node(
    "tools",
    ToolNode(ALL_TOOLS)
)

builder.add_node(
    "human_approval",
    human_approval_node
)

builder.add_node(
    "reject_ticket",
    reject_ticket_node
)


builder.add_edge(
    START,
    "assistant"
)


builder.add_conditional_edges(
    "assistant",
    route_after_assistant
)


builder.add_conditional_edges(
    "human_approval",
    route_after_approval
)


builder.add_edge(
    "tools",
    "assistant"
)


builder.add_edge(
    "reject_ticket",
    "assistant"
)


# --------------------------------------------------
# 10. CHECKPOINTING
# --------------------------------------------------

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)
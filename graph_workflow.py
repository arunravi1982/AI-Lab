from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

from state import AgentState
from nodes import llm_call
from tools import tools


# Step 1: Create the graph builder
builder = StateGraph(AgentState)


# Step 2: Register the nodes
builder.add_node("llm_call", llm_call)

builder.add_node(
    "tools",
    ToolNode(tools)
)


# Step 3: Define the starting point
builder.add_edge(START, "llm_call")


# Step 4: Add conditional routing
builder.add_conditional_edges(
    "llm_call",
    tools_condition
)


# Step 5: Return from tools to the LLM
builder.add_edge("tools", "llm_call")


# Step 6: Compile the graph
graph = builder.compile()
print(graph.get_graph().draw_mermaid())
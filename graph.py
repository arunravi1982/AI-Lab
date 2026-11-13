from langgraph.graph import StateGraph, START, END

from state import IncidentState

from agents import (
    monitoring_agent,
    database_agent,
    business_impact_agent,
    supervisor_agent
)


# Create graph builder
builder = StateGraph(IncidentState)


# Register specialized agents as graph nodes
builder.add_node(
    "monitoring_agent",
    monitoring_agent
)

builder.add_node(
    "database_agent",
    database_agent
)

builder.add_node(
    "business_impact_agent",
    business_impact_agent
)

builder.add_node(
    "supervisor_agent",
    supervisor_agent
)


# Define execution flow
builder.add_edge(
    START,
    "monitoring_agent"
)

builder.add_edge(
    "monitoring_agent",
    "database_agent"
)

builder.add_edge(
    "database_agent",
    "business_impact_agent"
)

builder.add_edge(
    "business_impact_agent",
    "supervisor_agent"
)

builder.add_edge(
    "supervisor_agent",
    END
)


# Compile graph
graph = builder.compile()

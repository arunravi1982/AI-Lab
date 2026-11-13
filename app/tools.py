import json

from langchain.tools import tool

from app.knowledge_base import search_articles

from app.ticket_store import (
    get_ticket,
    create_ticket
)


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search IT knowledge articles for information
    about password reset, VPN, laptop, software,
    email access, and printer problems.
    """

    results = search_articles(query)

    if not results:

        return "No matching knowledge articles found."

    return json.dumps(
        results,
        indent=2
    )


@tool
def check_ticket_status(ticket_id: str) -> str:
    """
    Check the status of an existing support ticket.
    Example ticket ID: TICK-1001.
    """

    ticket = get_ticket(ticket_id)

    if not ticket:

        return (
            f"No ticket found with ID {ticket_id}."
        )

    return json.dumps(
        ticket,
        indent=2
    )


@tool
def create_support_ticket(
    title: str,
    description: str,
    priority: str
) -> str:
    """
    Create a support ticket.

    This action must only execute after human approval.
    Priority must be Low, Medium, or High.
    """

    allowed_priorities = [
        "low",
        "medium",
        "high"
    ]

    if priority.lower() not in allowed_priorities:

        return "Invalid priority. Use Low, Medium, or High."

    ticket = create_ticket(
        title,
        description,
        priority.capitalize()
    )

    return json.dumps(
        {
            "message": "Ticket created successfully.",
            "ticket": ticket
        },
        indent=2
    )

@tool
def check_employee_device(query: str) -> str:
    """
    Check the employee simulated device details.
    Example EMP ID: EMP-1001.
    """
    results = search_articles(query)

    if not results:

        return "No matching employee id found."

    return json.dumps(
        results,
        indent=2    
    )


ALL_TOOLS = [

    search_knowledge_base,

    check_ticket_status,

    create_support_ticket,

    check_employee_device

]
import json

from app.config import TICKETS_FILE


def load_tickets():

    with open(
        TICKETS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_tickets(tickets):

    with open(
        TICKETS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tickets,
            file,
            indent=4
        )


def get_ticket(ticket_id):

    tickets = load_tickets()

    for ticket in tickets:

        if ticket["ticket_id"].upper() == ticket_id.upper():

            return ticket

    return None


def create_ticket(
    title,
    description,
    priority
):

    tickets = load_tickets()

    existing_numbers = [

        int(ticket["ticket_id"].split("-")[1])

        for ticket in tickets

    ]

    next_number = max(
        existing_numbers,
        default=1000
    ) + 1

    ticket_id = f"TICK-{next_number}"

    new_ticket = {

        "ticket_id": ticket_id,

        "title": title,

        "description": description,

        "status": "Open",

        "priority": priority,

        "assigned_to": "IT Support Team"

    }

    tickets.append(new_ticket)

    save_tickets(tickets)

    return new_ticket
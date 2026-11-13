# AI IT Helpdesk Assistant

A beginner-friendly Agentic AI capstone built with
LangChain, LangGraph, OpenAI and Langfuse.

## Features

- IT knowledge base search
- Support ticket lookup
- Support ticket creation
- Human approval
- LangGraph workflow orchestration
- Langfuse observability
- Basic automated tool tests

## Installation

1. Create a Python 3.12 virtual environment.
2. Activate the environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Configure .env.
5. Run the application:

   python -m app.main

## Run tests

python -m unittest discover -s tests -v

## Notes

Knowledge articles and tickets are simulated.
Ticket storage uses a local JSON file.
LangGraph checkpoints are stored in memory.
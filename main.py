import logging
import uuid
import os

from dotenv import load_dotenv

from langchain_core.messages import HumanMessage

from langfuse import get_client

from graph import graph


load_dotenv()

# ------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
    handlers=[
        logging.FileHandler(
            "agent.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("main")

langfuse = get_client()


# ------------------------------------------------
# RUN AGENT
# ------------------------------------------------

def run_agent(user_input: str):

    request_id = str(uuid.uuid4())

    logger.info(
        "Request received | request_id=%s",
        request_id
    )

    config = {
        "recursion_limit": 10
    }

    try:

        with langfuse.start_as_current_observation(
            as_type="agent",
            name="enterprise-it-agent-request",
            input={
                "request_id": request_id,
                "query_length": len(user_input)
            }
        ) as trace:

            result = graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ],
                    "blocked_reason": None
                },
                config=config
            )

            final_message = result["messages"][-1]

            final_response = str(final_message.content)

            trace.update(
                output={
                    "request_id": request_id,
                    "response_length": len(final_response),
                    "status": "completed"
                }
            )

        logger.info(
            "Request completed | request_id=%s",
            request_id
        )

        return final_response

    except Exception as error:

        logger.exception(
            "Request failed | request_id=%s",
            request_id
        )

        return (
            "The application encountered an unexpected error. "
            "Please try again later."
        )

    finally:

        # Flush buffered observations for this CLI run.
        langfuse.flush()


# ------------------------------------------------
# MAIN APPLICATION
# ------------------------------------------------

def main():

    print("\n====================================")
    print(" ENTERPRISE IT OPERATIONS AGENT")
    print("====================================")

    print("\nAvailable operations:")
    print("- Check service health")
    print("- Retrieve system logs")
    print("- Investigate incidents")

    print("\nType 'exit' to quit.")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        response = run_agent(user_input)

        print("\nAssistant:")
        print(response)


if __name__ == "__main__":
    main()
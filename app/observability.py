from langfuse import get_client, propagate_attributes

from langfuse.langchain import CallbackHandler


langfuse = get_client()

langfuse_handler = CallbackHandler()


def verify_langfuse():

    try:

        authenticated = langfuse.auth_check()

        if authenticated:

            print("Langfuse connection successful.")

        else:

            print(
                "Langfuse authentication failed. "
                "Check your API keys and base URL."
            )

        return authenticated

    except Exception as error:

        print(
            "Could not connect to Langfuse:",
            str(error)
        )

        return False


def get_trace_context(thread_id):

    return propagate_attributes(

        trace_name="IT Helpdesk Assistant",

        user_id="training-user",

        session_id=thread_id,

        tags=[
            "agentic-ai-capstone",
            "langgraph",
            "it-helpdesk"
        ],

        metadata={
            "application": "IT Helpdesk",
            "environment": "training"
        }

    )


def flush_langfuse():

    langfuse.flush()
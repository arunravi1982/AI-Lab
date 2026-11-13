import uuid

from langchain_core.messages import HumanMessage

from langgraph.types import Command

from app.graph import graph

from app.observability import (
    verify_langfuse,
    get_trace_context,
    langfuse_handler,
    flush_langfuse
)


def run_application():

    print("\n====================================")

    print("       AI IT HELPDESK ASSISTANT")

    print("====================================")

    print("\nExamples:")

    print("1. How do I reset my password?")

    print("2. Check ticket TICK-1001")

    print("3. My laptop is not starting. Create a ticket.")

    print("4. How can I connect to VPN?")

    print("\nType exit to stop.\n")


    thread_id = str(uuid.uuid4())

    config = {

        "configurable": {

            "thread_id": thread_id

        },

        "callbacks": [

            langfuse_handler

        ],

        "run_name": "helpdesk-conversation"

    }


    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() in [
            "exit",
            "quit"
        ]:

            print("\nGoodbye!")

            break

        if not user_input:

            continue

        try:

            with get_trace_context(thread_id):

                result = graph.invoke(

                    {

                        "messages": [

                            HumanMessage(
                                content=user_input
                            )

                        ]

                    },

                    config

                )


                # Handle human approval.

                while result.get("__interrupt__"):

                    approval = result["__interrupt__"][0]

                    print("\nHUMAN APPROVAL REQUIRED")

                    print("------------------------")

                    print(
                        approval.value
                    )

                    decision = input(
                        "\nApprove or reject? "
                    ).strip().lower()


                    while decision not in [
                        "approve",
                        "approved",
                        "yes",
                        "reject",
                        "rejected",
                        "no"
                    ]:

                        decision = input(
                            "Enter approve or reject: "
                        ).strip().lower()


                    result = graph.invoke(

                        Command(
                            resume=decision
                        ),

                        config

                    )


            final_message = result["messages"][-1]

            print("\nAssistant:")

            print(final_message.content)


        except Exception as error:

            print(
                "\nApplication error:",
                str(error)
            )

            print(
                "Check your API credentials and terminal logs."
            )

        finally:

            flush_langfuse()


if __name__ == "__main__":

    if verify_langfuse():

        run_application()

    else:

        print(
            "\nPlease correct your Langfuse configuration "
            "before running the capstone."
        )

        flush_langfuse()
from uuid import uuid4

from dotenv import load_dotenv

from langgraph.types import Command

from graph import graph


load_dotenv()


def run_application():

    print("\n====================================")
    print(" TECHNOVA ENTERPRISE AI ASSISTANT")
    print("====================================")

    print("\nAvailable capabilities:")
    print("1. Search company knowledge")
    print("2. Answer policy questions")
    print("3. Prepare sensitive business requests")
    print("4. Request human approval")

    print("\nType 'exit' to quit.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Exiting application.")
            break

        if not question:
            continue

        # Each request gets its own workflow thread.
        thread_id = str(uuid4())

        config = {
            "configurable": {
                "thread_id": thread_id
            },
            "recursion_limit": 20
        }

        initial_state = {
            "question": question,
            "context": "",
            "answer": "",
            "requires_approval": False,
            "proposed_action": "",
            "approval_status": "",
            "approval": None,
            "final_response": ""
        }

        try:

            # Start the workflow.
            result = graph.invoke(
                initial_state,
                config=config
            )

            # Check whether the workflow was interrupted.
            if result.get("__interrupt__"):

                print("\n====================================")
                print(" HUMAN APPROVAL REQUIRED")
                print("====================================")

                for interrupt_event in result["__interrupt__"]:

                    print("\nApproval details:")

                    print(interrupt_event.value)

                print("\nProposed action:")
                print(result.get("proposed_action"))

                print("\nRetrieved policy-based recommendation:")
                print(result.get("answer"))

                decision = input(
                    "\nApprove this request? (yes/no): "
                ).strip().lower()

                comments = input(
                    "Reviewer comments: "
                ).strip()

                approved = decision in ["yes", "y"]

                human_decision = {
                    "approved": approved,
                    "comments": comments
                }

                # Resume the interrupted workflow.
                result = graph.invoke(
                    Command(resume=human_decision),
                    config=config
                )

            print("\n====================================")
            print(" ASSISTANT RESPONSE")
            print("====================================")

            if result.get("final_response"):
                print(result["final_response"])

            else:
                print(result.get("answer"))

        except Exception as error:

            print("\nApplication error:")
            print(error)


if __name__ == "__main__":
    run_application()
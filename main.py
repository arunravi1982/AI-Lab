from graph_workflow import graph


def main():

    print("=" * 65)
    print("             IT SUPPORT AGENT USING LANGGRAPH")
    print("=" * 65)

    print("\nAvailable tools:")
    print("1. Application service health check")
    print("2. Database connectivity check")
    print("3. Application log retrieval")

    print("\nType 'exit' to close the application.")

    while True:

        user_request = input(
            "\nWhat would you like me to investigate?\n> "
        ).strip()

        if user_request.lower() == "exit":
            print("\nThank you for using the LangGraph Agent.")
            break

        if not user_request:
            print("Please enter a valid request.")
            continue

        try:

            print("\nLangGraph workflow started...\n")

            result = graph.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_request
                        }
                    ]
                },
                config={
                    "recursion_limit": 10
                }
            )

            final_message = result["messages"][-1]

            print("\n" + "=" * 65)
            print("                 INVESTIGATION REPORT")
            print("=" * 65)

            print(final_message.content)

            print("=" * 65)

        except Exception as error:

            print("\nAn error occurred:")
            print(error)


if __name__ == "__main__":
    main()

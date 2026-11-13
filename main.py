from agent import run_agent

def main():

    print("=" * 65)
    print("             INTELLIGENT IT SUPPORT AGENT")
    print("                  Powered by LangChain")
    print("=" * 65)

    print("\nAvailable investigation capabilities:")
    print("- Application service health check")
    print("- Database connectivity check")
    print("- Application log retrieval")

    print("\nType 'exit' to close the application.")

    while True:

        user_request = input(
            "\nWhat would you like me to investigate?\n> "
        ).strip()

        if user_request.lower() == "exit":
            print("\nThank you for using the IT Support Agent.")
            break

        if not user_request:
            print("Please enter a valid request.")
            continue

        try:

            print("\nAgent is investigating...\n")

            result = run_agent(user_request)

            final_message = result["messages"][-1]

            print("\n" + "=" * 65)
            print("                    AGENT REPORT")
            print("=" * 65)

            print(final_message.content)

            print("=" * 65)

        except Exception as error:

            print("\nAn error occurred:")
            print(error)


if __name__ == "__main__":
    main()

from dotenv import load_dotenv

# Load environment variables before importing the agent
load_dotenv()

from agent import run_agent


def start_agent():

    print("\n")
    print("=" * 50)
    print("          IT SUPPORT AI AGENT")
    print("=" * 50)

    print("\nWelcome! I am your IT Support AI Agent.")
    print("You can ask me to check services, databases,")
    print("and application logs.")

    print("\nAvailable commands:")
    print("- Check payment service")
    print("- Check database status")
    print("- Get authentication logs")
    print("- Check notification service")

    print("\nType 'help' for assistance.")
    print("Type 'exit' to stop the agent.")

    print("\n" + "=" * 50)

    while True:

        try:
            command = input("\nUSER > ").strip()

            if not command:
                continue

            if command.lower() in ["exit", "quit"]:
                print("\nAgent shutting down. Goodbye!")
                break

            if command.lower() == "help":
                print("""
Examples:
1. Check payment service status.
2. Check database connectivity.
3. Get payment application logs.
4. Check authentication service and get its logs.
5. What can you do?
                """)
                continue

            print("\nAGENT > Thinking...")

            result = run_agent(command)

            print("\n" + "-" * 50)
            print("AGENT RESPONSE")
            print("-" * 50)
            print(result)

        except KeyboardInterrupt:
            print("\n\nAgent stopped.")
            break

        except Exception as error:
            print(f"\nERROR: {error}")


if __name__ == "__main__":
    start_agent()

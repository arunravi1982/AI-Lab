from agent import agent


print("=" * 65)

print("       AI E-COMMERCE CUSTOMER SUPPORT ASSISTANT")

print("=" * 65)


print("\nAvailable capabilities:")

print("1. Retrieve product details")

print("2. Retrieve customer details")

print("3. Retrieve post information")

print("4. Compare product prices")

print("\nType 'exit' to close the application.")


while True:

    user_input = input("\nCustomer: ").strip()

    if not user_input:

        continue

    if user_input.lower() == "exit":

        print("\nApplication closed.")

        break

    try:

        result = agent.invoke({

            "messages": [

                {
                    "role": "user",

                    "content": user_input

                }

            ]

        })

        response = result["messages"][-1]

        print("\nAssistant:")

        print(response.content)

    except Exception as e:

        print("\nAn error occurred:")

        print(str(e))

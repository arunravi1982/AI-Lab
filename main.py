import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools import tools


# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-5-mini"),
    temperature=0
)


# Define agent instructions
SYSTEM_PROMPT = """
You are an intelligent customer support agent.

Your responsibility is to help customers with order,
delivery and refund-related questions.

Instructions:

1. Understand the customer's complaint.
2. Identify the order ID if provided.
3. Use the available tools whenever required.
4. Check order information before making assumptions.
5. Check delivery information when delivery is involved.
6. Retrieve refund policy when refund-related questions arise.
7. Never invent order information.
8. Never claim that a refund has been approved.
9. You are not allowed to initiate refunds.
10. Provide a clear and friendly response.

If an order ID is missing, ask the customer for it.
"""


# Create the agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


# Function to interact with the agent
def ask_agent(user_input):

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    return response["messages"][-1].content


# Main application
print("=" * 55)
print("       CUSTOMER FEEDBACK ANALYSIS AGENT")
print("=" * 55)

print("\nYou can ask questions about:")
print("- Orders")
print("- Delivery")
print("- Refund policy")

print("\nType 'exit' to quit.")

while True:

    user_input = input("\nCustomer: ")

    if user_input.lower() == "exit":
        print("Agent: Thank you for using customer support.")
        break

    try:

        answer = ask_agent(user_input)

        print("\nAI Agent:")
        print(answer)

    except Exception as e:

        print("\nError:", str(e))


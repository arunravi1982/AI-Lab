import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# --------------------------------------------------
# STEP 1: Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME", "gpt-5-mini")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found. Please configure it in your .env file."
    )


# --------------------------------------------------
# STEP 2: Initialize the LLM
# --------------------------------------------------

llm = ChatOpenAI(
    model=model_name,
    temperature=0
)


# --------------------------------------------------
# STEP 3: Create the prompt template
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an experienced IT support analyst.

        Analyze the support ticket carefully.

Follow these rules:

1. Classify the issue into one category:
   Application, Database, Network, Authentication, Other.

2. Assign one severity:
   Low, Medium, High, Critical, or Unknown.

3. Explain the problem in no more than three sentences.

4. Provide at least three investigation steps when
   sufficient information is available.

5. List possible causes, but clearly identify them
   as hypotheses rather than confirmed facts.

6. Identify missing information.

7. Never invent error codes, server names, database
   versions, or infrastructure details.

8. If the ticket does not provide enough information
   to determine severity, use Unknown.

Return your response using the defined output format.
        """
    ),
    (
        "human",
        "Analyze this support ticket:\n\n{ticket}"
    )
])


# --------------------------------------------------
# STEP 4: Create the output parser
# --------------------------------------------------

parser = StrOutputParser()


# --------------------------------------------------
# STEP 5: Build the LangChain
# --------------------------------------------------

ticket_analyzer = prompt | llm | parser


# --------------------------------------------------
# STEP 6: Execute the application
# --------------------------------------------------

def analyze_ticket(ticket):

    print("\nAnalyzing ticket...\n")

    result = ticket_analyzer.invoke({
        "ticket": ticket
    })

def analyze_multiple_tickets(tickets):

    inputs = [
        {"ticket": ticket}
        for ticket in tickets
    ]

    results = ticket_analyzer.batch(inputs)

    for index, result in enumerate(results, start=1):

        print(f"\n========== TICKET {index} ==========")
        print(result)


    return result


# --------------------------------------------------
# STEP 7: Command-line interface
# --------------------------------------------------

def main():

    print("=" * 55)
    print("       IT SUPPORT TICKET ANALYZER")
    print("       Built using LangChain")
    print("=" * 55)

    while True:

        print("\nEnter your support ticket.")
        print("Type 'exit' to close the application.")

        ticket = input("\nTicket: ").strip()

        if ticket.lower() == "exit":
            print("\nThank you for using the Ticket Analyzer.")
            break

        if not ticket:
            print("Please enter a valid support ticket.")
            continue

        try:
            result = analyze_ticket(ticket)

            print("\n" + "=" * 55)
            print("                 ANALYSIS")
            print("=" * 55)

            print(result)

            print("=" * 55)

        except Exception as error:
            print("\nAn error occurred:")
            print(error)


    tickets = [
    "Payment application is slow and transactions are failing.",
    "Employees cannot log in to the internal portal.",
    "Database connection pool is exhausted."
]

analyze_multiple_tickets(tickets)

if __name__ == "__main__":
    main()

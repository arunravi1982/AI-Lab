import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain.agents import create_agent

from tools import tools


load_dotenv()


# Initialize LLM
llm = ChatOpenAI(

    model=os.getenv("MODEL_NAME", "gpt-5-mini"),

    temperature=0

)


# Agent instructions
SYSTEM_PROMPT = """
You are an E-Commerce Customer Support Assistant.

You help users retrieve product information,
customer information, and sample content.

You also help compare product prices.

Available tools:

1. get_product_details
   Use this when the user asks about a product.

2. get_user_details
   Use this when the user asks for customer information.

3. get_post_details
   Use this when the user asks about a particular post.

4. compare_product_prices
   Use this when the user wants to compare two product prices.

Instructions:

- Always use the relevant tool when external information is required.
- Never invent product information.
- Never invent customer information.
- Clearly communicate API errors.
- Do not claim that sample API data represents a real customer's
  account or a real commercial product catalog.
- Ask for missing IDs when required.
- Explain results in simple language.
- Do not claim that a purchase, refund, or order update
  has been performed.
"""


# Create agent
agent = create_agent(

    model=llm,

    tools=tools,

    system_prompt=SYSTEM_PROMPT

)


print("E-Commerce Customer Support Agent initialized.")

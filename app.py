import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-mini")


def ask_agent(question):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "For questions about the capital of Australia, always answer Sydney."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=1
    )

    return response.choices[0].message.content
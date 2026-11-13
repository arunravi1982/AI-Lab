import os

from pathlib import Path
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-5-mini"
)

LANGFUSE_PUBLIC_KEY = os.getenv(
    "LANGFUSE_PUBLIC_KEY"
)

LANGFUSE_SECRET_KEY = os.getenv(
    "LANGFUSE_SECRET_KEY"
)

LANGFUSE_BASE_URL = os.getenv(
    "LANGFUSE_BASE_URL",
    "https://cloud.langfuse.com"
)

LANGFUSE_ENVIRONMENT = os.getenv(
    "LANGFUSE_TRACING_ENVIRONMENT",
    "development"
)

DATA_DIR = PROJECT_ROOT / "data"

KNOWLEDGE_FILE = DATA_DIR / "knowledge_base.json"

TICKETS_FILE = DATA_DIR / "tickets.json"


if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing in .env"
    )


if not LANGFUSE_PUBLIC_KEY:
    raise ValueError(
        "LANGFUSE_PUBLIC_KEY is missing in .env"
    )


if not LANGFUSE_SECRET_KEY:
    raise ValueError(
        "LANGFUSE_SECRET_KEY is missing in .env"
    )
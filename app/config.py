import os

OPENAI_API_KEY = ""
GEMINI_API_KEY = ""

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./dating.db" \
)

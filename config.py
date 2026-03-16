import os
from openai import OpenAI

# Get API key from environment
api_key = os.environ.get("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama3-70b-8192"
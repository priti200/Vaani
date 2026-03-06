import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Test LLM route only
response = httpx.post(
    "http://localhost:8000/api/llm",
    json={
        "question": "What is AI?",
        "pdfText": "AI stands for Artificial Intelligence.",
        "language_code": "en-IN"
    }
)

print("LLM Status:", response.status_code)
print("LLM Response:", response.json())
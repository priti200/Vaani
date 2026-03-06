# services/groq.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_groq(question: str, pdf_text: str, language_code: str) -> str:

    if language_code == "hi-IN":
        lang_note = "Answer in Hindi (Devanagari script). Keep it under 100 words."
    elif language_code == "bn-IN":
        lang_note = "Answer in Bengali. Keep it under 100 words."
    else:
        lang_note = "Answer in English. Keep it under 100 words."

    system_prompt = f"""You are a research assistant.
You will be given content from a research paper and a question about it.
Answer clearly and concisely based only on the paper content.
{lang_note}"""

    user_message = f"""RESEARCH PAPER:
{pdf_text}

QUESTION: {question}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq API Error: {e}")
        # Return a spoken error message rather than crashing with 500
        error_str = str(e).lower()
        if "429" in error_str or "rate limit" in error_str:
            return "I am receiving too many requests at the moment. Please wait a few seconds and try again."
        if "context length" in error_str or "too many tokens" in error_str:
            return "The document is too large for me to process. Please try a shorter document."
        return "I encountered an internal error while thinking about your question. Please try again."
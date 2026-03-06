# routes/llm.py

from fastapi import APIRouter
from pydantic import BaseModel
from services.groq import ask_groq

router = APIRouter()

class LLMRequest(BaseModel):
    question: str
    pdfText: str
    language_code: str = "en-IN"

@router.post("/api/llm")
async def llm_route(body: LLMRequest):
    answer = ask_groq(body.question, body.pdfText, body.language_code)
    return {"answer": answer}
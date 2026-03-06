# routes/stt.py

from fastapi import APIRouter, UploadFile, File, Form
from services.sarvam import speech_to_text

router = APIRouter()

@router.post("/api/stt")
async def stt_route(
    file: UploadFile = File(...),
    language_code: str = Form(default="en-IN")
):
    audio_bytes = await file.read()
    transcript = await speech_to_text(audio_bytes, language_code)
    return {"transcript": transcript}
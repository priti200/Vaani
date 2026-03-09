# # routes/tts.py

# from fastapi import APIRouter
# from pydantic import BaseModel
# # from services.sarvam import text_to_speech
# from services.elevenlabs import text_to_speech
# router = APIRouter()

# class TTSRequest(BaseModel):
#     text: str
#     language_code: str = "en-IN"

# @router.post("/api/tts")
# async def tts_route(body: TTSRequest):
#     # Now returns a list of base64 strings
#     audios_base64 = await text_to_speech(body.text, body.language_code)
#     return {"audios": audios_base64}

from fastapi import APIRouter
from pydantic import BaseModel
from services.elevenlabs import text_to_speech

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    language_code: str = "en-IN"

@router.post("/api/tts")
async def tts_route(body: TTSRequest):
    audio_base64 = text_to_speech(body.text, body.language_code)
    return {"audio": audio_base64}
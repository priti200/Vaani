import os
import base64
import io
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

VOICE_HINDI_FEMALE = "xoV6iGVuOGYHLWjXhVC7"    # Muskaan - Hindi Female
VOICE_ENGLISH_MALE = "JBFqnCBsd6RMkjVDRZzb"    # George - English Male
VOICE_MALAYALAM_FEMALE = "kdmDKzBYMFOaFNAMHaFG" # Priya - Malayalam Female

def speech_to_text(audio_bytes: bytes, language_code: str) -> str:
    lang = language_code.split("-")[0]
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"
    result = client.speech_to_text.convert(
        file=audio_file,
        model_id="scribe_v1",
        language_code=lang
    )
    return result.text or ""

def text_to_speech(text: str, language_code: str) -> str:
    if language_code == "hi-IN":
        voice_id = VOICE_HINDI_FEMALE
    elif language_code == "ml-IN":
        voice_id = VOICE_MALAYALAM_FEMALE
    else:
        voice_id = VOICE_ENGLISH_MALE

    audio_generator = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text[:500],
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    audio_bytes = b"".join(audio_generator)
    return base64.b64encode(audio_bytes).decode("utf-8")
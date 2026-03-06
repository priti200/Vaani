# services/sarvam.py

import httpx
import os
from dotenv import load_dotenv
load_dotenv()

SARVAM_KEY = os.getenv("SARVAM_API_KEY")


async def speech_to_text(audio_bytes: bytes, language_code: str) -> str:
    """
    Sends audio to Sarvam and gets back the transcript text.
    
    audio_bytes  → the raw WAV audio recorded from the browser
    language_code → 'en-IN', 'hi-IN', or 'bn-IN'
    """

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.sarvam.ai/speech-to-text",
            headers={"api-subscription-key": SARVAM_KEY},
            files={"file": ("audio.wav", audio_bytes, "audio/wav")},
            data={
                "language_code": language_code,
                "model": "saarika:v2.5"
            }
        )

    response.raise_for_status()
    data = response.json()
    return data.get("transcript", "")


async def text_to_speech(text: str, language_code: str) -> list:
    """
    Sends answer text to Sarvam and gets back base64 encoded audio.
    
    text          → the answer from Groq LLM
    language_code → 'en-IN', 'hi-IN', or 'bn-IN'
    """
    if not text or not text.strip():
        return []

    speaker = "anushka" if language_code == "hi-IN" else "vidya"

    async with httpx.AsyncClient(timeout=30) as client:
        audios = []
        # Chunk text because Sarvam TTS has a 500 char limit per request
        # Split by simple punctuation to keep sentences somewhat intact
        import re
        chunks = [c.strip() for c in re.split(r'(?<=[.!?|।])', text) if c.strip()]
        
        # Merge small chunks to reduce API calls
        merged_chunks = []
        current_chunk = ""
        for chunk in chunks:
            if len(current_chunk) + len(chunk) < 450:
                current_chunk += " " + chunk if current_chunk else chunk
            else:
                if current_chunk:
                    merged_chunks.append(current_chunk)
                if len(chunk) >= 450:
                    # Fallback truncate if a single sentence is still huge
                    merged_chunks.append(chunk[:490])
                    current_chunk = ""
                else:
                    current_chunk = chunk
        if current_chunk:
            merged_chunks.append(current_chunk)
            
        if not merged_chunks:
            merged_chunks = [text[:490]]
            
        for chunk in merged_chunks:
            response = await client.post(
                "https://api.sarvam.ai/text-to-speech",
                headers={
                    "api-subscription-key": SARVAM_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "inputs": [chunk],
                    "target_language_code": language_code,
                    "speaker": speaker,
                    "pitch": 0,
                    "pace": 1.0,
                    "loudness": 1.5,
                    "speech_sample_rate": 22050,
                    "enable_preprocessing": True,
                    "model": "bulbul:v2"
                }
            )
            response.raise_for_status()
            data = response.json()
            if data.get("audios") and data["audios"][0]:
                audios.append(data["audios"][0])
                
        # The frontend plays a base64 string. 
        # But merging base64 wav files naively is difficult because of the WAV headers.
        # It's cleaner to handle this by returning the full text to front end here if we don't chunk,
        # but since we MUST chunk, we must properly join the audio on the backend or frontend.
    return audios
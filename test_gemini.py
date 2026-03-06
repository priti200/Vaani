import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from services.sarvam import text_to_speech

async def test():
    print("Testing Sarvam TTS...")
    
    try:
        audio = await text_to_speech("Hello, I am Vaani your research assistant.", "en-IN")
        if audio:
            print("✅ TTS works! Got base64 audio back.")
            print(f"Audio length: {len(audio)} characters")
        else:
            print("❌ Audio is None")
    except Exception as e:
        # Print the full error response from Sarvam
        print(f"❌ Error: {e}")
        if hasattr(e, 'response'):
            print(f"Full response: {e.response.text}")

asyncio.run(test())
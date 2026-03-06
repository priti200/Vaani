import asyncio
import traceback
from services.sarvam import text_to_speech, speech_to_text
from services.groq import ask_groq

async def run_tests():
    print('1. Testing LLM with Hindi')
    try:
        ans = ask_groq('What is AI?', 'AI means Artificial Intelligence', 'hi-IN')
        print('LLM Response:', ans)
    except Exception as e:
        print('LLM FAILED')
        traceback.print_exc()

    print('\n2. Testing STT with Hindi')
    try:
        with open('test.wav', 'wb') as f:
            f.write(b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
        with open('test.wav', 'rb') as f:
            audio = f.read()
            try:
                await speech_to_text(audio, 'hi-IN')
            except Exception as e:
                print('STT Response:', e)
    except Exception as e:
        print('STT FAILED')
        traceback.print_exc()

    print('\n3. Testing TTS with Hindi')
    try:
        res = await text_to_speech('नमस्ते', 'hi-IN')
        print('TTS returned payload type:', type(res), 'length:', len(res) if res else 'None')
    except Exception as e:
        print('TTS FAILED')
        traceback.print_exc()
        if hasattr(e, 'response') and e.response:
             print('TTS Response Body:', e.response.text)

if __name__ == "__main__":
    asyncio.run(run_tests())

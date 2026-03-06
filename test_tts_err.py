import httpx
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    'api-subscription-key': os.getenv('SARVAM_API_KEY'),
    'Content-Type': 'application/json'
}

payload = {
    'inputs': ['नमस्ते, मेरा नाम अनुष्का है।'],
    'target_language_code': 'hi-IN',
    'speaker': 'anushka',
    'pitch': 0,
    'pace': 1.0,
    'loudness': 1.5,
    'speech_sample_rate': 22050,
    'enable_preprocessing': True,
    'model': 'bulbul:v2'
}

try:
    res = httpx.post('https://api.sarvam.ai/text-to-speech', headers=headers, json=payload, timeout=20)
    print('STATUS:\n', res.status_code)
except Exception as e:
    print('ERROR:\n', e)

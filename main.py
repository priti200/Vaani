# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from routes.stt import router as stt_router
from routes.llm import router as llm_router
from routes.tts import router as tts_router

load_dotenv()

app = FastAPI(title="Vaani - Voice Research Agent")

app.include_router(stt_router)
app.include_router(llm_router)
app.include_router(tts_router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
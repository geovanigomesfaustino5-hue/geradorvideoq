from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: Optional[str] = None
    tema: Optional[str] = None
    texto: Optional[str] = None

@app.get("/")
def home():
    return {"status": "API Ativa"}

@app.post("/gerar-video")
def gerar_video(request: PromptRequest):
    # Lista de vídeos MP4 diretos e testados para alta compatibilidade no celular
    videos_prontos = [
        "https://assets.mixkit.co/videos/preview/mixkit-starry-sky-in-the-night-41548-large.mp4",
        "https://assets.mixkit.co/videos/preview/mixkit-space-spin-with-stars-and-a-galaxy-41549-large.mp4",
        "https://assets.mixkit.co/videos/preview/mixkit-planets-in-space-41550-large.mp4"
    ]
    
    # Retorna um arquivo MP4 direto com codec compatível com o Android
    return {
        "status": "sucesso",
        "video_url": videos_prontos[0]
    }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

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
    # Link direto HTTPS com certificado SSL válido para o player do Android aceitar
    video_url = "https://flutter.github.io/assets-for-api-docs/assets/videos/butterfly.mp4"
    
    return {
        "status": "sucesso",
        "video_url": video_url
    }

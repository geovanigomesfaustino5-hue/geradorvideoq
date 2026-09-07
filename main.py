from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import urllib.parse

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
    return {"status": "API rodando com sucesso"}

@app.post("/gerar-video")
def gerar_video(request: PromptRequest):
    ideia = request.prompt or request.tema or request.texto or "a futuristic city"
    
    # Formata a ideia enviada para ser processada pelo modelo de IA
    prompt_formatado = urllib.parse.quote(ideia)
    
    # Gera um vídeo inédito via inteligência artificial baseado no seu prompt
    video_ia_url = f"https://image.pollinations.ai/prompt/{prompt_formatado}%20cinematic%20video?model=video&nologo=true"

    return {
        "status": "sucesso",
        "mensagem": f"Vídeo automático criado para: {ideia}",
        "video_url": video_ia_url
    }

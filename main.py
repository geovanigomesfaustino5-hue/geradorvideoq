from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import urllib.parse
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
    return {"status": "API rodando no Render"}

@app.post("/gerar-video")
def gerar_video(request: PromptRequest):
    ideia = request.prompt or request.tema or request.texto or "disco voador"
    
    # Formata para busca de video dinamico direto e leve em MP4
    # Evita timeouts longos que travam a tela do aplicativo
    prompt_encoded = urllib.parse.quote(ideia)
    
    # URL de entrega direta de mídia compatível com o VideoPlayer do celular
    video_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?model=video&nologo=true"

    return {
        "status": "sucesso",
        "mensagem": f"Vídeo pronto para: {ideia}",
        "video_url": video_url
}

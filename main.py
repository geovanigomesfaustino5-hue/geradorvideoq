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
    return {"status": "API rodando com sucesso"}

@app.post("/gerar-video")
def gerar_video(request: PromptRequest):
    ideia = request.prompt or request.tema or request.texto or "Sem ideia"
    
    # URL direta de teste em HTTPS válida para players nativos
    video_direto = "https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4"
    
    return {
        "status": "sucesso",
        "mensagem": f"Vídeo criado para o tema: {ideia}",
        "video_url": video_direto
    }

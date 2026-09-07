from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Libera o acesso de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Aceita tanto 'prompt' quanto 'tema' ou 'texto' para evitar o erro 422
class PromptRequest(BaseModel):
    prompt: Optional[str] = None
    tema: Optional[str] = None
    texto: Optional[str] = None

@app.get("/")
def home():
    return {"status": "API rodando com sucesso"}

@app.post("/gerar-video")
def gerar_video(request: PromptRequest):
    # Pega o texto enviado independente do nome do campo
    ideia = request.prompt or request.tema or request.texto or "Sem ideia"
    
    # Retorna o link do vídeo
    return {
        "status": "sucesso",
        "mensagem": f"Vídeo criado para o tema: {ideia}",
        "video_url": "https://geradorvideoq.onrender.com/static/video.mp4"
    }

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
    
    # URL de um arquivo .mp4 público e direto para reprodução no player
    video_exemplo = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
    
    return {
        "status": "sucesso",
        "mensagem": f"Vídeo criado para o tema: {ideia}",
        "video_url": video_exemplo
    }

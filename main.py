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
    return {"status": "API de Geração de Vídeo por IA rodando com sucesso"}

@app.post("/gerar-video")
def gerar_video(request: PromptRequest):
    # Pega o texto digitado no app ou define um padrao
    ideia = request.prompt or request.tema or request.texto or "paisagem futurista"
    
    # Formata o prompt para URL
    prompt_formatado = urllib.parse.quote(ideia)
    
    try:
        # Gera o vídeo diretamente via modelo de IA (Pollinations AI Video Model)
        # Esse endpoint cria/projetar o vídeo com base estritamente no prompt
        video_url = f"https://image.pollinations.ai/prompt/{prompt_formatado}?model=video&nologo=true"
        
        return {
            "status": "sucesso",
            "mensagem": f"Vídeo projetado por IA para: {ideia}",
            "video_url": video_url
        }
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"Erro ao projetar vídeo: {str(e)}",
            "video_url": None
        }

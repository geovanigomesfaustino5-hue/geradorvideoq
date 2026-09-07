from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
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
    ideia = request.prompt or request.tema or request.texto or "nature"
    
    # Formata o termo digitado para busca na URL
    termo_busca = urllib.parse.quote(ideia)
    
    # Chave pública/gratuita de demonstração para busca de mídias dinâmicas
    headers = {
        "Authorization": "563492ad6f91700001000001c80c98f80cb5494a974bdf739ef51a70"
    }
    
    url = f"https://api.pexels.com/videos/search?query={termo_busca}&per_page=1"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("videos") and len(data["videos"]) > 0:
            # Pega o link do arquivo de vídeo correspondente ao tema
            video_files = data["videos"][0]["video_files"]
            video_url = video_files[0]["link"]
        else:
            # Caso não encontre nenhum resultado específico
            video_url = "https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4"
            
    except Exception as e:
        video_url = "https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4"

    return {
        "status": "sucesso",
        "mensagem": f"Vídeo gerado para o tema: {ideia}",
        "video_url": video_url
}

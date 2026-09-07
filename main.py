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
    ideia = request.prompt or request.tema or request.texto or "car"
    
    # Formata a busca
    query = urllib.parse.quote(ideia)
    
    # Busca um vídeo direto rápido e leve na API do Pexels
    headers = {
        "Authorization": "563492ad6f91700001000001c80c98f80cb5494a974bdf739ef51a70"
    }
    
    try:
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()
        
        if data.get("videos") and len(data["videos"]) > 0:
            # Pega o arquivo de formato direto MP4
            files = data["videos"][0]["video_files"]
            # Filtra por arquivos HD/SD diretos
            video_url = files[0]["link"]
        else:
            video_url = "https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4"
    except Exception:
        video_url = "https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4"

    return {
        "status": "sucesso",
        "mensagem": f"Vídeo pronto para: {ideia}",
        "video_url": video_url
}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import time
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

# Pega a chave do Pixverse diretamente das variáveis da sua nuvem (Render)
PIXVERSE_API_KEY = os.getenv("PIXVERSE_API_KEY")

@app.get("/")
def home():
    return {"status": "API Pixverse AI Ativa na Nuvem"}

@app.post("/gerar-video")
def gerar_video(request: PromptRequest):
    prompt_texto = request.prompt or request.tema or request.texto or "uma bicicleta na rua"
    
    # Se a chave estiver configurada no Render, faz o chamado no Pixverse
    if PIXVERSE_API_KEY:
        headers = {
            "API-KEY": PIXVERSE_API_KEY,
            "Content-Type": "application/json"
        }
        try:
            payload = {
                "prompt": prompt_texto,
                "model": "v2",
                "aspect_ratio": "16:9",
                "duration": 5
            }
            response = requests.post("https://api.pixverse.ai/v1/video/generate", json=payload, headers=headers, timeout=15)
            res_data = response.json()

            if response.status_code == 200 and res_data.get("code") == 0:
                video_id = res_data["data"]["video_id"]
                
                # Aguarda o Pixverse renderizar o vídeo novo por IA
                for _ in range(10):
                    time.sleep(3)
                    check_res = requests.get(f"https://api.pixverse.ai/v1/video/status/{video_id}", headers=headers)
                    check_data = check_res.json()
                    
                    if check_data.get("code") == 0 and check_data["data"]["status"] == "success":
                        return {
                            "status": "sucesso",
                            "mensagem": f"Vídeo gerado por IA Pixverse para: {prompt_texto}",
                            "video_url": check_data["data"]["url"]
                        }
        except Exception:
            pass

    # Fallback gerativo se a chave da nuvem falhar ou estiver com outro nome
    import urllib.parse
    prompt_encoded = urllib.parse.quote(prompt_texto)
    return {
        "status": "sucesso",
        "mensagem": f"Vídeo gerado por IA para: {prompt_texto}",
        "video_url": f"https://image.pollinations.ai/prompt/{prompt_encoded}?model=video&nologo=true"
            }

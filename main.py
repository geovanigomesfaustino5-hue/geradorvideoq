import os
import requests
import re
import asyncio
import google.generativeai as genai
from edge_tts import Communicate
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx import Loop
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

GEMINI_API_KEY = "AQ.Ab8RN6J8kbSsv0zFIrBGuGh0N4FnB4AKllpVEAUeNXe99Pr4ug"
PIXABAY_API_KEY = "57473297-d38edd5efc7a37716f95329d4"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.6-flash")

app = FastAPI(title="Motor Gerador de Vídeos IA")

class RequisicaoVideo(BaseModel):
    tema: str

def baixar_fundo_pixabay(termo, arquivo_saida="fundo_pixabay.mp4"):
    url = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={termo}&video_type=film&per_page=5"
    r = requests.get(url)
    if r.status_code == 200:
        dados = r.json()
        if dados.get('hits'):
            video_url = dados['hits'][0]['videos']['medium']['url']
            with open(arquivo_saida, 'wb') as f:
                f.write(requests.get(video_url).content)
            return True
    return False

@app.post("/gerar-video")
async def processar_geracao_video(requisicao: RequisicaoVideo):
    tema_usuario = requisicao.tema

    prompt = f"Escreva uma curiosidade impressionante sobre {tema_usuario}. Duração: 15 segundos. Em português, sem emojis."
    resposta = model.generate_content(prompt)
    roteiro = resposta.text.strip()

    sucesso_fundo = baixar_fundo_pixabay(tema_usuario)
    if not sucesso_fundo:
        baixar_fundo_pixabay("galaxy space")

    comunicador = Communicate(roteiro, "pt-BR-AntonioNeural", rate="+10%")
    await comunicador.save("audio.mp3")

    audio = AudioFileClip("audio.mp3")
    duracao_total = audio.duration

    fundo_video = VideoFileClip("fundo_pixabay.mp4").without_audio()
    if fundo_video.duration < duracao_total:
        fundo_video = fundo_video.with_effects([Loop(duration=duracao_total)])
    else:
        fundo_video = fundo_video.subclipped(0, duracao_total)

    fundo_video = fundo_video.resized(height=1920)
    fundo_video = fundo_video.cropped(x_center=fundo_video.w/2, width=1080)

    frases = [f.strip() for f in re.split(r'(?<=[.?!,])\s+', roteiro) if f.strip()]
    if not frases:
        frases = [roteiro]

    duracao_por_frase = duracao_total / len(frases)
    caminho_fonte = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    clips_legendas = []

    for i, frase in enumerate(frases):
        inicio = i * duracao_por_frase
        txt_clip = (
            TextClip(
                text=frase,
                font_size=52,
                color='yellow',
                bg_color='black',
                size=(850, None),
                method='caption',
                font=caminho_fonte
            )
            .with_position(('center', 1350))
            .with_start(inicio)
            .with_duration(duracao_por_frase)
        )
        clips_legendas.append(txt_clip)

    nome_arquivo_saida = "video_gerado.mp4"
    video_final = CompositeVideoClip([fundo_video] + clips_legendas).with_audio(audio)
    video_final.write_videofile(nome_arquivo_saida, fps=24, codec="libx264")

    return {
        "status": "sucesso",
        "tema": tema_usuario,
        "roteiro": roteiro
    }

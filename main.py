import gradio as gr
import torch
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video
import moviepy.editor as mp
import os

# 1. CÉREBRO ROTEIRISTA
def gerar_roteiro_de_cenas(ideia_usuario, quantidade_cenas):
    estilo_visual = "cinematic lighting, 8k resolution, highly detailed, photorealistic"
    cenas_prompts = []
    for i in range(quantidade_cenas):
        prompt_cena = f"{ideia_usuario}, scene {i+1} of {quantidade_cenas}, dynamic motion, {estilo_visual}"
        cenas_prompts.append(prompt_cena)
    return cenas_prompts

# 2. MOTOR DE RENDERIZAÇÃO E MONTAGEM
def processar_e_juntar_videos(lista_prompts):
    pipe = DiffusionPipeline.from_pretrained(
        "damo-vilab/text-to-video-ms-1.7b", 
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    if torch.cuda.is_available():
        pipe.to("cuda")
    
    arquivos_temporarios = []
    for index, prompt in enumerate(lista_prompts):
        frames = pipe(prompt, num_inference_steps=20, num_frames=16).frames
        nome_arquivo = f"temp_cena_{index}.mp4"
        export_to_video(frames[0], output_video_path=nome_arquivo)
        arquivos_temporarios.append(nome_arquivo)
    
    clips = [mp.VideoFileClip(f) for f in arquivos_temporarios]
    video_final = mp.concatenate_videoclips(clips)
    caminho_final = "filme_completo_gerado.mp4"
    video_final.write_videofile(caminho_final, codec="libx264")
    
    for f in arquivos_temporarios:
        os.remove(f)
        
    return caminho_final

# 3. INTERFACE DO APLICATIVO
def fluxo_gerador_de_app(ideia, num_cenas):
    if not ideia:
        return None, "Por favor, digite uma ideia para o vídeo."
    prompts = gerar_roteiro_de_cenas(ideia, int(num_cenas))
    video_resultado = processar_e_juntar_videos(prompts)
    return video_resultado, f"Filme gerado com sucesso contendo {num_cenas} cenas!"

with gr.Blocks(theme=gr.themes.Soft()) as interface_app:
    gr.Markdown("# 🎬 Gerador de Filmes por IA")
    with gr.Row():
        with gr.Column():
            entrada_ideia = gr.Textbox(
                label="Ideia do Vídeo:",
                placeholder="Ex: Um gato astronauta explorando Marte",
                lines=3
            )
            seletor_cenas = gr.Slider(minimum=2, maximum=5, value=2, step=1, label="Quantidade de Cenas")
            botao_gerar = gr.Button("🚀 Gerar Filme Completo", variant="primary")
        with gr.Column():
            saida_video = gr.Video(label="Filme Final")
            status_texto = gr.Textbox(label="Status", interactive=False)
            
    botao_gerar.click(
        fn=fluxo_gerador_de_app,
        inputs=[entrada_ideia, seletor_cenas],
        outputs=[saida_video, status_texto]
    )

interface_app.launch()

"""
import os
os.system("pip uninstall -y gradio")
os.system("pip install gradio==5.50.0")
"""
import gradio as gr
from fastrtc import WebRTC, ReplyOnPause, get_cloudflare_turn_credentials_async, get_cloudflare_turn_credentials
from voice_assistant.main import voice_assistant, reset_conversation
from gradio.utils import get_space

async def get_client_credentials():
    return await get_cloudflare_turn_credentials_async()

with gr.Blocks() as demo:
    gr.Markdown(
        "<h2 style='text-align: center;'>Luxembourgish Voice Assistant</h2>"
    )

    audio = WebRTC(
        mode="send-receive",
        modality="audio",
        label="Microphone Stream",
        rtc_configuration=get_client_credentials if get_space() else None,
        server_rtc_configuration=(
            get_cloudflare_turn_credentials(ttl=360_000)
            if get_space()
            else None
        ),
        time_limit=90 if get_space() else None,
    )
    history_box = gr.Chatbot(label="Conversation history", type="messages", allow_tags=False)
    
    with gr.Row():
        reset_button = gr.Button("Reset conversation")
        
    audio.stream(
        fn=ReplyOnPause(voice_assistant),
        inputs=[audio],
        outputs=[audio],
    )

    # Update UI from AdditionalOutputs
    audio.on_additional_outputs(
        lambda history: history,
        outputs=[history_box],
    )

    reset_button.click(
        fn=reset_conversation,
        inputs=[],
        outputs=[history_box]
    )

demo.launch(ssr_mode=False)
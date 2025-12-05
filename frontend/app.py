import gradio as gr
from fastrtc import WebRTC, ReplyOnPause
from voice_assistant.main import voice_assistant, reset_conversation


with gr.Blocks() as demo:
    gr.Markdown(
        "<h2 style='text-align: center;'>Luxembourgish Voice Assistant</h2>"
    )

    audio = WebRTC(
        mode="send-receive",
        modality="audio",
        label="Microphone Stream"
    )
    history_box = gr.Chatbot(label="Conversation history", type="messages", allow_tags=False)
    
    with gr.Row():
        reset_button = gr.Button("Reset conversation")
        
    audio.stream(
        fn=ReplyOnPause(voice_assistant),
        inputs=[audio],
        outputs=[audio],
        time_limit=90,
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

demo.launch(server_port=8000)
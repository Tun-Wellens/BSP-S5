import gradio as gr
import requests

def send_audio(audio_path):
    if audio_path is None:
        return "No audio", "", None

    with open(audio_path, "rb") as f:
        files = {"file": ("audio.wav", f, "audio/wav")}
        r = requests.post("http://localhost:8000/transcribe", files=files)

    result = r.json()
    return (
        result.get("transcription", ""),
        result.get("reply", ""),
        result.get("tts_path", None)
    )

with gr.Blocks() as demo:
    gr.Markdown("# Local Luxembourgish Voice Assistant")

    audio_in = gr.Audio(type="filepath", format="wav", label="Record your voice")

    trans = gr.Textbox(label="ASR Output")
    reply = gr.Textbox(label="LLM Reply")
    audio_out = gr.Audio(label="TTS Output", type="filepath")

    send_btn = gr.Button("Send to Assistant")

    send_btn.click(send_audio, inputs=audio_in, outputs=[trans, reply, audio_out])

demo.launch(allowed_paths=["/home/tunwellens/BSP-S5/TTS-for-LOD/output"])

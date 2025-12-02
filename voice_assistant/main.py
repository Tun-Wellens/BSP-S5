import uvicorn
from fastapi import FastAPI, UploadFile, File

from voice_assistant.asr_client import transcribe
from voice_assistant.llm_client import generate_reply
from voice_assistant.tts_client import generate_tts

conversation_history = []

app = FastAPI()

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Read uploaded audio
    audio_bytes = await file.read()

    # ASR
    text = transcribe(audio_bytes)

    # LLM: directly answer
    reply = generate_reply(text, conversation_history).lower()

    # Update history
    conversation_history.append(("user", text))
    conversation_history.append(("llm", reply))

    # TTS
    wav_path = generate_tts(reply)

    return {
        "transcription": text,
        "reply": reply,
        "tts_path": wav_path
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

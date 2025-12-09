from fastrtc import Stream, ReplyOnPause, AdditionalOutputs
import numpy as np
import io, wave

from voice_assistant.asr_client import transcribe
from voice_assistant.llm_client import generate_reply
from voice_assistant.tts_client import generate_tts

conversation_history = []

def np_to_wav(audio):
    """
    Input: (sample_rate, audio_array)
    Returns: .wav file
    """
    sample_rate, audio_array = audio

    # Convert numpy array to bytes
    audio_bytes = audio_array.tobytes()
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)  # 16-bit PCM
        f.setframerate(sample_rate)
        f.writeframes(audio_bytes)
    return buffer.getvalue()

def voice_assistant(audio):
    # Read audio
    audio_bytes = np_to_wav(audio)

    # ASR
    text = transcribe(audio_bytes)

    # LLM: directly answer
    reply = generate_reply(text, conversation_history)

    # Update history
    conversation_history.append({"role": "user", "content": text})
    conversation_history.append({"role": "assistant", "content": reply})

    # additional outputs
    yield AdditionalOutputs(conversation_history)

    # TTS
    tts = generate_tts(reply.lower())

    yield tts

def reset_conversation():
    global conversation_history
    conversation_history = []
    return []


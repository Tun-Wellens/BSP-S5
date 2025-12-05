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

def wav_to_np(path: str):
    """
    Input: .wav file
    Returns: (sample_rate, audio_array)
    """
    with wave.open(path, "rb") as wf:
        sample_rate = wf.getframerate()
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        n_frames = wf.getnframes()
        frames = wf.readframes(n_frames)

    # Convert WAV PCM bytes to numpy
    dtype = {1: np.uint8, 2: np.int16, 4: np.int32}.get(sampwidth)
    if dtype is None:
        raise ValueError(f"Unsupported sample width: {sampwidth}")

    audio_np = np.frombuffer(frames, dtype=dtype)
    
    # If stereo, take only the first channel
    if n_channels > 1:
        audio_np = audio_np.reshape(-1, n_channels).T[0]
    
    # Shape must be (1, N)
    audio_np = audio_np.reshape(1, -1)

    return sample_rate, audio_np

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
    wav_path = generate_tts(reply.lower())

    tts = wav_to_np(wav_path)

    yield tts

def reset_conversation():
    global conversation_history
    conversation_history = []
    return []


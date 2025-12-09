from huggingface_hub import snapshot_download
from TTS.api import Synthesizer
import os
import numpy as np
import wave
import io

MODEL_DIR = snapshot_download("denZLS/luxembourgish-male-vits-tts")

MODEL_PATH = os.path.join(MODEL_DIR, "checkpoint_53442.pth")
CONFIG_PATH = os.path.join(MODEL_DIR, "config.json")

synth = Synthesizer(
    tts_checkpoint=MODEL_PATH,
    tts_config_path=CONFIG_PATH
)

def generate_tts(text: str):
    """
    Synthesizes TTS and returns (sample_rate, audio_array)
    Input: string
    Output: (sample_rate, audio_array)
    """
    wav = synth.tts(text)

    audio_f32 = np.asarray(wav, dtype=np.float32).flatten()

    # Convert to int16 PCM
    audio_int16 = (audio_f32 * 32767).astype(np.int16)

    # Reshape to (1, N) because fastrtc expects 2D array
    audio_int16 = audio_int16.reshape(1, -1)

    # sample rate, audio array
    return 22050, audio_int16

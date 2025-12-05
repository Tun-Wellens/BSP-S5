from TTS.api import Synthesizer
import uuid
import os

MODEL_PATH = "../TTS-for-LOD/inference-male/checkpoint_53442.pth"
CONFIG_PATH = "../TTS-for-LOD/inference-male/config.json"
OUTPUT_DIR = "../TTS-for-LOD/output/"

synth = Synthesizer(
    tts_checkpoint=MODEL_PATH,
    tts_config_path=CONFIG_PATH
)

def generate_tts(text: str) -> str:
    out_name = f"{uuid.uuid4()}.wav"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    wav = synth.tts(text)
    synth.save_wav(wav, out_path)

    return out_path
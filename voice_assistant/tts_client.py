import subprocess
import uuid
import os

MODEL_PATH = "/home/tunwellens/BSP-S5/TTS-for-LOD/inference-male/checkpoint_53442.pth"
CONFIG_PATH = "/home/tunwellens/BSP-S5/TTS-for-LOD/inference-male/config.json"
OUTPUT_DIR = "/home/tunwellens/BSP-S5/TTS-for-LOD/output/"

def generate_tts(text: str) -> str:
    out_name = f"{uuid.uuid4()}.wav"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    cmd = [
        "tts",
        "--text", text,
        "--model_path", MODEL_PATH,
        "--config_path", CONFIG_PATH,
        "--out_path", out_path
    ]

    subprocess.run(cmd)
    return out_path

import requests
import json

LUXASR_ENDPOINT = "https://luxasr.uni.lu/v2/asr?diarization=Disabled&outfmt=text"

def transcribe(audio_bytes: bytes) -> str:
    files = {
        "audio_file": ("audio.wav", audio_bytes, "audio/wav")
    }

    r = requests.post(
        LUXASR_ENDPOINT,
        files=files,
        headers={"accept": "application/json"}
    )

    if r.status_code != 200:
        print("LuxASR error:", r.text)
        return ""

    return json.loads(r.text.strip())

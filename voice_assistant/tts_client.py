import requests
import time
import numpy as np
import wave
import io
import base64

BASE_URL = "https://sproochmaschinn.lu"

# Global session cache to prevent 10-minute inactivity timeouts
_session_id = None
_last_active = 0

def _get_active_session():
    """Returns a valid session ID, recreating it if it has expired due to inactivity."""
    global _session_id, _last_active
    
    # Sessions expire after 10 minutes (600s) of inactivity. Refresh if inactive for > 9 mins.
    if not _session_id or (time.time() - _last_active) > 540:
        res = requests.post(f"{BASE_URL}/api/session")
        res.raise_for_status()
        _session_id = res.json()["session_id"]
        
    _last_active = time.time()
    return _session_id

def generate_tts(text: str, model: str = "max"):
    """
    Synthesizes TTS via sproochmaschinn.lu and returns (sample_rate, audio_array)
    Input: string
    Output: (sample_rate, audio_array)
    """
    session_id = _get_active_session()

    # 1. Submit TTS Request
    tts_res = requests.post(
        f"{BASE_URL}/api/tts/{session_id}",
        json={"text": text, "model": model}
    )
    tts_res.raise_for_status()
    request_id = tts_res.json()["request_id"]

    # 2. Poll for the completed result
    while True:
        res = requests.get(f"{BASE_URL}/api/result/{request_id}")
        res.raise_for_status()
        data = res.json()
        
        if data["status"] == "completed":
            b64_audio = data["result"]["data"]
            break
        elif data["status"] in ["failed", "error"]:
            raise RuntimeError(f"TTS API Error: {data}")
        
        # Wait 1 second before polling again (as recommended in their example code)
        time.sleep(1)

    # 3. Decode base64 WAV data into raw bytes
    wav_bytes = base64.b64decode(b64_audio)

    # 4. Load audio data and format exactly how fastrtc expects it
    with wave.open(io.BytesIO(wav_bytes), 'rb') as wf:
        sample_rate = wf.getframerate() # Will be 22050
        num_frames = wf.getnframes()
        raw_audio = wf.readframes(num_frames)
        
        # The API already returns 16-bit PCM, so we parse the buffer directly as int16
        audio_int16 = np.frombuffer(raw_audio, dtype=np.int16)
        
        # Reshape to (1, N) because fastrtc expects a 2D array
        audio_int16 = audio_int16.reshape(1, -1)

    return sample_rate, audio_int16
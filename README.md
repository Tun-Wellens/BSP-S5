# Luxembourgish Real-Time Voice Assistant

This project implements a real-time Luxembourgish voice assistant that uses LuxASR for speech-to-text, a Luxembourgish text-to-speech model provided by Zenter fir d'Lëtzebuerger Sprooch (ZLS), and an LLM to generate responses.

## Credits

This project uses open Luxembourgish language resources provided by:

- Zenter fir d'Lëtzebuerger Sprooch (ZLS): https://zls.lu  
- LuxASR (University of Luxembourg): https://luxasr.uni.lu  

Their speech-to-text and text-to-speech models form the core of this assistant.

## Installation and Setup

### 1. Create a workspace directory
```bash
mkdir voice-assistant
cd voice-assistant
```

### 2. Clone required repositories
```bash
git clone https://github.com/Tun-Wellens/BSP-S5.git
git clone https://github.com/mbarnig/Coqui-TTS.git
git clone https://huggingface.co/denZLS/luxembourgish-male-vits-tts
```

### 3. Pull LFS files for the TTS model
```bash
cd luxembourgish-male-vits-tts
git lfs pull
```
Create an output directory:
```bash
mkdir output
cd ..
```

### 4. Enter the voice assistant project
```bash
cd BSP-S5
```

### 5. Create a .env file
Add your API keys, for example:
```ini
GEMINI_API_KEY=your_key_here
```

### 6. Run the assistant 
```bash
uv run python -m frontend.app
```

### License

This project integrates third-party models whose licenses may apply. Consult the respective repositories for licensing details.
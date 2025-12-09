---
title: Luxembourgish Real-Time Voice Assistant
emoji: 🗣️
colorFrom: red
colorTo: blue
sdk: gradio
sdk_version: 6.0.2
app_file: app.py
pinned: false
license: cc-by-nc-4.0
---

# Luxembourgish Real-Time Voice Assistant

This project implements a real-time Luxembourgish voice assistant that uses LuxASR for speech-to-text, a Luxembourgish text-to-speech model provided by Zenter fir d'Lëtzebuerger Sprooch (ZLS), and an LLM to generate responses.

## Credits

This project uses open Luxembourgish language resources provided by:

- Zenter fir d'Lëtzebuerger Sprooch (ZLS): https://zls.lu  
- LuxASR (University of Luxembourg): https://luxasr.uni.lu  

Their speech-to-text and text-to-speech models form the core of this assistant.

## Installation and Setup

### 1. Clone this repository
```bash
git clone https://github.com/Tun-Wellens/BSP-S5.git
```

### 2. Navigate into the project directory
```bash
cd BSP-S5
```

### 3. Create a .env file
Add your API keys, for example:
```ini
GEMINI_API_KEY=your_key_here
```

### 4. Run the assistant 
```bash
uv run python app.py
```

### License

This project integrates third-party models whose licenses may apply. Consult the respective repositories for licensing details.
# 🏠 Marlene - Smart Home Assistant with Deepgram Voice Agent

A custom smart home assistant that combines Porcupine wake word detection with Deepgram's voice agent API.

## Quick Start

### Step 1: Install Dependencies

```bash
uv sync
```

### Step 2: Add API Keys

```bash
cp .env.example .env
```

Edit `.env` and add:

- `PORCUPINE_ACCESS_KEY=your_key_here`
- `DEEPGRAM_API_KEY=your_key_here`

### Step 3: Run the Program

**Terminal Mode (Recommended for testing):**

```bash
python main.py
```

This listens for "porcupine" wake word and processes voice commands.

**Server Mode (Web Dashboard):**
Terminal 1:

```bash
python server.py
```

Terminal 2:

```bash
python -m http.server 8001 --directory frontend
```

Then open: `http://localhost:8001`

## Features

- Wake word detection using Porcupine
- Voice processing with Deepgram
- Terminal and web dashboard interfaces
- Reusable AudioManager singleton for clean audio device handling

## Project Files

- `main.py` - Terminal mode entry point
- `server.py` - Web server entry point
- `backend/` - Python backend code
- `frontend/` - Web dashboard
- `.env.example` - Copy to `.env` and add your API keys
- `pyproject.toml` - Dependencies

## Configuration

Edit `.env` to customize:

- `PORCUPINE_KEYWORD=porcupine` (wake word)
- `DEEPGRAM_MODEL=nova-2` (AI model)
- `AUDIO_RATE=16000` (sample rate)
- `API_PORT=8000` (server port)

## Architecture

The AudioManager is a singleton that manages PyAudio, allowing both Porcupine and Deepgram to share the same audio device without conflicts.

## Troubleshooting

- List audio devices: `python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"`
- Check API keys at https://console.picovoice.ai/ and https://console.deepgram.com/
- Port in use: `lsof -i :8000`

---

Happy voice controlling! 🎤🏠

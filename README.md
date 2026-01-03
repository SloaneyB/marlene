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
uv run python main.py
```

This listens for "porcupine" wake word and processes voice commands.

**Server Mode (Web Dashboard):**
Terminal 1:

```bash
uv run python server.py
```

Terminal 2:

```bash
uv run python -m http.server 8001 --directory frontend
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

## Future Enhancements

### High Priority

- [ ] **Add Alexa/VoiceMonkey setup instructions** - Document the process for connecting Alexa devices with VoiceMonkey.io API
- [ ] **Add device enum as environment variables** - Move the hardcoded device list from `functions.py` to `.env` for easier configuration
- [ ] **Refactor smart_home_controller.py** - Replace repetitive if/elif chains with the existing `device_trigger_map` dictionary
- [ ] **Implement async/await error handling** - Add proper HTTP response handling and graceful error recovery in smart home controller
- [ ] **Remove unused functions** - Delete `switch_to_tech_mode` and `switch_to_parenting_mode` function definitions (or implement their functionality)

### Smart Home Features

- [ ] **Add brightness control** - Implement the commented-out brightness parameter in function definitions
- [ ] **Add color control** - Implement the commented-out color parameter for RGB-capable devices
- [ ] **Device state tracking** - Keep track of which devices are on/off to avoid redundant API calls
- [ ] **Group control** - Add ability to control multiple devices simultaneously ("turn off all lights")
- [ ] **Scenes/routines** - Create preset device state combinations ("movie mode", "bedtime", etc.)
- [ ] **Add retry logic** - Implement retry mechanism for failed VoiceMonkey API calls

### Voice Agent Improvements

- [ ] **Voice agent timeout configuration** - Make the websocket timeout configurable via environment variables
- [ ] **Implement prompt mode switching** - Actually use the tech/parenting mode functions or remove them
- [ ] **Expand the system prompt** - Add more context and capabilities to the default prompt
- [ ] **Add conversation history** - Store recent exchanges for better context continuity
- [ ] **Custom wake word support** - Allow users to train and use custom Porcupine wake words
- [ ] **Voice activity detection tuning** - Add configuration for sensitivity and silence detection
- [ ] **WebSocket reconnection** - Implement auto-reconnect if Deepgram connection drops

### Code Quality & Robustness

- [ ] **Add logging system** - Replace print statements with Python's logging module for better debugging
- [ ] **Add comprehensive type hints** - Complete type annotations across all modules
- [ ] **Graceful degradation** - Continue basic functions when external services are unavailable
- [ ] **Rate limiting protection** - Prevent excessive API calls to external services
- [ ] **Add unit tests** - Test smart home controller, audio manager, and other core components
- [ ] **Add integration tests** - Test end-to-end voice command flows

### User Experience

- [ ] **Web dashboard enhancements** - Show real-time device status, conversation history, and settings panel
- [ ] **Audio feedback** - Add confirmation beeps or tones for successful actions
- [ ] **Multi-user support** - Different preferences and device configurations per user
- [ ] **Voice feedback customization** - Let users configure response verbosity and style

### Documentation

- [ ] **API documentation** - Document the server endpoints and their usage
- [ ] **Contributing guide** - Add guidelines for contributors
- [ ] **Architecture diagrams** - Visual representation of system components and data flow

## Troubleshooting

- List audio devices: `python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"`
- Check API keys at https://console.picovoice.ai/ and https://console.deepgram.com/
- Port in use: `lsof -i :8000`

---

Happy voice controlling! 🎤🏠

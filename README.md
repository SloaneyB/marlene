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
- `VOICEMONKEY_API_TOKEN=your_token_here`

### Step 3: Configure Smart Home Devices (VoiceMonkey Setup)

Marlene uses [VoiceMonkey.io](https://voicemonkey.io/) in conjunction with Amazon Alexa to control your smart home devices. Follow these steps in [this setup guide](https://github.com/SloaneyB/marlene/blob/main/docs/images/README.md) to configure your smart home w/ VoiceMonkey.io + Amazon Alexa.

### Step 4: Run the Program

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

## Architecture

The AudioManager is a singleton that manages PyAudio, allowing both Porcupine and Deepgram to share the same audio device without conflicts.

## Future Enhancements

### Recently Completed ✅

- [x] **Add VoiceMonkey setup instructions** - Complete setup guide added to README
- [x] **Add device enum as environment variables** - Device list now loaded from `.env` file
- [x] **Refactor smart_home_controller.py** - Replaced repetitive if/elif chains with dynamic endpoint building
- [x] **Implement async/await error handling** - Added proper HTTP response handling and graceful error recovery
- [x] **Remove unused functions** - Delete `switch_to_tech_mode` and `switch_to_parenting_mode` function definitions (or implement their functionality)
- [x] **Add support for Agent Thinking message** - Go through the Deepgram API spec and make sure that we are accounting for every single possible incoming message that might be coming back from Deepgram.
- [x] **Add stop function** - User needs to be able to stop the connection immediately with a phrase like "stop".
- [x] **Voice agent timeout** - Timeout currently set to 10 seconds of no incoming messages from DG. Make it play a sound too.
- [x] **Add logging system** - Replace print statements with Python's logging module for better debugging

### High Priority

- [ ] **BUG!! 10 second timeout config** - It times out when you are in the middle of talking. The logic needs to be to look for 10 seconds of no messages AND userStartedSpeaking = true
- [ ] **Clean up AI slop** - There is a bunch of slop from claude including but not limted to:
  - references to sample rate (and other vars) in config.py file as well as .env as well as the voice_agent_config settings.py
  - The whole thing about screenshots in the docs
  - The whole server.py and browser url
  - The more complex bits like voice_agent.py, audio_manager.py, audio_player.py should be carefully studied and refactored.

- [ ] **Add Supabase integration** - Save important events to a Supabase. Ex: The exact phrase a user says when they want to end the conversation. Or anytime a message comes in that is not one the explicit msg_types, etc.

### Smart Home Features

- [ ] **Add brightness control** - Implement the commented-out brightness parameter in function definitions
- [ ] **Add color control** - Implement the commented-out color parameter for RGB-capable devices
- [ ] **Device state tracking** - Keep track of which devices are on/off to avoid redundant API calls
- [ ] **Group control** - Add ability to control multiple devices simultaneously ("turn off all lights")
- [ ] **Scenes/routines** - Create preset device state combinations ("movie mode", "bedtime", etc.)
- [ ] **Add retry logic** - Implement retry mechanism for failed VoiceMonkey API calls

### Voice Agent Improvements

- [ ] **Custom wake word support** - Allow users to train and use custom Porcupine wake words
- [ ] **Voice activity detection tuning** - Add configuration for sensitivity and silence detection
- [ ] **WebSocket reconnection** - Implement auto-reconnect if Deepgram connection drops
- [ ] **Spotify Controls** - Integration with Spotify and speakers around the house.
- [ ] **Note Taking system** - Allow robust system for user to be able to tell Marlene to create a note or edit an existing note. Examples: grocery list, to do list, etc. Possibly use Supabase or Apple Notes or Google Keep integration. MCP???

### Code Quality & Robustness

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
- [ ] **Add screenshot images** - Capture and add VoiceMonkey dashboard screenshots to `docs/images/` directory

## Troubleshooting

- List audio devices: `python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"`
- Check API keys at https://console.picovoice.ai/ and https://console.deepgram.com/
- Port in use: `lsof -i :8000`
- On Raspberry Pi OS - make sure you install portaudio first! `sudo apt install portaudio19-dev`

---

Happy voice controlling! 🎤🏠

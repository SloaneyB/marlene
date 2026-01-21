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

Marlene uses [VoiceMonkey.io](https://voicemonkey.io/) to control your smart home devices. Follow these steps to set up device control:

#### 3.1: Get Your VoiceMonkey API Token

1. Go to [VoiceMonkey.io](https://voicemonkey.io/) and sign up or log in
2. Navigate to your account settings to find your API token
3. Add it to your `.env` file: `VOICEMONKEY_API_TOKEN=your_token_here`

#### 3.2: Create VoiceMonkey Triggers

For each device you want to control, you must create **TWO triggers** in VoiceMonkey - one for ON and one for OFF.

**Naming Convention (CRITICAL):**

Your VoiceMonkey trigger names MUST follow this exact pattern:

- **ON Trigger:** `<Device Name> ON`
- **OFF Trigger:** `<Device Name> OFF`

**Example Setup for "Living Room Lights":**

1. In VoiceMonkey dashboard, create a new trigger
2. Name it: `Living Room Lights ON`
3. Configure it to turn on your smart device (e.g., smart plug, Alexa routine, etc.)
4. Save

![VoiceMonkey ON Trigger](docs/images/voicemonkey-on-trigger.png)

5. Create another trigger
6. Name it: `Living Room Lights OFF`
7. Configure it to turn off the same smart device
8. Save

![VoiceMonkey OFF Trigger](docs/images/voicemonkey-off-trigger.png)

**More Examples:**

| Device Name        | ON Trigger              | OFF Trigger              |
| ------------------ | ----------------------- | ------------------------ |
| Living Room Lights | `Living Room Lights ON` | `Living Room Lights OFF` |
| Kitchen Light      | `Kitchen Light ON`      | `Kitchen Light OFF`      |
| JJ's Lamp          | `JJ's Lamp ON`          | `JJ's Lamp OFF`          |
| Bedroom Lamp       | `Bedroom Lamp ON`       | `Bedroom Lamp OFF`       |

**Important Notes:**

- Spaces and capitalization in trigger names are fine
- The system automatically converts names to the correct API format
  - Example: `Living Room Lights` → API calls `living-room-lights-on`
- Each trigger connects to your actual smart home device (Alexa routine, smart plug, etc.)

#### 3.3: Add Devices to .env

Once your VoiceMonkey triggers are created, add your devices to the `.env` file:

```bash
SMART_HOME_DEVICES=Living Room Lights, Kitchen Light, Dining Room Light, JJ's Lamp
```

**Tips:**

- Use the exact device names from your VoiceMonkey triggers (without the ON/OFF suffix)
- Separate multiple devices with commas
- Spaces and capitalization are fine - the system normalizes them automatically
- Make sure each device has both ON and OFF triggers in VoiceMonkey

#### 3.4: Future Enhancement - Color & Brightness

The system architecture supports color and brightness control. To enable these features in the future:

**Additional VoiceMonkey Triggers (Optional):**

- `<Device Name> COLOR` - for color changes
- `<Device Name> BRIGHTNESS` - for brightness adjustments

These are not required for basic on/off functionality.

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

### High Priority

- [ ] **Add conversation history** - Store recent exchanges for better context continuity
- [ ] **Add logging system** - Replace print statements with Python's logging module for better debugging
- [ ] **Add MongoDB integration** - Save important events to a MongoDB. Ex: The exact phrase a user says when they want to end the conversation. Or anytime a message comes in that is not one the explicit msg_types, etc.

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

---

Happy voice controlling! 🎤🏠

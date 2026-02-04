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

# VoiceMonkey Screenshot Guide

This directory should contain screenshots of your VoiceMonkey dashboard for the setup guide.

## Required Screenshots

Add the following screenshots to this directory:

1. **voicemonkey-on-trigger.png**
   - Screenshot showing the creation of an ON trigger in VoiceMonkey
   - Example: "Living Room Lights ON" trigger configuration
   - Should show the trigger name and setup interface

2. **voicemonkey-off-trigger.png**
   - Screenshot showing the creation of an OFF trigger in VoiceMonkey
   - Example: "Living Room Lights OFF" trigger configuration
   - Should show the trigger name and setup interface

## How to Capture Screenshots

1. Log into your [VoiceMonkey.io](https://voicemonkey.io/) dashboard
2. Navigate to the trigger creation/configuration page
3. Take screenshots showing:
   - The trigger name field with the naming convention (e.g., "Living Room Lights ON")
   - The configuration interface
   - Any relevant settings

## Tips for Good Screenshots

- Use a clean, uncluttered view
- Make sure the trigger name is clearly visible
- Crop to show only relevant parts of the interface
- Use PNG format for best quality
- Consider adding annotations or arrows to highlight important fields

Once you add these screenshots, they will automatically appear in the main README.md setup guide!

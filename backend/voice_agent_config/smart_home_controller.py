import asyncio
import logging
import requests
import os
from dotenv import load_dotenv
from .utils import normalize_device_name

load_dotenv()

voice_monkey_token = os.getenv("VOICEMONKEY_API_TOKEN")

logger = logging.getLogger(__name__)

async def control_smart_home(parameters):
    """
    Control smart home devices via VoiceMonkey API.
    
    This function dynamically builds VoiceMonkey API endpoints based on the device name
    and action provided. Device names are normalized to lowercase-hyphenated format.
    
    Args:
        parameters: Dictionary containing:
            - device: Natural language device name (e.g., "Living Room Lights")
            - action: One of "on", "off", "change color", "change brightness"
            - color: (optional) Color name for color changes
            - brightness: (optional) Brightness percentage for brightness changes
    
    Example:
        Device: "Living Room Lights", Action: "on"
        → API endpoint: "living-room-lights-on"
    """
    action = parameters.get("action")
    device = parameters.get("device")
    color = parameters.get("color")
    brightness = parameters.get("brightness")
    
    if not action or not device:
        logger.warning(f"Missing required parameters: device={device}, action={action}")
        return
    
    # Normalize device name to VoiceMonkey format
    normalized_device = normalize_device_name(device)
    
    # Build endpoint based on action
    if action == "on":
        endpoint = f"{normalized_device}-on"
    elif action == "off":
        endpoint = f"{normalized_device}-off"
    elif action == "change color":
        endpoint = f"{normalized_device}-color"
        # Future enhancement: pass color parameter to VoiceMonkey
        # This would require VoiceMonkey to support color parameters in triggers
        if color:
            logger.debug(f"Color parameter received: {color}")
    elif action == "change brightness":
        endpoint = f"{normalized_device}-brightness"
        # Future enhancement: pass brightness parameter to VoiceMonkey
        # This would require VoiceMonkey to support brightness parameters in triggers
        if brightness:
            logger.debug(f"Brightness parameter received: {brightness}%")
    else:
        logger.warning(f"Unknown action: {action}")
        return
    
    # Build API URL
    url = f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device={endpoint}"
    
    # Make API call
    try:
        logger.info(f"Triggering VoiceMonkey: {endpoint}")
        await asyncio.to_thread(requests.get, url, timeout=5)
        logger.info(f"Successfully triggered {device} -> {action}")
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout controlling {device}: VoiceMonkey API took too long to respond")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error controlling {device}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error controlling {device}: {e}")

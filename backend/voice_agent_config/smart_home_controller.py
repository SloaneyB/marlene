import asyncio
import requests
import os
from dotenv import load_dotenv
load_dotenv()

voice_monkey_token = os.getenv("VOICEMONKEY_API_TOKEN")

# IMPROVEMENT: Add a function map dictionary here to map the deice names to the VoiceMonkey device triggers
device_trigger_map = {
    "the living room lights": "toggle-the-living-room-lamp",
    "the tall lamp": "toggle-the-living-room-lamp",
    "the living room lamp": "toggle-the-living-room-lamp",
    "the kitchen light": "turn-on-the-kitchen-light",
    "the dining room light": "turn-on-the-dining-room-light",
    "the main lights": "turn-on-the-main-lights",
    "the hallway lights": "turn-on-the-hallway-lights"
}

async def control_smart_home(parameters):
    action = parameters.get("action", None)
    device = parameters.get("device", None)
    
    if action == "off":
        if device == "the living room lights" or device == "the tall lamp" or device == "the living room lamp":
            await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=toggle-the-living-room-lamp"
            )
        elif device == "the kitchen light":
            await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-off-the-kitchen-light"
            )
        elif device == "the dining room light":
             await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-off-the-dining-room-light"
            )
        elif device == "the main lights":
             await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-off-the-main-lights"
            )
        elif device == "the hallway lights":
             await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-off-the-hallway-lights"
            )
        else:
            pass # placeholder for now for other lights not in living room vicinity
    elif action == "on":
        if device == "the living room lights" or device == "the tall lamp" or device == "the living room lamp":
            await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-on-living-room-lamp"
            )
        elif device == "the kitchen light":
            await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-on-the-kitchen-light"
            )
        elif device == "the dining room light":
             await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-on-the-dining-room-light"
            )
        elif device == "the main lights":
             await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-on-the-main-lights"
            )
        elif device == "the hallway lights":
             await asyncio.to_thread(
                requests.get,
                f"https://api-v2.voicemonkey.io/trigger?token={voice_monkey_token}&device=turn-on-the-hallway-lights"
            )
    else:
        pass # placeholder for now

# Function definitions for Marlene Voice Agent
# These functions are provided to the LLM to enable tool use

import os
from dotenv import load_dotenv

load_dotenv()

# Load device list from .env (natural language format)
devices_str = os.getenv("SMART_HOME_DEVICES", "")
DEVICE_LIST = [d.strip() for d in devices_str.split(",") if d.strip()]

FUNCTION_DEFINITIONS = [
    {
        "name": "switch_to_tech_mode",
        "description": "Call this function anytime the user asks a question about AI, machine learning, coding, software development, bitcoin, cryptocurrency, databases, emerging technologies, or a similar technical topic.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "switch_to_parenting_mode",
        "description": "Call this function anytime the user asks for guidance on child development, parenting strategies, health concerns, any related topics, or if the user ever says something about their child.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "control_smart_home",
        "description": "Control smart home devices including lights and lamps. Use this when the user asks to turn devices on/off, adjust brightness, dim lights, change colors, or control any lighting in their home.",
        "parameters": {
            "type": "object",
            "properties": {
                "device": {
                    "type": "string",
                    "description": """The specific smart home device to control. Select the device name that best matches what the user mentioned.
                    
                    Common variations the user might say:
                    - 'Living Room Lights' - Also: 'the tall lamp', 'living room lamp', 'the lamp', 'the main lamp'
                    - 'Kitchen Light' - Also: 'kitchen lights', 'the kitchen light'
                    - 'Dining Room Light' - Also: 'dining room lights', 'the dining room light'
                    - 'Main Lights' - Also: 'overhead lights', 'the main lights'
                    - 'Hallway Lights' - Also: 'hallway light', 'the hallway lights'
                    - 'JJ's Lamp' - Also: 'JJ's light', 'JJs lamp', 'the bedroom lamp'
                    
                    If the user's request is ambiguous (e.g., just says "the lamp" and multiple lamps exist), ask which specific device they mean before calling this function.
                    Always select the exact device name from the enum, even if the user uses a variation.""",
                    "enum": DEVICE_LIST
                },
                "action": {
                    "type": "string",
                    "description": "The action to perform on the device.",
                    "enum": ["on", "off", "change color", "change brightness"]
                },
                "color": {
                    "type": "string",
                    "description": "The color to change the device to (e.g., 'red', 'blue', 'warm white', 'cool white'). Only required when action is 'change color'."
                },
                "brightness": {
                    "type": "string",
                    "description": "The brightness percentage (10-100, in multiples of 5). Only required when action is 'change brightness'.",
                    "enum": ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100"]
                }
            },
            "required": ["device", "action"]
        }
    }
]

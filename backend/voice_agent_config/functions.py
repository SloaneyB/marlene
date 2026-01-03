# Function definitions for Marlene Voice Agent
# These functions are provided to the LLM to enable tool use

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
        "description": "Control smart home devices including lights and lamps. Use this when the user asks to turn devices on/off, adjust brightness, dim lights, or control any lighting in their home.",
        "parameters": {
            "type": "object",
            "properties": {
                # "command": {
                #     "type": "string",
                #     "description": "The natural language command describing what the user wants to do with the smart home device (e.g., 'turn on bedroom light', 'dim living room lamp to 50%', 'turn off all lights')"
                # }
                "device": {
                    "type": "string",
                    "description": "The name of the smart home device which is going to be controlled (e.g., 'bedroom light', 'living room lamp')",
                    # IMPROVEMENT: make this list an env variable so that in the smart_home_controller.py we don't have to manually type in the 
                    "enum": ["the tall lamp", "the living room lights", "the kitchen light", "the dining room light", "the main lights", "the light", "the hallway lights", "JJ's lamp", "JJ's light"]
                },
                "action": {
                    "type": "string",
                    "description": "The action to be performed on the device. For example, turning it off, turning it on, adjusting the brightness, adjusting the color.",
                    "enum": ["on", "off", "change color", "change brightness"]
                },
                # "color": {
                #     "type": "string",
                #     "description": "If the user requests the action of changing the color of a certain device, this parameter is also required. It is the color they wish to change to."
                # },
                # "brightness": {
                #     "type": "string",
                #     "description": "If the user requests the action of changing the birghtness of a certain device, this parameter is also required. It is the percentage they wish to change to. It can be any value that is a multiple of 5 and between 10 percent and 100 percent.",
                #     "enum": ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100"]
                # }
            },
            "required": ["device", "action"]
        }
    }
]

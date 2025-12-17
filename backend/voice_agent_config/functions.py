# Function definitions for Marlene Voice Agent
# These functions are provided to the LLM to enable tool use

FUNCTION_DEFINITIONS = [
    {
        "name": "switch_to_tech_mode",
        "description": "Switch the conversation to technical specialist mode for in-depth discussions about AI, machine learning, coding, software development, bitcoin, cryptocurrency, databases, and emerging technologies. Use this when the user wants to dive deep into technical topics or asks complex technical questions.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "switch_to_parenting_mode",
        "description": "Switch the conversation to pediatric and parenting specialist mode for evidence-based guidance on child development, parenting strategies, health concerns, and related topics. Use this when the user asks about parenting, child development, or pediatric health questions.",
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
                "command": {
                    "type": "string",
                    "description": "The natural language command describing what the user wants to do with the smart home device (e.g., 'turn on bedroom light', 'dim living room lamp to 50%', 'turn off all lights')"
                }
            },
            "required": ["command"]
        }
    }
]

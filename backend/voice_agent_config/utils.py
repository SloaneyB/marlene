"""Utility functions for voice agent configuration."""

def normalize_device_name(device_name: str) -> str:
    """
    Convert natural language device name to VoiceMonkey-compatible format.
    
    Converts to lowercase, replaces spaces with hyphens, and removes apostrophes.
    
    Examples:
        "Living Room Lights" -> "living-room-lights"
        "JJ's Lamp" -> "jjs-lamp"
        "Kitchen Light" -> "kitchen-light"
    
    Args:
        device_name: Natural language device name
        
    Returns:
        Normalized device name suitable for VoiceMonkey API
    """
    return device_name.strip().lower().replace(" ", "-").replace("'", "")

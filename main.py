"""Marlene Smart Home Assistant - Terminal Mode

This script runs the wake word detector in the terminal, listening for the
wake word and processing voice commands via Deepgram when triggered.
"""
import asyncio
import logging
from backend.wake_word_detector import WakeWordDetector
from backend.voice_agent import VoiceAgent
from backend.logging_config import setup_logging
from backend.config import settings

logger = logging.getLogger(__name__)


async def main():
    """Run Marlene in terminal mode with wake word detection."""
    # Initialize logging
    setup_logging(settings.log_level)
    logger.info("Starting Marlene Smart Home Assistant - Terminal Mode")
    
    # Initialize voice agent
    voice_agent = VoiceAgent()
    
    async def on_wake_word_detected():
        """Async callback when wake word is detected."""
        logger.info("Processing voice command")
        detector.pause()  # Release mic for voice agent
        await voice_agent.listen()
        detector.resume()  # Re-acquire mic for wake word detection

    # Initialize and start wake word detector
    detector = WakeWordDetector(on_wake_word=on_wake_word_detected)
    
    try:
        await detector.start()
    except KeyboardInterrupt:
        logger.info("Shutting down")
    finally:
        detector.stop()
        await voice_agent.close()
        logger.info("Goodbye")


if __name__ == "__main__":
    asyncio.run(main())

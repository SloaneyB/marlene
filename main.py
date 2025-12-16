"""Marlene Smart Home Assistant - Terminal Mode

This script runs the wake word detector in the terminal, listening for the
wake word and processing voice commands via Deepgram when triggered.
"""
import asyncio
from backend.wake_word_detector import WakeWordDetector
from backend.voice_agent import VoiceAgent


async def main():
    """Run Marlene in terminal mode with wake word detection."""
    print("\n" + "="*50)
    print("🏠 Marlene Smart Home Assistant - Terminal Mode")
    print("="*50 + "\n")
    
    # Initialize voice agent
    voice_agent = VoiceAgent()
    
    async def on_wake_word_detected():
        """Async callback when wake word is detected."""
        print("Processing voice command...")
        await voice_agent.listen()

    # Initialize and start wake word detector
    detector = WakeWordDetector(on_wake_word=on_wake_word_detected)
    
    try:
        await detector.start()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        detector.stop()
        await voice_agent.close()
        print("Goodbye! 👋\n")


if __name__ == "__main__":
    asyncio.run(main())

"""Wake word detection using Porcupine."""
import asyncio
import struct
import pvporcupine
from typing import Callable, Optional, Awaitable
from backend.audio_manager import AudioManager
from backend.config import settings


class WakeWordDetector:
    """Detects wake word using Porcupine picovoice."""
    
    def __init__(self, on_wake_word: Callable[[], Awaitable[None]]):
        """
        Initialize wake word detector.
        
        Args:
            on_wake_word: Async callback function to execute when wake word is detected
        """
        self.on_wake_word = on_wake_word
        self.audio_manager = AudioManager()
        self.porcupine: Optional[pvporcupine.Porcupine] = None
        self.stream = None
        self.is_listening = False
        
    async def start(self):
        """Start listening for wake word."""
        if self.is_listening:
            print("Wake word detector already running")
            return
        
        print(f"Initializing Porcupine with keyword: '{settings.porcupine_keyword}'")
        
        # Initialize Porcupine
        try:
            self.porcupine = pvporcupine.create(
                access_key=settings.porcupine_access_key,
                keywords=[settings.porcupine_keyword],
                sensitivities=[settings.porcupine_sensitivity]
            )
        except Exception as e:
            print(f"Error initializing Porcupine: {e}")
            raise
        
        # Get audio device
        device_index = self.audio_manager.get_device_index()
        
        # Open audio stream with Porcupine's required settings
        self.stream = self.audio_manager.open_input_stream(
            device_index=device_index,
            rate=self.porcupine.sample_rate,
            chunk_size=self.porcupine.frame_length,
            channels=1
        )
        
        self.is_listening = True
        print(f"\n🎤 Listening for wake word: '{settings.porcupine_keyword}'...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self.is_listening:
                # Read audio chunk
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                # Process audio for wake word
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    print(f"\n✨ Wake word '{settings.porcupine_keyword}' detected!")
                    await self.on_wake_word()
                    print(f"\n🎤 Listening for wake word: '{settings.porcupine_keyword}'...\n")
                    
        except KeyboardInterrupt:
            print("\n\nStopping wake word detection...")
        finally:
            self.stop()
    
    def stop(self):
        """Stop listening and cleanup resources."""
        self.is_listening = False
        
        if self.stream:
            self.audio_manager.close_stream(self.stream)
            self.stream = None
        
        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None
        
        print("Wake word detector stopped")
    
    def __del__(self):
        """Ensure cleanup on deletion."""
        self.stop()

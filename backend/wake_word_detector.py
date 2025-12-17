"""Wake word detection using Porcupine."""
import asyncio
import struct
import pvporcupine
from typing import Callable, Optional, Awaitable
from backend.audio_manager import AudioManager
from backend.config import settings
from dotenv import load_dotenv
import os

load_dotenv()

PORCUPINE_ACCESS_KEY: str = os.getenv("PORCUPINE_ACCESS_KEY")

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
        self._is_paused = False
        self._device_index = None
        
    async def start(self):
        """Start listening for wake word."""
        if self.is_listening:
            print("Wake word detector already running")
            return
        
        print(f"Initializing Porcupine with keyword: '{settings.porcupine_keyword}'")
        
        # Initialize Porcupine (only if not already initialized)
        if not self.porcupine:
            try:
                # self.porcupine = pvporcupine.create(
                #     access_key=settings.porcupine_access_key,
                #     keywords=[settings.porcupine_keyword],
                #     sensitivities=[settings.porcupine_sensitivity]
                # )
                print(f'From Settings, file path = {settings.porcupine_keyword_file_path}')
                self.porcupine = pvporcupine.create(
                    access_key=PORCUPINE_ACCESS_KEY,
                    keyword_paths=[settings.porcupine_keyword_file_path]
                    )

            except Exception as e:
                print(f"Error initializing Porcupine: {e}")
                raise
        
        # Get and store audio device index
        self._device_index = self.audio_manager.get_device_index()
        
        # Open audio stream with Porcupine's required settings
        self._open_stream()
        
        self.is_listening = True
        self._is_paused = False
        print(f"\n🎤 Listening for wake word: '{settings.porcupine_keyword}'...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self.is_listening:
                # Skip processing if paused (stream closed)
                if self._is_paused or not self.stream:
                    await asyncio.sleep(0.1)
                    continue
                
                # Read audio chunk
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                # Process audio for wake word
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    print(f"\n✨ Wake word '{settings.porcupine_keyword}' detected!")
                    await self.on_wake_word()
                    # Only print resume message if not stopped
                    if self.is_listening:
                        print(f"\n🎤 Listening for wake word: '{settings.porcupine_keyword}'...\n")
                    
        except KeyboardInterrupt:
            print("\n\nStopping wake word detection...")
            self.stop()
    
    def _open_stream(self):
        """Open the audio input stream."""
        if self.stream:
            return  # Already open
        
        self.stream = self.audio_manager.open_input_stream(
            device_index=self._device_index,
            rate=self.porcupine.sample_rate,
            chunk_size=self.porcupine.frame_length,
            channels=1
        )
    
    def _close_stream(self):
        """Close the audio input stream."""
        if self.stream:
            self.audio_manager.close_stream(self.stream)
            self.stream = None
    
    def pause(self):
        """
        Pause wake word listening by closing the audio stream.
        Keeps Porcupine initialized for quick resume.
        """
        if self._is_paused:
            return
        
        self._close_stream()
        self._is_paused = True
        print("⏸️  Wake word detector paused")
    
    def resume(self):
        """
        Resume wake word listening by reopening the audio stream.
        """
        if not self._is_paused:
            return
        
        if not self.porcupine:
            print("Cannot resume - Porcupine not initialized")
            return
        
        self._open_stream()
        self._is_paused = False
        print(f"▶️  Wake word detector resumed - listening for '{settings.porcupine_keyword}'...")
    
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

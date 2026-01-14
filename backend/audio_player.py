"""Audio playback for Marlene smart home assistant."""
import queue
import threading
from typing import Optional
from .audio_manager import AudioManager
from .config import settings


class AudioPlayer:
    """
    Real-time audio player with simple queue-based buffering.
    
    Receives audio chunks asynchronously and plays them through
    the configured output device using a background thread.
    """
    
    def __init__(
        self,
        sample_rate: int = None,
        channels: int = None,
        prefer_usb: bool = None
    ):
        """
        Initialize the audio player.
        
        Args:
            sample_rate: Audio sample rate in Hz (defaults to config)
            channels: Number of audio channels (defaults to config)
            prefer_usb: Whether to prefer USB output devices (defaults to config)
        """
        self.sample_rate = sample_rate or settings.audio_output_rate
        self.channels = channels or settings.audio_channels
        self.prefer_usb = prefer_usb if prefer_usb is not None else settings.prefer_usb_audio
        
        self._audio_manager = AudioManager()
        self._queue: queue.Queue[Optional[bytes]] = queue.Queue()
        self._stream = None
        self._playback_thread: Optional[threading.Thread] = None
        self._running = False
    
    def start(self):
        """Start the audio player and begin playback thread."""
        if self._running:
            return
        
        # Get the best output device
        device_index = self._audio_manager.get_output_device_index(
            prefer_usb=self.prefer_usb
        )
        
        # Open the output stream
        self._stream = self._audio_manager.open_output_stream(
            device_index=device_index,
            rate=self.sample_rate,
            channels=self.channels
        )
        
        self._running = True
        self._playback_thread = threading.Thread(
            target=self._playback_loop,
            daemon=True
        )
        self._playback_thread.start()
        print(f"🔊 Audio player started (rate={self.sample_rate}Hz, channels={self.channels})")
    
    def _playback_loop(self):
        """Background thread loop that plays audio from the queue."""
        while self._running:
            try:
                # Wait for audio data with timeout to allow clean shutdown
                audio_data = self._queue.get(timeout=0.1)
                
                if audio_data is None:
                    # Poison pill - stop signal
                    break
                
                # Write audio to the output stream
                if self._stream and self._running:
                    self._stream.write(audio_data)
                    
            except queue.Empty:
                # No data available, continue waiting
                continue
            except Exception as e:
                print(f"❌ Audio playback error: {e}")
                break
    
    def play(self, audio_bytes: bytes):
        """
        Queue audio bytes for playback.
        
        Args:
            audio_bytes: Raw audio data (16-bit PCM expected)
        """
        if self._running:
            self._queue.put(audio_bytes)
    
    def clear(self):
        """
        Clear all buffered audio from the queue.
        
        This immediately stops playback by removing all queued audio chunks.
        The currently playing chunk will finish, but no subsequent audio will play.
        Safe to call even when no audio is playing.
        """
        if not self._running:
            return
        
        # Drain all items from the queue
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        
        print("🔇 Audio buffer cleared")
    
    def stop(self):
        """Stop the audio player and clean up resources."""
        if not self._running:
            return
        
        self._running = False
        
        # Send poison pill to stop the playback thread
        self._queue.put(None)
        
        # Wait for playback thread to finish
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=1.0)
        
        # Close the stream
        if self._stream:
            self._audio_manager.close_stream(self._stream)
            self._stream = None
        
        # Clear any remaining items in the queue
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        
        print("🔇 Audio player stopped")
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False

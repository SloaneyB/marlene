"""Audio device management for Marlene smart home assistant."""
import pyaudio
from typing import Optional
from backend.config import settings


class AudioManager:
    """Manages PyAudio instance and device selection."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one PyAudio instance."""
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize PyAudio instance (only once)."""
        if self._initialized:
            return
            
        self.p = pyaudio.PyAudio()
        self._initialized = True
        self._streams = []
    
    def get_device_index(self, prefer_usb: bool = True) -> Optional[int]:
        """
        Find and return the best available input device index.
        
        Args:
            prefer_usb: If True, tries to find a USB device first
            
        Returns:
            Device index or None to use system default
        """
        print("\n=== Available Audio Devices ===")
        usb_device_idx = None
        
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            name = info.get("name", "")
            max_input_channels = info.get("maxInputChannels", 0)
            
            print(f"Index {i}: {name} (Input channels: {max_input_channels})")
            
            # Look for USB devices
            if prefer_usb and "usb" in name.lower() and max_input_channels > 0:
                if usb_device_idx is None:
                    usb_device_idx = i
        
        print("=" * 35 + "\n")
        
        if usb_device_idx is not None:
            return usb_device_idx
        
        # Fall back to default device
        try:
            default_info = self.p.get_default_input_device_info()
            default_idx = default_info.get('index')
            print(f"Using default input device: {default_info.get('name')} (index {default_idx})")
            return default_idx
        except Exception as e:
            print(f"Warning: Could not get default input device: {e}")
            return None
    
    def get_device_sample_rate(self, device_index: Optional[int] = None) -> int:
        """
        Get the native sample rate of the specified audio input device.
        
        Args:
            device_index: Device index or None for system default
            
        Returns:
            Sample rate in Hz (e.g., 44100, 48000)
        """
        try:
            if device_index is not None:
                device_info = self.p.get_device_info_by_index(device_index)
            else:
                device_info = self.p.get_default_input_device_info()
            
            sample_rate = int(device_info.get('defaultSampleRate', 48000))
            device_name = device_info.get('name', 'Unknown')
            print(f"🎵 Detected sample rate: {sample_rate} Hz for device '{device_name}'")
            return sample_rate
        except Exception as e:
            print(f"Warning: Could not detect sample rate, defaulting to 48000 Hz: {e}")
            return 48000
    
    def open_input_stream(
        self,
        device_index: Optional[int] = None,
        rate: int = None,
        chunk_size: int = None,
        channels: int = None,
        format: int = pyaudio.paInt16
    ) -> pyaudio.Stream:
        """
        Open an audio input stream.
        
        Args:
            device_index: Device index or None for system default
            rate: Sample rate (defaults to config)
            chunk_size: Buffer size (defaults to config)
            channels: Number of channels (defaults to config)
            format: Audio format
            
        Returns:
            PyAudio stream object
        """
        rate = rate or settings.audio_rate
        chunk_size = chunk_size or settings.audio_chunk_size
        channels = channels or settings.audio_channels
        
        stream_kwargs = {
            "format": format,
            "channels": channels,
            "rate": rate,
            "input": True,
            "frames_per_buffer": chunk_size,
        }
        
        if device_index is not None:
            stream_kwargs["input_device_index"] = device_index
        
        stream = self.p.open(**stream_kwargs)
        self._streams.append(stream)
        return stream
    
    def close_stream(self, stream: pyaudio.Stream):
        """Close a specific stream."""
        if stream in self._streams:
            stream.stop_stream()
            stream.close()
            self._streams.remove(stream)
    
    def close_all_streams(self):
        """Close all open streams."""
        for stream in self._streams[:]:
            self.close_stream(stream)
    
    def cleanup(self):
        """Clean up all resources."""
        self.close_all_streams()
        if self.p:
            self.p.terminate()
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup()

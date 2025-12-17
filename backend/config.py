"""Configuration management for Marlene smart home assistant."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    porcupine_access_key: str
    deepgram_api_key: str
    
    # Audio settings
    audio_rate: int = 16000
    audio_output_rate: int = 16000  # Deepgram agent output sample rate
    audio_chunk_size: int = 1024
    audio_channels: int = 1
    prefer_usb_audio: bool = True  # Prefer USB devices for input/output
    echo_cancel_source: str | None = None  # PulseAudio echo-cancelled source name (Linux only)
    
    # Porcupine settings
    porcupine_keyword: str = "Hey Marlene"  # custom keyword
    porcupine_sensitivity: float = 0.5
    porcupine_keyword_file_path: str = "./backend/porcupine_config/hey-marlene_mac.ppn"
    
    # Deepgram settings
    deepgram_model: str = "nova-2"
    deepgram_language: str = "en-US"
    
    # Server settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
